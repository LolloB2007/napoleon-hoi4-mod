"""Reusable, country-scoped era mechanics. All numeric balance is provisional."""
import json

TAGS = 'FRA ENG HAB PRU RUS SPR POR TUR SWE DEN POL NET NAP SAR PAP VEN TUS BAV SAX HAN WUR ITA BAT HOL WES RHC WAR'.split()
DEFAULTS = {'treasury':50, 'debt':0, 'legitimacy':55, 'fervor':0, 'war_exhaustion':0, 'army_prestige':50, 'reform':0, 'supply_pressure':0}
# name, title, PP cost, cooldown, minima, maxima, deltas, extra condition, extra effect, description
ACTIONS = [
 ('bonds','Issue a Limited War Loan',35,180,{}, {'debt':70}, {'treasury':25,'debt':25,'legitimacy':-3},'','', 'Borrow against future revenue. Treasury +25, debt +25, legitimacy -3. High debt drains the treasury each month.'),
 ('repay','Retire State Debt',25,90,{'treasury':20,'debt':20},{},{'treasury':-20,'debt':-20,'legitimacy':2},'','', 'Spend 20 treasury to retire 20 debt and restore 2 legitimacy.'),
 ('audit','Audit the Revenue Offices',35,180,{'treasury':10},{'reform':95},{'treasury':-10,'reform':5,'legitimacy':3},'','', 'Pay 10 treasury for an administrative audit: reform +5 and legitimacy +3.'),
 ('recruit','Recruit a Limited Volunteer Contingent',50,365,{'treasury':12},{'war_exhaustion':70},{'treasury':-12,'war_exhaustion':4},'','add_manpower = 5000', 'Raise 5,000 volunteers at a cost of 12 treasury and 4 exhaustion. This does not change the conscription law.'),
 ('levee','Authorize an Emergency Levee',65,365,{'treasury':20,'fervor':35},{'war_exhaustion':60},{'treasury':-20,'war_exhaustion':12,'fervor':-10,'legitimacy':-4},'tag = FRA has_war = yes has_country_flag = french_revolutionary_path','add_manpower = 12000', 'Mobilize 12,000 men. Treasury -20, fervor -10, exhaustion +12 and legitimacy -4. Available only to revolutionary France at war.'),
 ('magazines','Fund Forward Magazines',35,120,{'treasury':15},{},{'treasury':-15,'supply_pressure':-12},'has_war = yes','add_timed_idea = { idea = nap_funded_magazines days = 90 }', 'Spend 15 treasury to reduce supply pressure by 12 and maintain temporary supply depots for 90 days.'),
 ('rest','Rotate Exhausted Formations',30,90,{'treasury':10,'war_exhaustion':8},{},{'treasury':-10,'war_exhaustion':-8,'army_prestige':-2},'has_war = yes','add_timed_idea = { idea = nap_army_rotation days = 45 }', 'Exhaustion -8 at the cost of 10 treasury, 2 prestige and a temporary reduction in operational tempo.'),
 ('requisition','Authorize Local Requisitions',20,120,{}, {'war_exhaustion':80},{'treasury':10,'supply_pressure':-6,'war_exhaustion':8,'legitimacy':-5},'has_war = yes','', 'Ease immediate supply pressure, but transfer the burden to civilians: treasury +10, supply pressure -6, exhaustion +8, legitimacy -5.'),
 ('staff','Expand the Staff College',45,180,{'treasury':15},{'reform':94},{'treasury':-15,'reform':6},'','army_experience = 10', 'Fund professional training: treasury -15, reform +6 and 10 army experience. The reform meter is capped at 100.'),
 ('relief','Relieve Distressed Communities',40,120,{'treasury':15},{'legitimacy':94},{'treasury':-15,'legitimacy':6,'war_exhaustion':-3},'','', 'Spend 15 treasury to restore 6 legitimacy and remove 3 exhaustion.'),
 ('demobilize','Normalize the Peacetime Establishment',35,180,{'war_exhaustion':10},{},{'war_exhaustion':-10,'legitimacy':3},'has_war = no','', 'Reduce wartime administrative burdens after peace: exhaustion -10 and legitimacy +3. Does not delete divisions or duplicate manpower.'),
 ('commissions','Review Officer Commissions',35,180,{'treasury':10},{'army_prestige':94},{'treasury':-10,'army_prestige':6,'reform':2},'','', 'Promote demonstrated competence within the officer corps: treasury -10, national army prestige +6 and reform +2.')
]

