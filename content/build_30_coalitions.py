"""Bounded coalition framework: invitations, subsidies, exits and finite rounds.

A01 removes calendar-driven coalition/treaty execution. Rounds advance from
political state and prior-round completion; the dates below are documentation
metadata only. Alternate territorial outcomes are implemented separately by A03.
"""
import json
from pdx import Entry,parse,dumps,walk
from build_10_era import change

ROSTER='HAB PRU RUS SPR POR SWE DEN NET SAR NAP BAV SAX'.split()
ROUNDS=[
 (1,'First Coalition','1792.4.19','FRA = { has_country_flag = french_revolutionary_path has_war = yes }','HAB PRU SPR POR SAR NAP NET'),
 (2,'Second Coalition','1798.1.1','FRA = { OR = { has_country_flag = directory_active has_country_flag = consulate_established } }','HAB RUS POR NAP'),
 (3,'Third Coalition','1805.1.1','FRA = { has_country_flag = empire_of_the_french }','HAB RUS SWE NAP'),
 (4,'Fourth Coalition','1806.1.1','FRA = { has_country_flag = empire_of_the_french }','PRU RUS SWE SAX'),
 (5,'Fifth Coalition','1809.1.1','FRA = { has_country_flag = empire_of_the_french }','HAB POR SPR'),
 (6,'Sixth Coalition','1813.1.1','FRA = { has_country_flag = grande_armee_destroyed }','PRU RUS HAB SWE POR SPR'),
 (7,'Seventh Coalition','1815.1.1','FRA = { has_country_flag = hundred_days }','PRU RUS HAB POR'),
]
OPENING=[
 ('theatre','napoleonic_end_theatre_war','DEN','SWE','nap_theatre_war_active','nap_theatre_war_ended','theatre_war_active','theatre_war_active','1789.7.8',1,101),
 ('varala','napoleonic_end_russo_swedish_war','SWE','RUS','nap_russo_swedish_war_active','nap_treaty_varala_signed','russo_swedish_war_active','russo_swedish_war_active','1790.8.13',2,102),
 ('sistova','napoleonic_end_austro_turkish_war','HAB','TUR','nap_austro_turkish_war_active','nap_treaty_sistova_signed','at_war_with_ottomans','austro_turkish_war_active','1791.8.3',3,103),
 ('jassy','napoleonic_end_russo_turkish_jassy','RUS','TUR','nap_russo_turkish_war_active','nap_treaty_jassy_signed','russo_turkish_war_active','russo_turkish_war_active','1792.1.8',4,104),
]


def eligible_round(number,finished,*,french_context=True,host_free=True):
    return french_context and host_free and number not in finished and (number==1 or number-1 in finished)


def transfer_subsidy(donor,recipient,active=True):
    if not active or donor<15 or recipient>85:return None
    return donor-15,recipient+15


def settle_model(state,*,winner,loser,jassy=False):
    result={**state,'wars':set(state['wars']),'resolved':set(state['resolved']),'owners':dict(state['owners'])}
    pair=frozenset((winner,loser))
    if pair in result['resolved'] or pair not in result['wars']:return result
    result['resolved'].add(pair);result['wars'].discard(pair)
    if jassy and winner=='RUS' and loser=='TUR' and result['owners'].get(192)=='TUR':
        result['owners'][192]='RUS'
    if jassy and winner=='TUR' and loser=='RUS' and result['owners'].get(192)=='RUS':
        result['owners'][192]='TUR'
    return result

def _winner_terms(winner,loser):
    """Bounded political settlement used when no approved territorial term exists."""
    return f'''{winner} = {{ add_stability = 0.04 add_war_support = 0.03 add_political_power = 75 }}
{loser} = {{ add_stability = -0.04 add_war_support = -0.03 add_political_power = -50 }}'''


