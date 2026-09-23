"""Compile the 450-focus French tree and 84 policy dilemmas.

Hand-authored chapter names and subjects live in france_catalogue.py. This
compiler defines graph contracts, route guards, bounded rewards and localisation.
"""
import json
from collections import Counter
from pdx import Entry, parse, dumps, walk
from build_10_era import change
from france_catalogue import CHAPTERS
from france_legacy import patch_legacy, leader, apply_focus_date_gates

ROUTES = {
 'common': 'tag = FRA',
 'constitutional': 'tag = FRA has_country_flag = french_constitutional_path NOT = { has_country_flag = french_royalist_path } NOT = { has_country_flag = french_bonapartist_path }',
 'royalist': 'tag = FRA has_country_flag = french_royalist_path NOT = { has_country_flag = french_constitutional_path } NOT = { has_country_flag = french_bonapartist_path }',
 'republican': 'tag = FRA has_country_flag = french_revolutionary_path NOT = { has_country_flag = french_constitutional_path } NOT = { has_country_flag = french_royalist_path } NOT = { has_country_flag = french_bonapartist_path }',
 'directory': 'nap_fra_route_republican = yes has_country_flag = directory_active',
 'consular': 'tag = FRA has_country_flag = french_bonapartist_path OR = { has_country_flag = consulate_established has_country_flag = empire_of_the_french has_country_flag = hundred_days } NOT = { has_country_flag = bourbon_restoration }',
 'imperial': 'tag = FRA has_country_flag = french_bonapartist_path OR = { has_country_flag = empire_of_the_french has_country_flag = hundred_days } NOT = { has_country_flag = bourbon_restoration }',
 'campaign': 'tag = FRA OR = { nap_fra_route_republican = yes nap_fra_route_consular = yes }',
 'late_imperial': 'tag = FRA OR = { nap_fra_route_imperial = yes has_country_flag = napoleon_on_elba has_country_flag = bourbon_restoration }',
}
PARENTS = {0:[],1:[[0]],2:[[0]],3:[[1]],4:[[2]],5:[[3,4]],6:[[5]],7:[[5]],8:[[6]],9:[[7]],10:[[8],[9]],11:[[10]],12:[[10]],13:[[11,12]],14:[[13]]}
EXCLUSIVE = {1:2,2:1,11:12,12:11}
XY = [(8,0),(4,1),(12,1),(4,2),(12,2),(8,3),(4,4),(12,4),(4,5),(12,5),(8,6),(4,7),(12,7),(8,8),(8,9)]
COSTS = [2,3,3,4,4,2,3,3,5,4,2,5,5,3,7]
DOMAINS = {
 'politics': ('political_power_factor = 0.01','GFX_goal_generic_political_pressure', {'legitimacy':1},'add_political_power = 10'),
 'finance': ('political_power_factor = 0.01','GFX_goal_generic_construct_civ_factory', {'treasury':3,'debt':-1},''),
 'administration': ('stability_factor = 0.01','GFX_goal_generic_political_pressure', {'reform':2,'legitimacy':1},''),
 'science': ('research_speed_factor = 0.01','GFX_goal_generic_scientific_exchange', {'reform':2},'add_political_power = 5'),
 'infantry': ('army_org_factor = 0.01','GFX_goal_generic_army_doctrines', {'army_prestige':1},'army_experience = 4'),
 'cavalry': ('army_speed_factor = 0.01','GFX_goal_generic_army_doctrines', {'army_prestige':1},'army_experience = 4'),
 'artillery': ('army_attack_factor = 0.01','GFX_goal_generic_army_artillery', {'supply_pressure':-1},'army_experience = 4'),
 'navy': ('navy_org_factor = 0.01','GFX_goal_generic_navy_battleship', {'treasury':1},'navy_experience = 5'),
 'diplomacy': ('political_power_factor = 0.01','GFX_goal_generic_improve_relations', {'legitimacy':1},'add_political_power = 12'),
 'royal': ('stability_factor = 0.01','GFX_goal_generic_neutrality_focus', {'legitimacy':2,'fervor':-1},'add_political_power = 5'),
 'republic': ('war_support_factor = 0.01','GFX_goal_generic_political_pressure', {'fervor':2,'legitimacy':1},''),
 'military': ('army_morale_factor = 0.01','GFX_goal_generic_army_doctrines', {'army_prestige':1,'supply_pressure':-1},'army_experience = 4'),
}
TECH_CATEGORIES = {'infantry':'category_napoleonic_infantry_tech','cavalry':'category_napoleonic_cavalry_tech','artillery':'category_napoleonic_artillery_tech','navy':'category_napoleonic_naval_tech','science':'category_napoleonic_support_tech'}