IDEAS = {
 'nap_war_weariness':('War Weariness','army_org_factor = -0.04 political_power_factor = -0.05','Exhaustion is impairing recruitment and field cohesion.'),
 'nap_acute_exhaustion':('Acute War Exhaustion','army_org_factor = -0.08 political_power_factor = -0.12','A prolonged campaign has depleted public confidence and army cohesion.'),
 'nap_legitimacy_crisis':('Legitimacy Crisis','stability_factor = -0.05 political_power_factor = -0.08','The government struggles to obtain compliance with its decisions.'),
 'nap_secure_authority':('Secure Authority','political_power_factor = 0.04','A broadly accepted administration can act more effectively.'),
 'nap_debt_crisis':('Burden of State Debt','political_power_factor = -0.08','Debt service consumes fiscal capacity. Debt of 60 or more costs treasury each month.'),
 'nap_extended_supply_lines':('Extended Supply Lines','supply_consumption_factor = 0.08 army_morale_factor = -0.04','Foreign occupations stretch magazines, roads and transport.'),
 'nap_battle_confidence':('Confidence in the Army','army_morale_factor = 0.04','Recent victories and institutional competence improve confidence.'),
 'nap_shaken_army':('Shaken Army','army_morale_factor = -0.04','Military reverses have weakened confidence in the army.'),
 'nap_staff_institutions':('Professional Staff Institutions','planning_speed = 0.04','A sustained reform effort has improved staff work.'),
 'nap_funded_magazines':('Funded Forward Magazines','supply_consumption_factor = -0.06','Temporary, paid supply preparations ease a campaign.'),
 'nap_army_rotation':('Rotating the Field Army','army_attack_factor = -0.04 army_morale_factor = 0.04','Restoring exhausted formations reduces immediate operational tempo.')
}


def change(name, value):
    return f'add_to_variable = {{ nap_{name} = {value} }}'


def constraints(action):
    _,_,_,_,minimum,maximum,_,extra,_,_ = action
    result = ['has_country_flag = nap_era_initialized', 'nap_era_country = yes']
    result += [f'NOT = {{ check_variable = {{ nap_{name} < {value} }} }}' for name,value in minimum.items()]
    result += [f'NOT = {{ check_variable = {{ nap_{name} > {value} }} }}' for name,value in maximum.items()]
    if extra:
        result.append(extra)
    return ' '.join(result)


def apply_action(state, action, *, at_war=False, revolutionary_france=False):
    """Reference model for resource bounds; not a HOI4 execution emulator."""
    _,_,_,_,minimum,maximum,deltas,extra,_,_ = action
    if any(state.get(k,0) < v for k,v in minimum.items()) or any(state.get(k,0) > v for k,v in maximum.items()):
        return None
    if 'has_war = yes' in extra and not at_war:
        return None
    if 'has_war = no' in extra and at_war:
        return None
    if 'french_revolutionary_path' in extra and not revolutionary_france:
        return None
    result = state.copy()
    for key,value in deltas.items():
        result[key] = max(0, min(100, result[key] + value))
    return result


def monthly_model(state, *, at_war, foreign_occupation):
    result = state.copy()
    def add(key, value):
        result[key] += value
    add('treasury', 1 if at_war else 3)
    add('war_exhaustion', 3 if at_war else -4)
    add('supply_pressure', 2 if at_war and foreign_occupation else -4)
    if at_war and foreign_occupation:
        add('war_exhaustion', 1)
    if result['debt'] >= 60:
        add('treasury', -2)
    if result['war_exhaustion'] >= 80:
        add('legitimacy', -1)
    if not at_war and result['war_exhaustion'] < 40 and result['legitimacy'] < 55:
        add('legitimacy', 1)
    return {key:max(0,min(100,value)) for key,value in result.items()}