def opening_effects():
    result=[]
    for key,effect,a,b,active,done,aflag,bflag,_,_,news in OPENING:
        for winner,loser in ((a,b),(b,a)):
            transfer=''
            if key=='jassy' and winner=='RUS':
                transfer='if = { limit = { 192 = { is_owned_by = TUR } RUS = { exists = yes } } RUS = { transfer_state = 192 } 192 = { add_core_of = RUS remove_core_of = TUR } }'
            elif key=='jassy' and winner=='TUR':
                transfer='if = { limit = { 192 = { is_owned_by = RUS } TUR = { exists = yes } } TUR = { transfer_state = 192 } 192 = { add_core_of = TUR remove_core_of = RUS } }'
            suffix='a_victory' if winner==a else 'b_victory'
            result.append(f'''{effect}_{suffix} = {{
 if = {{ limit = {{ has_global_flag = {active} {a} = {{ has_war_with = {b} }} NOT = {{ has_global_flag = nap_opening_peace_busy }} }}
  set_global_flag = nap_opening_peace_busy
  clr_global_flag = {active}
  set_global_flag = {done}
  {a} = {{ clr_country_flag = {aflag} }}
  {b} = {{ clr_country_flag = {bflag} }}
  if = {{ limit = {{ {a} = {{ has_war_with = {b} }} }} {a} = {{ white_peace = {b} }} }}
  {transfer}
  {_winner_terms(winner,loser)}
  {winner} = {{ news_event = {{ id = napoleonic_diplomacy.{news} hours = 6 }} }}
  clr_global_flag = nap_opening_peace_busy
 }}
}}''')
        result.append(f'''{effect} = {{
 if = {{ limit = {{ has_global_flag = {active} {a} = {{ has_war_with = {b} }} }} {effect}_a_victory = yes }}
}}''')
    return '\n'.join(result)+'\n'


def cap_guard(reverse=False):
    loser,winner=('FROM','ROOT') if reverse else ('ROOT','FROM')
    parts=[]
    for key,effect,a,b,active,*_ in OPENING:
        parts.append(f'if = {{ limit = {{ has_global_flag = {active} {loser} = {{ tag = {a} }} {winner} = {{ tag = {b} }} }} {effect}_b_victory = yes }}')
        parts.append(f'if = {{ limit = {{ has_global_flag = {active} {loser} = {{ tag = {b} }} {winner} = {{ tag = {a} }} }} {effect}_a_victory = yes }}')
    parts.append(f'''if = {{ limit = {{ has_global_flag = nap_coalition_active NOT = {{ has_global_flag = nap_coalition_peace_busy }} }}
 if = {{ limit = {{ {loser} = {{ tag = FRA }} {winner} = {{ has_country_flag = nap_coalition_member }} }} nap_coalition_coalition_victory_settlement = yes }}
 else_if = {{ limit = {{ {winner} = {{ tag = FRA }} {loser} = {{ tag = ENG has_country_flag = nap_coalition_member }} }} nap_coalition_french_victory_settlement = yes }}
 else_if = {{ limit = {{ {winner} = {{ tag = FRA }} {loser} = {{ has_country_flag = nap_coalition_member }} }} {loser} = {{ nap_coalition_separate_peace = yes }} }}
}}''')
    return '\n'.join(parts)