def fid(chapter, index):
    return f"FRA_nap_{chapter['key']}_{index:02d}"


def event_id(chapter_index, slot):
    return f'nap_fra_development.{1000+chapter_index*10+slot}'


def policy_delta(domain, generous):
    primary = {'politics':'legitimacy','finance':'treasury','administration':'reform','science':'reform','infantry':'army_prestige','cavalry':'army_prestige','artillery':'supply_pressure','navy':'army_prestige','diplomacy':'legitimacy','royal':'legitimacy','republic':'fervor','military':'army_prestige'}[domain]
    value = (5 if generous else 2) * (-1 if primary=='supply_pressure' else 1)
    return primary, value


def build(root):
    outputs = {}
    focuses, loc, effects, events, index = [], ['\ufeffl_english:'], [], ['add_namespace = nap_fra_development'], []
    ideas = ['ideas = { country = {']
    triggers = [f'nap_fra_route_{key} = {{ {value} }}' for key,value in ROUTES.items()]
    for ci, chapter in enumerate(CHAPTERS):
        key, domain, route = chapter['key'], chapter['domain'], chapter['route']
        guard = f'nap_fra_route_{route} = yes'
        modifier, icon, deltas, plain_effect = DOMAINS[domain]
        for tier, title, mods in [('programme',chapter['title']+' Programme',modifier),('settlement',chapter['title'],chapter['modifier'])]:
            idea = f'nap_fra_{key}_{tier}'
            ideas.append(f'{idea} = {{ picture = generic_morale_bonus allowed = {{ original_tag = FRA }} removal_cost = -1 modifier = {{ {mods} }} }}')
            loc += [f' {idea}:0 "{title}"', f' {idea}_desc:0 "The institutional effects of the {chapter["title"].lower()} programme. These balance values remain provisional."']
        for ni,name in enumerate(chapter['names']):
            identifier = fid(chapter,ni)
            x,y = XY[ni]
            x += (ci % 4)*24
            y += 18+(ci//4)*12
            cost = 10 if ni==14 and route in ('imperial','late_imperial','constitutional') else COSTS[ni]
            prerequisites = [[chapter['anchor']]] if ni==0 else [[fid(chapter,p) for p in group] for group in PARENTS[ni]]
            prerequisite_text = '\n'.join('prerequisite = { '+' '.join('focus = '+p for p in group)+' }' for group in prerequisites)
            exclusive = [fid(chapter,EXCLUSIVE[ni])] if ni in EXCLUSIVE else []
            if ni==0 and key in ('girondins','jacobins'):
                other = next(c for c in CHAPTERS if c['key']==('jacobins' if key=='girondins' else 'girondins'))
                exclusive.append(fid(other,0))
            exclusive_text = 'mutually_exclusive = { '+' '.join('focus = '+p for p in exclusive)+' }' if exclusive else ''
            reward = ['nap_era_initialize = yes']
            if ni in (5,10,14):
                slot = {5:1,10:2,14:3}[ni]
                reward.append(f'country_event = {{ id = {event_id(ci,slot)} hours = 6 }}')
            else:
                reward += [change(k,v) for k,v in deltas.items()]
                if plain_effect:
                    reward.append(plain_effect)
            if ni in (1,2,11,12):
                reward.append(f'set_country_flag = {identifier}_policy')
                reward.append(change('reform' if ni in (1,11) else 'legitimacy',2))
            if ni==0 and key in ('girondins','jacobins'):
                reward.append(f'set_country_flag = nap_fra_{key}_programme')
            if ni==8 and domain in TECH_CATEGORIES:
                reward.append(f'add_tech_bonus = {{ name = {identifier}_bonus bonus = 0.25 uses = 1 category = {TECH_CATEGORIES[domain]} }}')
                loc.append(f' {identifier}_bonus:0 "{name}"')
            if ni==13:
                reward.append(f'add_timed_idea = {{ idea = nap_fra_{key}_programme days = 180 }}')
            if ni==14:
                reward += [f'add_ideas = nap_fra_{key}_settlement', f'set_country_flag = nap_fra_{key}_complete']
            reward += ['nap_era_clamp = yes','nap_era_refresh = yes']
            effects.append(f'nap_reward_{identifier} = {{ if = {{ limit = {{ {guard} NOT = {{ has_country_flag = {identifier}_paid }} }} set_country_flag = {identifier}_paid '+' '.join(reward)+' } }')
            focuses.append(f'''shared_focus = {{
 id = {identifier}
 icon = {icon}
 x = {x} y = {y}
 cost = {cost}
 {prerequisite_text}
 {exclusive_text}
 available = {{ {guard} }}
 cancel_if_invalid = yes
 ai_will_do = {{ factor = 1 }}
 completion_reward = {{ nap_reward_{identifier} = yes }}
}}''')
            purpose = f'{name} advances the {chapter["title"].lower()} programme. {chapter["dilemma"]}'
            if ni in EXCLUSIVE:
                purpose += ' This is an exclusive policy choice; its alternative cannot also be taken.'
            if ni in (5,10,14):
                purpose += ' Completing this focus opens a policy dilemma with a funded programme and a lower-cost alternative.'
            if ni==14:
                purpose += ' The chapter concludes with a persistent institutional national spirit.'
            loc += [f' {identifier}:0 "{name}"', f' {identifier}_desc:0 "{purpose}"']
            index.append(dict(id=identifier,title=name,chapter=chapter['title'],route=route,days=cost*7,x=x,y=y,prerequisites=prerequisites,exclusive=exclusive))
        for slot, title in enumerate(chapter['questions'],1):
            eid = event_id(ci,slot)
            token = f'nap_fra_event_{ci}_{slot}_resolved'
            money = 8+slot*4
            var, gain = policy_delta(domain,True)
            _, small = policy_delta(domain,False)
            funded = f'NOT = {{ check_variable = {{ nap_treasury < {money} }} }}'
            valid = f'{guard} NOT = {{ has_country_flag = {token} }}'
            events.append(f'''country_event = {{
 id = {eid}
 title = {eid}.t
 desc = {eid}.d
 picture = GFX_report_event_generic_assembly
 is_triggered_only = yes
 fire_only_once = yes
 immediate = {{ if = {{ limit = {{ tag = FRA }} nap_era_initialize = yes }} }}
 option = {{
  name = {eid}.a
  trigger = {{ {valid} {funded} }}
  ai_chance = {{ factor = 60 }}
  if = {{ limit = {{ {valid} {funded} }}
   set_country_flag = {token}
   {change('treasury',-money)} {change(var,gain)} {change('reform',2)}
   nap_era_clamp = yes nap_era_refresh = yes
  }}
 }}
 option = {{
  name = {eid}.b
  trigger = {{ {valid} }}
  ai_chance = {{ factor = 40 }}
  if = {{ limit = {{ {valid} }}
   set_country_flag = {token}
   {change(var,small)} {change('legitimacy',-1)}
   nap_era_clamp = yes nap_era_refresh = yes
  }}
 }}
 option = {{ name = nap_fra_superseded trigger = {{ NOT = {{ {valid} }} }} ai_chance = {{ factor = 100 }} }}
}}''')
            sign = '+' if gain>0 else ''
            loc += [f' {eid}.t:0 "{title}"', f' {eid}.d:0 "{chapter["dilemma"]} The government must decide whether to fund the full programme or accept a more limited settlement. Funding costs {money} treasury, changes {var.replace("_"," ")} by {sign}{gain}, and adds 2 reform. The limited settlement produces a smaller change and costs 1 legitimacy."',f' {eid}.a:0 "Fund the {chapter["title"].lower()} programme."',f' {eid}.b:0 "Accept a limited settlement for now."']
    capstone = 'FRA_nap_national_settlement'
    targets = ' '.join('focus = '+fid(c,14) for c in CHAPTERS)
    focuses.append(f'''shared_focus = {{ id = {capstone} icon = GFX_goal_generic_political_pressure x = 96 y = 20 cost = 2 prerequisite = {{ {targets} }} available = {{ tag = FRA }} completion_reward = {{ if = {{ limit = {{ tag = FRA NOT = {{ has_country_flag = nap_fra_national_settlement_paid }} }} set_country_flag = nap_fra_national_settlement_paid nap_era_initialize = yes {change('legitimacy',5)} add_political_power = 25 nap_era_clamp = yes nap_era_refresh = yes }} }} }}''')
    loc += [f' {capstone}:0 "Record the National Settlement"',f' {capstone}_desc:0 "Record the first completed programme as a durable part of the state. This is a one-time administrative recognition, not the end of the campaign or a requirement to finish every incompatible route."',' nap_fra_superseded:0 "The political situation has changed; set this proposal aside."',' nap_fra_legacy_superseded:0 "This question is already settled or no longer applies."']
    ideas.append('} }')
    outputs['common/national_focus/nap_france_expansion.txt'] = '\n\n'.join(focuses)+'\n'
    outputs['common/scripted_triggers/nap_france_routes.txt'] = '\n'.join(triggers)+'\n'
    outputs['common/scripted_effects/nap_france_rewards.txt'] = '\n'.join(effects)+'\n'
    outputs['common/ideas/nap_france_programmes.txt'] = '\n'.join(ideas)+'\n'
    outputs['events/05_french_development.txt'] = '\n\n'.join(events)+'\n'
    outputs['localisation/english/nap_french_development_l_english.yml'] = '\n'.join(loc)+'\n'
    legacy = apply_focus_date_gates(parse((root/'content/legacy/FRA.txt').read_text(encoding='utf-8-sig')))
    tree = next(e for e in legacy if e.key=='focus_tree')
    for e in tree.children('focus'):
        if e.scalar('id')=='FRA_constitutional_monarchy':
            e.children('completion_reward')[0].value += leader('Louis XVI','conservatism')
        if e.scalar('id')=='FRA_restore_ancien_regime':
            e.children('completion_reward')[0].value += leader('Louis XVI','despotism','indecisive_leader')
        if e.scalar('id')=='FRA_reign_of_terror_focus':
            e.value.append(Entry('available',parse('NOT = { has_country_flag = nap_fra_girondins_programme }')))
        if e.scalar('id')=='FRA_sister_republics':
            for p in e.children('prerequisite'):
                if p.scalar('focus')=='FRA_reign_of_terror_focus':
                    p.value.append(Entry('focus','FRA_nap_girondins_14'))
    for chapter in CHAPTERS:
        tree.value.append(Entry('shared_focus',fid(chapter,0)))
    tree.value.append(Entry('shared_focus',capstone))
    outputs['common/national_focus/FRA.txt'] = '# Generated from retained legacy tree and the French chapter catalogue. Historical dates are minimum focus gates under A01.\n'+dumps(legacy)
    outputs.update(patch_legacy(root))
    outputs['docs/france-focus-index.json'] = json.dumps(index,indent=2)+'\n'
    durations = dict(sorted(Counter(x['days'] for x in index).items()))
    outputs['docs/france-expansion.md'] = f'''# French expansion: Milestone 3 implementation slice

29 original focuses are retained. 28 authored policy chapters add 420 focuses, and one cross-route administrative capstone brings the tree to **450**. There are **84 new policy events** and 56 chapter-related spirits (28 temporary programmes, 28 persistent settlements).

The new chapter durations in days are: {durations}. A focus is not a promise that every route can take it: each chapter contains exclusive policies, and Girondin/Jacobin programmes are mutually exclusive. The original four political routes remain the main paths.

Each chapter has two exclusive forks, parallel preparation work, three event dilemmas and a concluding institution. Events distinguish a funded policy from a lower-cost settlement. Resource checks are repeated on execution. Rewards and event choices have completion flags to prevent repeated payouts. No chapter grants unrestricted territorial cores, seizes a foreign state or invents a new political route.

The new focuses are grouped in four columns of chapter panels below the retained tree. Coordinates are statically unique; actual rendering, line routing and usability at this scale must be checked inside HOI4.

The existing French event files are retained under content/legacy and normalized through a parser for route/duplicate guards. Under A01, historical dates are minimum gates on the relevant legacy focuses; event progression is route/state-driven. The Directory follows the Thermidor transition so a republic that restrains the Terror is not stranded before the Consulate. Current rulers are not accidentally retired by an event ostensibly about a deposed king. Collective governments and restoration leaders receive explicit legacy leader creation where necessary.

This is not a declaration that all of Milestone 3 is finished. Deep scripted campaigns, state-level Vendee warfare, a complete modern-character conversion, active client-state management, final coring policy, full blockade enforcement and engine-tested balance remain further work. A01 chronology is implemented here; outcome-aware bounded peace is implemented by the stacked A03 pass.

The focus index JSON records IDs, titles, routes, durations, coordinates, prerequisites and exclusions. Names and event subjects are authored in france_catalogue.py; engine repetition is generated, not hand-copied.
'''
    return outputs