def build(root):
    output = {}
    trigger = 'nap_era_country = { OR = { ' + ' '.join(f'original_tag = {tag}' for tag in TAGS) + ' } }\n'
    output['common/scripted_triggers/nap_era.txt'] = trigger
    clamp = '\n'.join(f'clamp_variable = {{ var = nap_{key} min = 0 max = 100 }}' for key in DEFAULTS)
    init = '\n'.join(f'set_variable = {{ nap_{key} = {value} }}' for key,value in DEFAULTS.items())
    effects = f'''# Country scope throughout. Values represent abstract capacity, not historical currency.
nap_era_initialize = {{
 if = {{
  limit = {{ nap_era_country = yes NOT = {{ has_country_flag = nap_era_initialized }} }}
  set_country_flag = nap_era_initialized
  {init}
  if = {{ limit = {{ tag = FRA }} set_variable = {{ nap_treasury = 20 }} set_variable = {{ nap_debt = 65 }} set_variable = {{ nap_legitimacy = 35 }} set_variable = {{ nap_fervor = 20 }} }}
 }}
}}
nap_era_clamp = {{ {clamp} }}
nap_era_monthly = {{
 nap_era_initialize = yes
 if = {{ limit = {{ has_country_flag = nap_era_initialized }}
  if = {{ limit = {{ has_war = yes }} {change('treasury',1)} {change('war_exhaustion',3)} }}
  else = {{ {change('treasury',3)} {change('war_exhaustion',-4)} }}
  if = {{ limit = {{ has_war = yes any_controlled_state = {{ NOT = {{ is_owned_by = ROOT }} NOT = {{ is_core_of = ROOT }} }} }}
   {change('supply_pressure',2)} {change('war_exhaustion',1)}
  }} else = {{ {change('supply_pressure',-4)} }}
  if = {{ limit = {{ check_variable = {{ nap_debt > 59 }} }} {change('treasury',-2)} }}
  if = {{ limit = {{ check_variable = {{ nap_war_exhaustion > 79 }} }} {change('legitimacy',-1)} }}
  if = {{ limit = {{ has_war = no check_variable = {{ nap_war_exhaustion < 40 }} check_variable = {{ nap_legitimacy < 55 }} }} {change('legitimacy',1)} }}
  nap_era_clamp = yes
  nap_era_refresh = yes
 }}
}}
nap_era_refresh = {{
 if = {{ limit = {{ check_variable = {{ nap_war_exhaustion > 79 }} }} remove_ideas = nap_war_weariness add_ideas = nap_acute_exhaustion }}
 else_if = {{ limit = {{ check_variable = {{ nap_war_exhaustion > 49 }} }} remove_ideas = nap_acute_exhaustion add_ideas = nap_war_weariness }}
 else = {{ remove_ideas = nap_war_weariness remove_ideas = nap_acute_exhaustion }}
'''
    for key, threshold, idea in [('legitimacy',29,'nap_legitimacy_crisis'),('legitimacy',69,'nap_secure_authority'),('debt',59,'nap_debt_crisis'),('supply_pressure',39,'nap_extended_supply_lines'),('army_prestige',69,'nap_battle_confidence'),('army_prestige',29,'nap_shaken_army'),('reform',59,'nap_staff_institutions')]:
        condition = f'nap_{key} < {threshold+1}' if idea in ('nap_legitimacy_crisis','nap_shaken_army') else f'nap_{key} > {threshold}'
        effects += f' if = {{ limit = {{ check_variable = {{ {condition} }} }} add_ideas = {idea} }} else = {{ remove_ideas = {idea} }}\n'
    effects += '}\n'
    decisions = ['nap_era_management = {']
    loc = ['\ufeffl_english:', ' nap_era_management:0 "State and Army Administration"', ' nap_era_management_desc:0 "Treasury: [?nap_treasury|0] / Debt: [?nap_debt|0]\\nLegitimacy: [?nap_legitimacy|0] / Fervor: [?nap_fervor|0]\\nWar exhaustion: [?nap_war_exhaustion|0] / Army prestige: [?nap_army_prestige|0]\\nReform: [?nap_reform|0] / Supply pressure: [?nap_supply_pressure|0]\\nAll meters run from 0 to 100. These are game abstractions, not historical measurements."']
    for key in DEFAULTS:
        loc.append(f' nap_{key}:0 "{key.replace("_"," ").title()}"')
    for action in ACTIONS:
        key,title,cost,cooldown,_,_,deltas,_,extra,desc = action
        guard = constraints(action)
        reward = ' '.join(change(name,value) for name,value in deltas.items())
        effects += f'nap_era_action_{key} = {{ if = {{ limit = {{ {guard} }} {reward} {extra} nap_era_clamp = yes nap_era_refresh = yes }} }}\n'
        decisions.append(f' nap_era_{key} = {{ icon = generic_prepare_civil_war cost = {cost} days_re_enable = {cooldown} visible = {{ nap_era_country = yes }} available = {{ {guard} }} complete_effect = {{ nap_era_action_{key} = yes }} ai_will_do = {{ factor = 1 }} }}')
        loc += [f' nap_era_{key}:0 "{title}"', f' nap_era_{key}_desc:0 "{desc}"']
    decisions.append('}')
    output['common/scripted_effects/nap_era.txt'] = effects
    output['common/decisions/nap_era.txt'] = '\n'.join(decisions) + '\n'
    output['common/decisions/categories/nap_era.txt'] = 'nap_era_management = { icon = generic_political_discourse allowed = { always = yes } visible = { nap_era_country = yes has_country_flag = nap_era_initialized } }\n'
    output['common/on_actions/nap_era.txt'] = '''# on_monthly is already country-scoped. Do not nest every_country here.
on_actions = {
 on_startup = { effect = { every_country = { limit = { nap_era_country = yes } nap_era_initialize = yes nap_era_refresh = yes } } }
 on_monthly = { effect = { if = { limit = { nap_era_country = yes } nap_era_monthly = yes } } }
 on_army_leader_won_combat = { effect = { FROM = { if = { limit = { nap_era_country = yes } nap_era_initialize = yes add_to_variable = { nap_army_prestige = 0.05 } nap_era_clamp = yes } } } }
 on_army_leader_lost_combat = { effect = { FROM = { if = { limit = { nap_era_country = yes } nap_era_initialize = yes add_to_variable = { nap_army_prestige = -0.10 } nap_era_clamp = yes } } } }
}
'''
    ideas = ['ideas = { country = {']
    for key,(name,modifier,desc) in IDEAS.items():
        ideas.append(f' {key} = {{ picture = generic_morale_bonus allowed = {{ always = yes }} removal_cost = -1 modifier = {{ {modifier} }} }}')
        loc += [f' {key}:0 "{name}"', f' {key}_desc:0 "{desc}"']
    ideas.append('} }')
    output['common/ideas/nap_era.txt'] = '\n'.join(ideas) + '\n'
    output['localisation/english/nap_era_l_english.yml'] = '\n'.join(loc) + '\n'
    output['docs/era-mechanics.md'] = '''# Reusable era mechanics (Milestone 6 slice)

Eight bounded meters: treasury, debt, legitimacy, fervor, war exhaustion, national army prestige, administrative/military reform and foreign-campaign supply pressure. They are explicitly game abstractions.

Initialization is idempotent. The monthly hook runs once per eligible country, without a nested world scan. Occupation checks only run during war. Peace restores capacity and reduces exhaustion; high debt drains fiscal capacity; long foreign campaigns increase pressure.

Twelve decisions have finite political-power costs, resource checks and 90-365 day cooldowns. Resource predicates are repeated at effect execution. Levee is restricted to revolutionary France at war. No decision deletes units, creates territorial cores or changes faction membership.

Eleven national spirits represent threshold effects and two temporary paid policies. Severe and ordinary exhaustion are mutually exclusive. Values clamp to 0-100 after pulses and decisions. Battle hooks affect national army prestige, not individual-general prestige.

This is not all of Milestone 6: individual leader reputation, nationalism, state-specific occupation politics, client management and a fuller economic model remain separate work. Unit tests exercise the reference resource model and generated syntax; they are not HOI4 runtime tests. Balance numbers are provisional.
'''
    output['docs/era-actions.json'] = json.dumps([{'id':a[0],'pp_cost':a[2],'cooldown_days':a[3],'minimum':a[4],'maximum':a[5],'deltas':a[6]} for a in ACTIONS],indent=2)+'\n'
    return output