def build(root):
    output={}
    loc=['\ufeffl_english:',' nap_coalition_council:0 "Coalition Diplomacy"',' nap_coalition_council_desc:0 "Membership is voluntary. Funding, separate peace and re-entry depend on the current round and resources. A coalition settlement is limited, not a license to annex defeated countries."',' nap_coalition_superseded:0 "The diplomatic situation has changed."',' nap_coalition_coordination:0 "Coalition Staff Coordination"',' nap_coalition_coordination_desc:0 "Shared planning arrangements improve staff work, but do not replace each government."',' nap_coalition_template_name:0 "Coalition Council"',' nap_coalition_manifest_name:0 "A Negotiated European Settlement"',' nap_coalition_manifest_desc:0 "This coalition seeks a bounded settlement. Its political and territorial terms are scripted, not a standard total-war partition."']
    triggers=['nap_coalition_candidate = { OR = { '+' '.join('tag = '+t for t in ROSTER)+' } exists = yes is_subject = no NOT = { has_country_flag = nap_coalition_cooldown } NOT = { is_in_faction_with = FRA } OR = { is_in_faction = no is_in_faction_with = ENG } }']
    effects,events,decisions=[],['add_namespace = nap_coalition'],['nap_coalition_council = {']
    output['common/factions/templates/nap_coalitions.txt']='nap_coalition_template = { name = nap_coalition_template_name icon = GFX_faction_logo_generic_16 manifest = nap_coalition_manifest visible = { always = no } }\n'
    output['common/factions/goals/nap_coalitions.txt']='nap_coalition_manifest = { name = nap_coalition_manifest_name description = nap_coalition_manifest_desc is_manifest = yes ratio_progress = { total_amount = 1 completed_amount = 0 } }\n'
    for n,name,date,context,roster in ROUNDS:
        previous=f'has_global_flag = nap_coalition_{n-1}_finished' if n>1 else ''
        guard=f'tag = ENG exists = yes is_subject = no is_in_faction = no NOT = {{ has_global_flag = nap_coalition_active }} NOT = {{ has_country_flag = nap_coalition_cooldown }} NOT = {{ has_global_flag = nap_coalition_{n}_finished }} {previous} {context} NOT = {{ is_in_faction_with = FRA }}'
        triggers.append(f'nap_coalition_{n}_eligible = {{ {guard} }}')
        invites='\n'.join(f'{tag} = {{ if = {{ limit = {{ nap_coalition_candidate = yes }} set_country_flag = {{ flag = nap_invited_round_{n} days = 60 }} country_event = {{ id = nap_coalition.{100+n} days = 3 }} }} }}' for tag in roster.split())
        effects.append(f'''nap_coalition_start_{n} = {{ if = {{ limit = {{ nap_coalition_{n}_eligible = yes }}
 nap_era_initialize = yes
 create_faction_from_template = {{ template = nap_coalition_template name = nap_coalition_{n}_name }}
 if = {{ limit = {{ has_faction_template = nap_coalition_template is_faction_leader = yes }}
 set_global_flag = nap_coalition_active
 set_country_flag = nap_coalition_host
 set_country_flag = nap_coalition_member
 set_variable = {{ nap_coalition_round = {n} }}
 add_ideas = nap_coalition_coordination
 if = {{ limit = {{ NOT = {{ has_war_with = FRA }} }} declare_war_on = {{ target = FRA type = annex_everything }} }}
 {invites}
 }}
}} }}''')
        events.append(f'''country_event = {{ id = nap_coalition.{n} title = nap_coalition.{n}.t desc = nap_coalition.{n}.d picture = GFX_report_event_generic_assembly fire_only_once = yes
 trigger = {{ nap_coalition_{n}_eligible = yes }} mean_time_to_happen = {{ days = 14 }}
 option = {{ name = nap_coalition.{n}.a ai_chance = {{ factor = 80 }} trigger = {{ nap_coalition_{n}_eligible = yes }} nap_coalition_start_{n} = yes }}
 option = {{ name = nap_coalition.{n}.b ai_chance = {{ factor = 20 }} if = {{ limit = {{ nap_coalition_{n}_eligible = yes }} set_global_flag = nap_coalition_{n}_finished set_country_flag = {{ flag = nap_coalition_cooldown days = 365 }} }} }}
}}''')
        accept=f'nap_coalition_candidate = yes has_country_flag = nap_invited_round_{n} has_global_flag = nap_coalition_active ENG = {{ has_country_flag = nap_coalition_host has_faction_template = nap_coalition_template is_faction_leader = yes check_variable = {{ nap_coalition_round = {n} }} has_war_with = FRA }} NOT = {{ check_variable = {{ nap_treasury < 8 }} }}'
        events.append(f'''country_event = {{ id = nap_coalition.{100+n} title = nap_coalition.{100+n}.t desc = nap_coalition.{100+n}.d picture = GFX_report_event_generic_assembly is_triggered_only = yes
 immediate = {{ nap_era_initialize = yes }}
 option = {{ name = nap_coalition.{100+n}.a ai_chance = {{ factor = 75 }} trigger = {{ {accept} }}
  if = {{ limit = {{ {accept} }} clr_country_flag = nap_invited_round_{n} set_country_flag = nap_coalition_member set_variable = {{ nap_member_round = {n} }} {change('treasury',-8)} ENG = {{ add_to_faction = ROOT }} add_ideas = nap_coalition_coordination if = {{ limit = {{ NOT = {{ has_war_with = FRA }} }} declare_war_on = {{ target = FRA type = annex_everything }} }} nap_era_clamp = yes }}
 }}
 option = {{ name = nap_coalition.{100+n}.b ai_chance = {{ factor = 25 }} clr_country_flag = nap_invited_round_{n} set_country_flag = {{ flag = nap_coalition_cooldown days = 180 }} }}
}}''')
        loc += [f' nap_coalition_{n}_name:0 "{name}"',f' nap_coalition.{n}.t:0 "Organizing the {name}"',f' nap_coalition.{n}.d:0 "The current French crisis permits a new coalition. Britain can organize a temporary alliance and invite the relevant governments. Invitations are not automatic declarations on their behalf. Existing unrelated factions are not replaced."',f' nap_coalition.{n}.a:0 "Open the coalition council and commit Britain."',f' nap_coalition.{n}.b:0 "Decline this round of commitments."',f' nap_coalition.{100+n}.t:0 "Invitation to the {name}"',f' nap_coalition.{100+n}.d:0 "Britain proposes joint action against France. Joining costs 8 treasury and commits us to the war, but retains a route to separate peace. Refusal does not create a war or transfer territory."',f' nap_coalition.{100+n}.a:0 "Commit to this coalition."',f' nap_coalition.{100+n}.b:0 "Remain outside the coalition."']
    finished='\n'.join(f'if = {{ limit = {{ ENG = {{ check_variable = {{ nap_coalition_round = {n} }} }} }} set_global_flag = nap_coalition_{n}_finished }}' for n in range(1,8))
    effects.append(f'''nap_coalition_french_victory_settlement = {{
 if = {{ limit = {{ has_global_flag = nap_coalition_active }}
  FRA = {{ add_stability = 0.05 add_war_support = 0.04 add_political_power = 100 }}
  ENG = {{ if = {{ limit = {{ exists = yes }} add_stability = -0.03 add_political_power = -50 }} }}
  nap_coalition_end_round = yes
 }}
}}
nap_coalition_coalition_victory_settlement = {{
 if = {{ limit = {{ has_global_flag = nap_coalition_active }}
  FRA = {{ add_stability = -0.06 add_war_support = -0.05 add_political_power = -100 }}
  ENG = {{ if = {{ limit = {{ exists = yes }} add_stability = 0.04 add_political_power = 75 }} }}
  nap_coalition_end_round = yes
 }}
}}
nap_coalition_end_round = {{
 if = {{ limit = {{ has_global_flag = nap_coalition_active NOT = {{ has_global_flag = nap_coalition_peace_busy }} }}
  set_global_flag = nap_coalition_peace_busy clr_global_flag = nap_coalition_active
  {finished}
  every_country = {{ limit = {{ is_in_faction_with = ENG has_faction_template = nap_coalition_template ENG = {{ has_country_flag = nap_coalition_host has_faction_template = nap_coalition_template }} }} set_country_flag = nap_coalition_member }}
  every_country = {{ limit = {{ has_country_flag = nap_coalition_member }}
   clr_country_flag = nap_coalition_member set_country_flag = nap_coalition_settlement_pending
   set_country_flag = {{ flag = nap_coalition_cooldown days = 365 }}
   remove_ideas = nap_coalition_coordination
   if = {{ limit = {{ NOT = {{ tag = ENG }} is_in_faction_with = ENG ENG = {{ has_country_flag = nap_coalition_host has_faction_template = nap_coalition_template }} }} ENG = {{ remove_from_faction = PREV }} }}
  }}
  ENG = {{ if = {{ limit = {{ has_country_flag = nap_coalition_host has_faction_template = nap_coalition_template is_faction_leader = yes }} dismantle_faction = yes }} clr_country_flag = nap_coalition_host }}
  every_country = {{ limit = {{ has_country_flag = nap_coalition_settlement_pending }}
   clr_country_flag = nap_coalition_settlement_pending
   if = {{ limit = {{ has_war_with = FRA }} white_peace = FRA }}
   nap_era_initialize = yes {change('war_exhaustion',-8)} nap_era_clamp = yes
  }}
  clr_global_flag = nap_coalition_peace_busy
 }}
}}
nap_coalition_separate_peace = {{
 if = {{ limit = {{ has_country_flag = nap_coalition_member NOT = {{ has_global_flag = nap_coalition_peace_busy }} }}
  if = {{ limit = {{ tag = ENG }} nap_coalition_end_round = yes }}
  else = {{
   set_global_flag = nap_coalition_peace_busy
   clr_country_flag = nap_coalition_member clr_country_flag = nap_coalition_peace_requested
   set_country_flag = {{ flag = nap_coalition_cooldown days = 365 }} remove_ideas = nap_coalition_coordination
   if = {{ limit = {{ is_in_faction_with = ENG ENG = {{ has_country_flag = nap_coalition_host has_faction_template = nap_coalition_template }} }} ENG = {{ remove_from_faction = PREV }} }}
   if = {{ limit = {{ has_war_with = FRA }} white_peace = FRA }}
   nap_era_initialize = yes {change('war_exhaustion',-8)} nap_era_clamp = yes
   clr_global_flag = nap_coalition_peace_busy
  }}
 }}
}}
''')
    for i,tag in enumerate(['ENG']+ROSTER):
        request=f'tag = {tag} has_country_flag = nap_coalition_member has_war_with = FRA NOT = {{ has_country_flag = nap_coalition_peace_requested }} NOT = {{ has_country_flag = nap_coalition_peace_refused }}'
        peace_valid=f'tag = FRA {tag} = {{ has_country_flag = nap_coalition_peace_requested has_country_flag = nap_coalition_member has_war_with = FRA }}'
        decisions.append(f'nap_coalition_peace_{tag} = {{ icon = generic_political_discourse cost = 25 days_re_enable = 180 visible = {{ tag = {tag} has_country_flag = nap_coalition_member }} available = {{ {request} }} complete_effect = {{ if = {{ limit = {{ {request} }} set_country_flag = {{ flag = nap_coalition_peace_requested days = 90 }} FRA = {{ country_event = {{ id = nap_coalition.{200+i} days = 1 }} }} }} }} ai_will_do = {{ factor = 0 modifier = {{ add = 5 check_variable = {{ nap_war_exhaustion > 60 }} }} }} }}')
        events.append(f'''country_event = {{ id = nap_coalition.{200+i} title = nap_coalition.{200+i}.t desc = nap_coalition.{200+i}.d picture = GFX_report_event_generic_assembly is_triggered_only = yes
 option = {{ name = nap_coalition_peace_accept trigger = {{ {peace_valid} }} ai_chance = {{ factor = 80 }} if = {{ limit = {{ {peace_valid} }} {tag} = {{ nap_coalition_separate_peace = yes }} }} }}
 option = {{ name = nap_coalition_peace_refuse trigger = {{ {peace_valid} }} ai_chance = {{ factor = 20 }} if = {{ limit = {{ {peace_valid} }} {tag} = {{ clr_country_flag = nap_coalition_peace_requested set_country_flag = {{ flag = nap_coalition_peace_refused days = 180 }} }} add_political_power = -15 }} }}
 option = {{ name = nap_coalition_superseded trigger = {{ NOT = {{ {peace_valid} }} }} }}
}}''')
        loc += [f' nap_coalition_peace_{tag}:0 "Seek a Negotiated Coalition Settlement"',f' nap_coalition_peace_{tag}_desc:0 "Ask France for a bounded peace. France may refuse. A British settlement closes the whole coalition round; another participant can leave separately. No new borders are imposed."',f' nap_coalition.{200+i}.t:0 "A Coalition Government Seeks Peace"',f' nap_coalition.{200+i}.d:0 "The government of {tag} has offered a limited settlement. Acceptance restores peace without annexation; refusal costs political capital and the war continues. Detailed alternate-winner terms remain a separate approved design task."']
        if tag=='ENG':continue
        subsidy=f'tag = ENG has_country_flag = nap_coalition_host has_global_flag = nap_coalition_active NOT = {{ check_variable = {{ nap_treasury < 15 }} }} {tag} = {{ has_country_flag = nap_coalition_member has_war_with = FRA NOT = {{ check_variable = {{ nap_treasury > 85 }} }} }}'
        effects.append(f'nap_coalition_subsidize_{tag} = {{ if = {{ limit = {{ {subsidy} }} {change("treasury",-15)} {tag} = {{ {change("treasury",15)} {change("war_exhaustion",-3)} nap_era_clamp = yes }} nap_era_clamp = yes }} }}')
        decisions.append(f'nap_coalition_subsidy_{tag} = {{ icon = generic_prepare_civil_war cost = 20 days_re_enable = 180 visible = {{ tag = ENG {tag} = {{ has_country_flag = nap_coalition_member }} }} available = {{ {subsidy} }} complete_effect = {{ nap_coalition_subsidize_{tag} = yes }} ai_will_do = {{ factor = 1 }} }}')
        loc += [f' nap_coalition_subsidy_{tag}:0 "Subsidize {tag}"',f' nap_coalition_subsidy_{tag}_desc:0 "Transfer exactly 15 treasury from Britain to this active coalition participant, reducing its exhaustion by 3. The recipient must have room below the treasury cap. This is a transfer, not newly created money."']
    loc += [' nap_coalition_peace_accept:0 "Accept a limited settlement."',' nap_coalition_peace_refuse:0 "Continue the campaign."']
    decisions.append('}')
    output['common/scripted_triggers/nap_coalitions.txt']='\n'.join(triggers)+'\n'
    output['common/scripted_effects/nap_coalitions.txt']='\n'.join(effects)+'\n'
    output['events/06_coalitions.txt']='\n\n'.join(events)+'\n'
    output['common/decisions/nap_coalitions.txt']='\n'.join(decisions)+'\n'
    output['common/decisions/categories/nap_coalitions.txt']='nap_coalition_council = { icon = generic_political_discourse allowed = { always = yes } visible = { OR = { tag = FRA tag = ENG has_country_flag = nap_coalition_member } } }\n'
    output['common/ideas/nap_coalitions.txt']='ideas = { country = { nap_coalition_coordination = { picture = generic_army_bonus allowed = { always = yes } removal_cost = -1 modifier = { planning_speed = 0.03 } } } }\n'
    output['localisation/english/nap_coalitions_l_english.yml']='\n'.join(loc)+'\n'
    output['common/on_actions/nap_coalitions.txt']='''on_actions = {
 on_monthly = { effect = {
  if = { limit = { has_country_flag = nap_coalition_member NOT = { has_war_with = FRA } } nap_coalition_separate_peace = yes }
  if = { limit = { tag = ENG has_global_flag = nap_coalition_active OR = { NOT = { FRA = { exists = yes } } NOT = { has_faction_template = nap_coalition_template } } } nap_coalition_end_round = yes }
 } }
 on_capitulation_immediate = { effect = {
'''+cap_guard()+'''\n } }
 on_before_peace_conference_start = { effect = {
'''+cap_guard(True)+'''\n } }
}'''
    output['docs/coalition-rounds.json']=json.dumps([dict(round=n,name=name,earliest=date,context=context,invitees=tags.split()) for n,name,date,context,tags in ROUNDS],indent=2)+'\n'
    output['docs/coalition-framework.md']='''# Coalition framework (Milestone 4 slice)

Seven finite rounds share a British convenor, candidate checks, consent events, paid subsidies, membership flags, exhaustion-aware peace requests and re-entry cooldowns. Dates are eligibility floors; neither invitations nor foreign declarations occur merely because a date is reached. Britain can decline a round, and invitees can refuse without being forced into war.

The framework creates its own temporary native faction only when Britain is independent and faction-free. It does not dismantle unrelated factions or recruit their members. The inherited British coalition focus becomes a readiness flag rather than creating an incompatible permanent faction early.

Twelve subsidy decisions transfer 15 treasury from donor to recipient without exceeding the cap. Thirteen participant peace requests can be accepted or rejected by France; British acceptance closes the round, while another participant can leave separately. Participants detach before white peace. Automatically attached subject members are included in end-of-round cleanup. Template checks protect unrelated factions. Flags and transaction locks precede peace callbacks.

Opening-war settlements are no longer fired by historical dates. Capitulation and pre-conference hooks settle them; A03 adds outcome-aware bounded terms. Jassy changes state 192 only if still Ottoman-owned; core edits use state scope. Capitulation and pre-conference hooks have opposite ROOT/FROM conventions. Third-party victories do not grant Russia a treaty windfall.

A03 makes opening-war and coalition-capitulation settlements outcome-aware. Historical terms are applied only to the historical winner; reverse outcomes receive bounded political terms, and the Russo-Turkish reverse outcome restores state 192 only if Russia actually owns it. Britain remains the convenor; fallback leadership and deeper war-goal-specific territorial catalogues remain future work. The faction manifest is a neutral placeholder, not a progression reward. Native faction/peace behavior requires a real engine test. The source protects the intended transactions but does not establish how every simultaneous-war callback behaves in HOI4.
'''
    return output


def postprocess(outputs,root):
    old=parse((root/'content/legacy/m2_diplomacy.txt').read_text(encoding='utf-8-sig'))
    setup=next(e for e in old if e.key=='napoleonic_setup_1789_diplomacy')
    result={'common/scripted_effects/napoleonic_diplomacy_setup.txt':dumps([setup])+opening_effects()}
    result['common/on_actions/napoleonic_on_actions.txt']='on_actions = { on_startup = { effect = { FRA = { napoleonic_setup_1789_map = yes napoleonic_setup_1789_diplomacy = yes news_event = { id = napoleonic_timeline.0 days = 1 } } } } }\n'
    events=parse((root/'content/legacy/m2_events.txt').read_text(encoding='utf-8-sig'))
    for event in events:
        if event.key!='country_event':continue
        row=next(r for r in OPENING if event.scalar('id')=='napoleonic_diplomacy.'+str(r[9]))
        event.value=[e for e in event.value if e.key not in ('immediate','trigger','mean_time_to_happen')]
        if not event.children('is_triggered_only'):
            event.value.append(Entry('is_triggered_only','yes'))
        event.value.append(Entry('immediate',parse(row[1]+' = yes')))
        for option in event.children('option'):
            option.value=[e for e in option.value if e.key in ('name','trigger','ai_chance')]
    result['events/04_1789_diplomacy.txt']=dumps(events)
    eng=parse((root/'content/legacy/ENG.txt').read_text(encoding='utf-8-sig'))
    for node in walk(eng):
        if node.key=='create_faction' and node.value=='coalition_against_france':
            node.key='set_country_flag';node.value='nap_coalition_host_request'
    result['common/national_focus/ENG.txt']=dumps(eng)
    return result
