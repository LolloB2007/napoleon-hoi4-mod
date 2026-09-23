"""Decision-driven French campaign mechanics.

This layer turns the major French historical arcs into ongoing decisions and
bounded variables. Existing narrative events remain authoritative for leader and
government transitions, but key transitions are invoked by decisions rather
than focus-completion timers or calendar-driven MTTH chains.
"""
from __future__ import annotations
import json
from pdx import Entry,parse,dumps,walk
from build_10_era import change

VARS = {
 'vendee_unrest':15,
 'assignat_inflation':5,
 'faction_tension':20,
 'girondin_influence':40,
 'jacobin_influence':40,
 'napoleon_prestige':10,
 'continental_pressure':0,
 'peninsular_resistance':0,
 'russian_supply':0,
 'russian_cohesion':100,
}
CONTINENTAL_TARGETS = [
 ('RUS','Russia'),('PRU','Prussia'),('HAB','Austria'),('SPR','Spain'),
 ('POR','Portugal'),('NET','the Netherlands'),('DEN','Denmark'),('SWE','Sweden'),
]

CATEGORIES = {
 'nap_fra_revolutionary_crisis':('Revolutionary Government','Manage institutions, factional pressure, the Vendée, emergency finance and the Terror.'),
 'nap_fra_napoleon_rise':("Bonaparte's Ascent",'Turn military prestige into political authority through Italy, Egypt, Brumaire, the Consulate and Empire.'),
 'nap_fra_continental_system':('The Continental System','Enforce or relax the blockade and pressure European states while Britain adapts.'),
 'nap_fra_peninsular_war':('The Peninsular War','Manage occupation, guerrilla resistance, supply and the political cost of Iberian intervention.'),
 'nap_fra_russian_campaign':('The Russian Campaign','Prepare magazines and remounts, preserve cohesion and choose between settlement, retreat and disaster.'),
 'nap_fra_restoration_cycle':('Collapse, Restoration and the Hundred Days','Control abdication, restoration, the return from Elba and the final European settlement.'),
 'nap_continental_foreign':('Continental Customs','Comply with French customs enforcement or tolerate smuggling and British trade.'),
}

IDEAS = {
 'nap_fra_vendee_revolt':('The Vendée in Revolt','stability_factor = -0.06 political_power_factor = -0.05 supply_consumption_factor = 0.04','Armed and political resistance in western France consumes troops, supplies and administrative attention.'),
 'nap_fra_assignat_crisis':('Assignat Inflation','stability_factor = -0.04 political_power_factor = -0.06','Emergency paper finance is undermining confidence and complicating government finance.'),
 'nap_fra_committee_public_safety':('Committee of Public Safety','war_support_factor = 0.05 political_power_factor = 0.03 stability_factor = -0.03','Emergency government concentrates authority at the cost of institutional restraint.'),
 'nap_fra_consular_machine':('The Consular Machine','political_power_factor = 0.04 stability_factor = 0.03','The Consulate has concentrated administration, finance and political decision-making.'),
 'nap_fra_marshals_empire':('Marshals of the Empire','army_morale_factor = 0.04 planning_speed = 0.04','A prestigious senior command cadre binds military advancement to the imperial state.'),
 'nap_continental_compliance':('Continental Customs Enforcement','trade_opinion_factor = -0.10 political_power_factor = -0.02','French customs pressure restricts commerce with Britain and creates domestic enforcement costs.'),
 'nap_british_continental_pressure':('Continental Trade Pressure','trade_opinion_factor = -0.15 political_power_factor = -0.03','A broad continental customs regime is obstructing British access to European markets.'),
 'nap_fra_peninsular_guerrilla_war':('The Spanish Ulcer','supply_consumption_factor = 0.10 army_morale_factor = -0.03 war_support_factor = -0.03','Guerrilla warfare and dispersed occupation duties consume supply and erode the political value of battlefield victories.'),
 'nap_fra_russian_logistics':('Russian Campaign Logistics','supply_consumption_factor = 0.14 army_morale_factor = -0.05','Distance, forage and transport losses are consuming the campaign faster than ordinary battlefield expenditure.'),
 'nap_fra_russian_prepared':('Prepared Eastern Magazines','supply_consumption_factor = -0.06 planning_speed = 0.04','Forward magazines, wagons and remounts give the army a temporary logistical reserve for the eastern campaign.'),
 'nap_fra_hundred_days_mobilization':('Hundred Days Mobilization','army_morale_factor = 0.05 army_attack_factor = 0.03 stability_factor = -0.03','Veterans and loyal formations have rallied quickly, but the restored imperial state remains politically fragile.'),
 'nap_fra_restoration_charter':('Charter of the Restoration','stability_factor = 0.04 political_power_factor = 0.03','The restored monarchy has accepted a bounded constitutional settlement rather than trying to erase the Revolution wholesale.'),
 'nap_fra_postwar_exhaustion':('Postwar Exhaustion','war_support_factor = -0.06 political_power_factor = -0.03','France must absorb demobilisation, debt, veterans and political disappointment after prolonged war.'),
}

DECISION_META=[]


def fvar(name): return 'nap_fra_'+name
def vadd(name,value): return f'add_to_variable = {{ {fvar(name)} = {value} }}'
def vset(name,value): return f'set_variable = {{ {fvar(name)} = {value} }}'
def at_least(name,value): return f'NOT = {{ check_variable = {{ {fvar(name)} < {value} }} }}'
def at_most(name,value): return f'NOT = {{ check_variable = {{ {fvar(name)} > {value} }} }}'


def add_decision(sections,loc,category,key,title,desc,guard,effect,cost=35,cooldown=None,once=False,visible=None,ai=1):
    visible = visible or guard
    bits=[
      f'icon = generic_political_discourse',
      f'cost = {cost}',
      f'visible = {{ {visible} }}',
      f'available = {{ {guard} }}',
      f'complete_effect = {{ {effect} = yes }}',
      f'ai_will_do = {{ factor = {ai} }}',
    ]
    if cooldown: bits.append(f'days_re_enable = {cooldown}')
    if once: bits.append('fire_only_once = yes')
    sections[category].append(f'{key} = {{ '+' '.join(bits)+' }')
    loc += [f' {key}:0 "{title}"',f' {key}_desc:0 "{desc}"']
    DECISION_META.append(dict(id=key,category=category,title=title,repeatable=not once))


def add_effect(effects,key,guard,body,france=True):
    scope = 'tag = FRA ' if france else ''
    tail = ' nap_fra_decision_clamp = yes nap_fra_decision_refresh = yes' if france else ''
    effects.append(f'{key} = {{ if = {{ limit = {{ {scope}{guard} }} {body}{tail} }} }}')


def build(root):
    global DECISION_META
    DECISION_META=[]
    sections={key:[] for key in CATEGORIES}
    loc=['\ufeffl_english:']
    effects=[]

    for key,(title,desc) in CATEGORIES.items():
        loc += [f' {key}:0 "{title}"',f' {key}_desc:0 "{desc}"']

    ideas=['ideas = { country = {']
    for key,(title,mods,desc) in IDEAS.items():
        ideas.append(f'{key} = {{ picture = generic_morale_bonus allowed = {{ always = yes }} removal_cost = -1 modifier = {{ {mods} }} }}')
        loc += [f' {key}:0 "{title}"',f' {key}_desc:0 "{desc}"']
    ideas.append('} }')

    init=' '.join(vset(k,v) for k,v in VARS.items())
    effects.append(f'''nap_fra_decision_initialize = {{
 if = {{ limit = {{ tag = FRA NOT = {{ has_country_flag = nap_fra_decision_system_initialized }} }}
  nap_era_initialize = yes
  set_country_flag = nap_fra_decision_system_initialized
  {init}
 }}
}}''')
    clamp=[]
    for key in VARS:
        clamp += [
          f'if = {{ limit = {{ check_variable = {{ {fvar(key)} > 100 }} }} {vset(key,100)} }}',
          f'if = {{ limit = {{ check_variable = {{ {fvar(key)} < 0 }} }} {vset(key,0)} }}',
        ]
    effects.append('nap_fra_decision_clamp = { '+' '.join(clamp)+' }')
    effects.append('''nap_fra_decision_refresh = {
 nap_fra_decision_clamp = yes
 if = { limit = { check_variable = { nap_fra_vendee_unrest > 59 } NOT = { has_idea = nap_fra_vendee_revolt } } add_ideas = nap_fra_vendee_revolt }
 if = { limit = { NOT = { check_variable = { nap_fra_vendee_unrest > 39 } } has_idea = nap_fra_vendee_revolt } remove_ideas = nap_fra_vendee_revolt }
 if = { limit = { check_variable = { nap_fra_assignat_inflation > 59 } NOT = { has_idea = nap_fra_assignat_crisis } } add_ideas = nap_fra_assignat_crisis }
 if = { limit = { NOT = { check_variable = { nap_fra_assignat_inflation > 39 } } has_idea = nap_fra_assignat_crisis } remove_ideas = nap_fra_assignat_crisis }
 if = { limit = { has_country_flag = nap_legacy_french_revolution_10_settled NOT = { has_country_flag = reign_of_terror_active } has_idea = nap_fra_committee_public_safety } remove_ideas = nap_fra_committee_public_safety }
 if = { limit = { has_global_flag = continental_system_active check_variable = { nap_fra_continental_pressure > 39 } ENG = { exists = yes } } ENG = { if = { limit = { NOT = { has_idea = nap_british_continental_pressure } } add_ideas = nap_british_continental_pressure } } }
 if = { limit = { OR = { NOT = { has_global_flag = continental_system_active } NOT = { check_variable = { nap_fra_continental_pressure > 24 } } } ENG = { exists = yes } } ENG = { if = { limit = { has_idea = nap_british_continental_pressure } remove_ideas = nap_british_continental_pressure } } }
 if = { limit = { has_country_flag = nap_fra_peninsular_active NOT = { OR = { has_war_with = SPR has_war_with = POR } } } clr_country_flag = nap_fra_peninsular_active remove_ideas = nap_fra_peninsular_guerrilla_war set_country_flag = nap_fra_peninsular_resolved add_stability = 0.02 }
 if = { limit = { has_country_flag = russian_campaign_active NOT = { has_war_with = RUS } } clr_country_flag = russian_campaign_active remove_ideas = nap_fra_russian_logistics remove_ideas = nap_fra_russian_prepared set_country_flag = nap_fra_russian_campaign_resolved }
 if = { limit = { NOT = { has_country_flag = hundred_days } has_idea = nap_fra_hundred_days_mobilization } remove_ideas = nap_fra_hundred_days_mobilization }
}''')

    effects.append(f'''nap_fra_decision_monthly = {{
 if = {{ limit = {{ tag = FRA }}
  nap_fra_decision_initialize = yes
  if = {{ limit = {{ has_country_flag = french_revolutionary_path has_war = yes }} {vadd('vendee_unrest',2)} {vadd('faction_tension',1)} }}
  if = {{ limit = {{ has_country_flag = nap_fra_assignats_active }} {vadd('assignat_inflation',3)} }}
  if = {{ limit = {{ has_country_flag = reign_of_terror_active }} {vadd('faction_tension',4)} {change('legitimacy',-1)} }}
  if = {{ limit = {{ OR = {{ has_country_flag = nap_fra_italian_campaign_active has_country_flag = nap_fra_egyptian_expedition_active has_country_flag = russian_campaign_active }} check_variable = {{ nap_army_prestige > 59 }} }} {vadd('napoleon_prestige',1)} }}
  if = {{ limit = {{ has_country_flag = nap_fra_peninsular_active OR = {{ has_war_with = SPR has_war_with = POR }} }} {vadd('peninsular_resistance',4)} {change('war_exhaustion',1)} {change('supply_pressure',2)} }}
  if = {{ limit = {{ has_country_flag = russian_campaign_active has_war_with = RUS }} {vadd('russian_supply',-6)} {vadd('russian_cohesion',-4)} {change('supply_pressure',3)} {change('war_exhaustion',2)}
    if = {{ limit = {{ OR = {{ check_variable = {{ nap_fra_russian_supply < 10 }} check_variable = {{ nap_fra_russian_cohesion < 15 }} }} NOT = {{ has_country_flag = nap_fra_russia_disaster_queued }} }} set_country_flag = nap_fra_russia_disaster_queued country_event = {{ id = napoleonic_collapse.1 hours = 6 }} }}
  }}
  if = {{ limit = {{ has_country_flag = grande_armee_destroyed has_country_flag = russian_campaign_active }} clr_country_flag = russian_campaign_active remove_ideas = nap_fra_russian_logistics remove_ideas = nap_fra_russian_prepared {vset('russian_supply',0)} }}
  nap_fra_decision_clamp = yes
  nap_fra_decision_refresh = yes
 }}
}}''')

    # Revolutionary government.
    add_effect(effects,'nap_fra_establish_national_assembly_effect',
      'has_completed_focus = FRA_convene_estates_general NOT = { has_country_flag = nap_fra_national_assembly }',
      f'set_country_flag = nap_fra_national_assembly {change("reform",3)} {change("legitimacy",3)} {vadd("faction_tension",5)}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_establish_national_assembly','Assert the National Assembly',
      'Turn the Estates-General into a permanent national legislature. Reform +3, legitimacy +3, faction tension +5.',
      'tag = FRA has_completed_focus = FRA_convene_estates_general NOT = { has_country_flag = nap_fra_national_assembly }',
      'nap_fra_establish_national_assembly_effect',30,once=True)

    add_effect(effects,'nap_fra_legislative_assembly_effect',
      'has_country_flag = nap_fra_national_assembly has_completed_focus = FRA_adopt_declaration NOT = { has_country_flag = nap_fra_legislative_assembly }',
      f'set_country_flag = nap_fra_legislative_assembly {change("reform",3)} {change("legitimacy",2)} {vadd("faction_tension",4)}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_legislative_assembly','Reconstitute the Legislative Assembly',
      'Translate the revolutionary settlement into a legislature capable of governing rather than merely declaring principles.',
      'tag = FRA has_country_flag = nap_fra_national_assembly has_completed_focus = FRA_adopt_declaration NOT = { has_country_flag = nap_fra_legislative_assembly }',
      'nap_fra_legislative_assembly_effect',35,once=True)

    add_effect(effects,'nap_fra_national_convention_effect',
      'has_country_flag = french_republic NOT = { has_country_flag = nap_fra_national_convention }',
      f'clr_country_flag = nap_fra_national_assembly clr_country_flag = nap_fra_legislative_assembly set_country_flag = nap_fra_national_convention {change("fervor",5)} {vadd("faction_tension",8)}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_national_convention','Convene the National Convention',
      'Replace the earlier assemblies with a republican convention. Revolutionary fervor rises, but so does factional tension.',
      'tag = FRA has_country_flag = french_republic NOT = { has_country_flag = nap_fra_national_convention }',
      'nap_fra_national_convention_effect',35,once=True)

    add_effect(effects,'nap_fra_support_girondins_effect','nap_fra_route_republican = yes NOT = { has_country_flag = directory_active }',
      f'{vadd("girondin_influence",10)} {vadd("faction_tension",4)} {change("legitimacy",2)} {change("fervor",-1)}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_support_girondins','Support the Girondin Clubs',
      'Strengthen decentralising republican deputies. Girondin influence +10, legitimacy +2, faction tension +4.',
      'tag = FRA nap_fra_route_republican = yes NOT = { has_country_flag = directory_active }',
      'nap_fra_support_girondins_effect',25,60)

    add_effect(effects,'nap_fra_support_jacobins_effect','nap_fra_route_republican = yes NOT = { has_country_flag = directory_active }',
      f'{vadd("jacobin_influence",10)} {vadd("faction_tension",5)} {change("fervor",3)} {change("legitimacy",-1)}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_support_jacobins','Mobilize the Jacobin Clubs',
      'Strengthen the radical clubs. Jacobin influence +10, fervor +3, legitimacy -1, faction tension +5.',
      'tag = FRA nap_fra_route_republican = yes NOT = { has_country_flag = directory_active }',
      'nap_fra_support_jacobins_effect',25,60)

    add_effect(effects,'nap_fra_issue_assignats_effect','has_country_flag = french_revolutionary_path NOT = { check_variable = { nap_treasury > 84 } }',
      f'set_country_flag = nap_fra_assignats_active {change("treasury",18)} {change("debt",8)} {change("legitimacy",-2)} {vadd("assignat_inflation",12)}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_issue_assignats','Issue a New Assignat Tranche',
      'Create immediate fiscal room at the cost of debt, legitimacy and accumulating inflation. Treasury +18, debt +8, assignat inflation +12.',
      'tag = FRA has_country_flag = french_revolutionary_path NOT = { check_variable = { nap_treasury > 84 } }',
      'nap_fra_issue_assignats_effect',15,90)

    add_effect(effects,'nap_fra_redeem_assignats_effect',
      f'has_country_flag = nap_fra_assignats_active {at_least("assignat_inflation",10)} NOT = {{ check_variable = {{ nap_treasury < 15 }} }}',
      f'{change("treasury",-15)} {change("debt",-5)} {change("legitimacy",2)} {vadd("assignat_inflation",-15)} if = {{ limit = {{ check_variable = {{ nap_fra_assignat_inflation < 10 }} }} clr_country_flag = nap_fra_assignats_active }}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_redeem_assignats','Redeem Assignats from Circulation',
      'Spend treasury to reduce paper-money pressure. Treasury -15, debt -5, legitimacy +2, assignat inflation -15.',
      f'tag = FRA has_country_flag = nap_fra_assignats_active {at_least("assignat_inflation",10)} NOT = {{ check_variable = {{ nap_treasury < 15 }} }}',
      'nap_fra_redeem_assignats_effect',20,90)

    add_effect(effects,'nap_fra_negotiate_vendee_effect',
      f'has_country_flag = french_revolutionary_path {at_least("vendee_unrest",10)} NOT = {{ check_variable = {{ nap_treasury < 8 }} }}',
      f'{change("treasury",-8)} {change("legitimacy",4)} {change("fervor",-2)} {vadd("vendee_unrest",-15)}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_negotiate_vendee','Negotiate with Refractory Parishes',
      'Use concessions, local intermediaries and relief to lower Vendée unrest by 15 at a fiscal and revolutionary-political cost.',
      f'tag = FRA has_country_flag = french_revolutionary_path {at_least("vendee_unrest",10)} NOT = {{ check_variable = {{ nap_treasury < 8 }} }}',
      'nap_fra_negotiate_vendee_effect',30,60)

    add_effect(effects,'nap_fra_columns_vendee_effect',
      f'has_country_flag = french_revolutionary_path {at_least("vendee_unrest",15)}',
      f'{change("war_exhaustion",4)} {change("legitimacy",-5)} {change("fervor",3)} {vadd("vendee_unrest",-20)}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_columns_vendee','Dispatch Republican Columns to the West',
      'Suppress unrest by force. Vendée unrest -20, but exhaustion rises and legitimacy falls.',
      f'tag = FRA has_country_flag = french_revolutionary_path {at_least("vendee_unrest",15)}',
      'nap_fra_columns_vendee_effect',35,75)

    add_effect(effects,'nap_fra_committee_public_safety_effect',
      'nap_fra_route_republican = yes has_completed_focus = FRA_reign_of_terror_focus NOT = { has_country_flag = nap_fra_committee_public_safety }',
      f'set_country_flag = nap_fra_committee_public_safety add_ideas = nap_fra_committee_public_safety {vadd("faction_tension",10)} {change("fervor",4)}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_committee_public_safety','Establish the Committee of Public Safety',
      'Create an emergency executive for war and internal crisis. It raises fervor and central capacity but intensifies factional tension.',
      'tag = FRA nap_fra_route_republican = yes has_completed_focus = FRA_reign_of_terror_focus NOT = { has_country_flag = nap_fra_committee_public_safety }',
      'nap_fra_committee_public_safety_effect',45,once=True)

    add_effect(effects,'nap_fra_debate_terror_effect',
      'has_country_flag = nap_fra_committee_public_safety NOT = { has_country_flag = nap_legacy_french_revolution_10_settled }',
      'country_event = { id = french_revolution.10 hours = 1 }')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_debate_terror','Debate Emergency Terror',
      'Put the Committee emergency programme before the Convention. The existing Terror event resolves whether the government embraces or restrains it.',
      'tag = FRA has_country_flag = nap_fra_committee_public_safety NOT = { has_country_flag = nap_legacy_french_revolution_10_settled }',
      'nap_fra_debate_terror_effect',20,once=True)

    thermidor_guard=f'has_country_flag = reign_of_terror_active OR = {{ {at_least("faction_tension",55)} check_variable = {{ nap_war_exhaustion > 39 }} }}'
    add_effect(effects,'nap_fra_thermidor_effect',thermidor_guard,
      f'remove_ideas = nap_fra_committee_public_safety {vadd("faction_tension",-20)} {vadd("jacobin_influence",-15)} country_event = {{ id = french_revolution.11 hours = 1 }}')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_thermidorian_reaction','Trigger a Thermidorian Reaction',
      'When factional tension or war exhaustion becomes severe, break the emergency regime and return authority to the Convention.',
      'tag = FRA '+thermidor_guard,'nap_fra_thermidor_effect',40,once=True)

    add_effect(effects,'nap_fra_install_directory_effect',
      'has_country_flag = nap_fra_thermidor_settled NOT = { has_country_flag = directory_active }',
      'country_event = { id = french_revolution.12 hours = 1 }')
    add_decision(sections,loc,'nap_fra_revolutionary_crisis','nap_fra_install_directory','Establish the Executive Directory',
      'Replace the post-Thermidor Convention with the Executive Directory through the existing guarded transition event.',
      'tag = FRA has_country_flag = nap_fra_thermidor_settled NOT = { has_country_flag = directory_active }',
      'nap_fra_install_directory_effect',30,once=True)

    # Bonaparte's ascent.
    add_effect(effects,'nap_fra_open_italian_campaign_effect',
      'has_completed_focus = FRA_italian_campaign NOT = { has_country_flag = nap_fra_italian_campaign_active } NOT = { has_country_flag = italian_campaign_won }',
      f'set_country_flag = nap_fra_italian_campaign_active if = {{ limit = {{ check_variable = {{ nap_fra_napoleon_prestige < 25 }} }} {vset("napoleon_prestige",25)} }} add_timed_idea = {{ idea = nap_funded_magazines days = 120 }} {change("treasury",-8)}')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_open_italian_campaign','Organize the Army of Italy',
      "Give Bonaparte an operational command, forward magazines and a political mandate. This starts the decision-driven Italian campaign.",
      'tag = FRA has_completed_focus = FRA_italian_campaign NOT = { has_country_flag = nap_fra_italian_campaign_active } NOT = { has_country_flag = italian_campaign_won }',
      'nap_fra_open_italian_campaign_effect',35,once=True)

    add_effect(effects,'nap_fra_italian_requisitions_effect','has_country_flag = nap_fra_italian_campaign_active',
      f'{change("treasury",8)} {change("supply_pressure",-5)} {change("legitimacy",-3)} {vadd("napoleon_prestige",3)}')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_italian_requisitions','Requisition Italian Magazines',
      'Live partly off the theatre. Treasury +8 and supply pressure -5, at a legitimacy cost; Napoleon prestige +3.',
      'tag = FRA has_country_flag = nap_fra_italian_campaign_active','nap_fra_italian_requisitions_effect',20,60)

    add_effect(effects,'nap_fra_italian_republics_effect','has_country_flag = nap_fra_italian_campaign_active',
      f'add_political_power = -20 {change("legitimacy",2)} {change("fervor",2)} {vadd("napoleon_prestige",5)}')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_italian_republics','Court the Italian Patriots',
      'Use republican clients and political theatre to convert campaigning into personal and revolutionary prestige.',
      'tag = FRA has_country_flag = nap_fra_italian_campaign_active','nap_fra_italian_republics_effect',25,75)

    add_effect(effects,'nap_fra_conclude_italian_campaign_effect',
      f'has_country_flag = nap_fra_italian_campaign_active {at_least("napoleon_prestige",35)}',
      f'clr_country_flag = nap_fra_italian_campaign_active set_country_flag = italian_campaign_won {change("army_prestige",5)} {vadd("napoleon_prestige",10)} add_stability = 0.02')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_conclude_italian_campaign','Conclude the Italian Campaign',
      'Convert battlefield reputation into a durable political fact. Requires Napoleon prestige 35; marks the Italian campaign successfully concluded.',
      f'tag = FRA has_country_flag = nap_fra_italian_campaign_active {at_least("napoleon_prestige",35)}',
      'nap_fra_conclude_italian_campaign_effect',35,once=True)

    add_effect(effects,'nap_fra_prepare_egypt_effect',
      'has_completed_focus = FRA_egyptian_expedition has_country_flag = italian_campaign_won NOT = { has_country_flag = nap_fra_egyptian_expedition_active } NOT = { has_country_flag = egyptian_expedition_complete }',
      f'set_country_flag = nap_fra_egyptian_expedition_active {change("treasury",-15)} {change("supply_pressure",10)} {vadd("napoleon_prestige",5)}')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_prepare_egypt','Prepare the Egyptian Expedition',
      'Commit money, shipping and political capital to Egypt. The expedition begins with substantial supply pressure.',
      'tag = FRA has_completed_focus = FRA_egyptian_expedition has_country_flag = italian_campaign_won NOT = { has_country_flag = nap_fra_egyptian_expedition_active } NOT = { has_country_flag = egyptian_expedition_complete }',
      'nap_fra_prepare_egypt_effect',45,once=True)

    add_effect(effects,'nap_fra_institute_egypt_effect','has_country_flag = nap_fra_egyptian_expedition_active NOT = { check_variable = { nap_treasury < 8 } }',
      f'{change("treasury",-8)} {change("reform",4)} {vadd("napoleon_prestige",4)} add_political_power = 15')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_institute_egypt','Found the Institut d’Égypte',
      'Use scholarship, surveys and administration to turn expeditionary prestige into reform and political capital.',
      'tag = FRA has_country_flag = nap_fra_egyptian_expedition_active NOT = { check_variable = { nap_treasury < 8 } }',
      'nap_fra_institute_egypt_effect',25,once=True)

    add_effect(effects,'nap_fra_egypt_supply_effect','has_country_flag = nap_fra_egyptian_expedition_active NOT = { check_variable = { nap_treasury < 10 } }',
      f'{change("treasury",-10)} {change("supply_pressure",-10)} {vadd("napoleon_prestige",2)}')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_egypt_supply','Secure Mediterranean Supply',
      'Spend treasury on shipping, depots and replacement stores. Supply pressure -10, Napoleon prestige +2.',
      'tag = FRA has_country_flag = nap_fra_egyptian_expedition_active NOT = { check_variable = { nap_treasury < 10 } }',
      'nap_fra_egypt_supply_effect',25,60)

    add_effect(effects,'nap_fra_return_egypt_effect',
      'has_country_flag = nap_fra_egyptian_expedition_active NOT = { check_variable = { nap_supply_pressure > 70 } }',
      f'clr_country_flag = nap_fra_egyptian_expedition_active set_country_flag = egyptian_expedition_complete {vadd("napoleon_prestige",10)} {change("legitimacy",2)}')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_return_egypt','Return from Egypt',
      'End the expedition before its logistical burden becomes politically ruinous. Requires supply pressure no higher than 70.',
      'tag = FRA has_country_flag = nap_fra_egyptian_expedition_active NOT = { check_variable = { nap_supply_pressure > 70 } }',
      'nap_fra_return_egypt_effect',30,once=True)

    brumaire_guard=f'has_completed_focus = FRA_brumaire_coup has_country_flag = directory_active has_country_flag = egyptian_expedition_complete {at_least("napoleon_prestige",45)} NOT = {{ has_country_flag = nap_legacy_french_revolution_14_settled }}'
    add_effect(effects,'nap_fra_stage_brumaire_effect',brumaire_guard,'country_event = { id = french_revolution.14 hours = 1 }')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_stage_brumaire','Stage the Coup of Brumaire',
      'Use military prestige to break the Directory. Requires Napoleon prestige 45 and a concluded Egyptian expedition.',
      'tag = FRA '+brumaire_guard,'nap_fra_stage_brumaire_effect',50,once=True)

    add_effect(effects,'nap_fra_constitution_year_viii_effect',
      'has_country_flag = consulate_established NOT = { has_country_flag = nap_fra_year_viii_settled }',
      f'set_country_flag = nap_fra_year_viii_settled add_ideas = nap_fra_consular_machine {change("reform",5)} {change("legitimacy",5)}')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_constitution_year_viii','Consolidate the Constitution of Year VIII',
      'Build the administrative state behind the Consulate. Reform +5, legitimacy +5 and a permanent Consular Machine spirit.',
      'tag = FRA has_country_flag = consulate_established NOT = { has_country_flag = nap_fra_year_viii_settled }',
      'nap_fra_constitution_year_viii_effect',40,once=True)

    empire_guard=f'has_completed_focus = FRA_proclaim_empire has_country_flag = consulate_established {at_least("napoleon_prestige",60)} NOT = {{ has_country_flag = nap_legacy_napoleonic_wars_3_settled }}'
    add_effect(effects,'nap_fra_proclaim_empire_effect',empire_guard,'country_event = { id = napoleonic_wars.3 hours = 1 }')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_proclaim_empire_decision','Submit the Empire to Plebiscitary Legitimacy',
      'Convert the Consulate into the Empire through the existing guarded proclamation event. Requires Napoleon prestige 60.',
      'tag = FRA '+empire_guard,'nap_fra_proclaim_empire_effect',55,once=True)

    coronation_guard='has_country_flag = empire_of_the_french NOT = { has_country_flag = nap_legacy_napoleonic_wars_4_settled }'
    add_effect(effects,'nap_fra_coronation_effect',coronation_guard,'country_event = { id = napoleonic_wars.4 hours = 1 }')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_coronation','Hold the Imperial Coronation',
      'Stage the coronation as a deliberate act of regime consolidation instead of waiting for a fixed delayed event.',
      'tag = FRA '+coronation_guard,'nap_fra_coronation_effect',50,once=True)

    add_effect(effects,'nap_fra_appoint_marshals_effect',
      'has_country_flag = empire_of_the_french has_completed_focus = FRA_grande_armee_focus NOT = { has_country_flag = nap_fra_marshals_appointed }',
      f'set_country_flag = nap_fra_marshals_appointed add_ideas = nap_fra_marshals_empire {change("army_prestige",8)} {vadd("napoleon_prestige",10)} add_command_power = 50')
    add_decision(sections,loc,'nap_fra_napoleon_rise','nap_fra_appoint_marshals','Create the Marshals of the Empire',
      'Institutionalize a senior imperial command cadre. Army prestige +8, Napoleon prestige +10 and a permanent Marshals spirit.',
      'tag = FRA has_country_flag = empire_of_the_french has_completed_focus = FRA_grande_armee_focus NOT = { has_country_flag = nap_fra_marshals_appointed }',
      'nap_fra_appoint_marshals_effect',45,once=True)

    # Continental System.
    continental_guard='has_completed_focus = FRA_continental_system_focus has_country_flag = empire_of_the_french NOT = { has_global_flag = continental_system_active }'
    add_effect(effects,'nap_fra_activate_continental_effect',continental_guard,
      f'country_event = {{ id = napoleonic_wars.10 hours = 1 }} {vadd("continental_pressure",10)}')
    add_decision(sections,loc,'nap_fra_continental_system','nap_fra_activate_continental_system','Issue the Continental Decrees',
      'Activate the Continental System through the existing event, then manage compliance through recurring diplomatic pressure.',
      'tag = FRA '+continental_guard,'nap_fra_activate_continental_effect',50,once=True)

    for tag,name in CONTINENTAL_TARGETS:
        key='nap_fra_continental_pressure_'+tag.lower()
        effect=key+'_effect'
        flag='nap_continental_enforced_'+tag.lower()
        guard=f'has_global_flag = continental_system_active {tag} = {{ exists = yes NOT = {{ has_war_with = FRA }} NOT = {{ has_country_flag = {flag} }} }} NOT = {{ check_variable = {{ nap_treasury < 5 }} }}'
        body=f'{change("treasury",-5)} {vadd("continental_pressure",8)} {tag} = {{ add_timed_idea = {{ idea = nap_continental_compliance days = 180 }} set_country_flag = {{ flag = {flag} days = 180 }} add_opinion_modifier = {{ target = FRA modifier = small_decrease }} }}'
        add_effect(effects,effect,guard,body)
        add_decision(sections,loc,'nap_fra_continental_system',key,'Pressure '+name+' to Enforce the Blockade',
          'Spend diplomatic and fiscal capital to impose 180 days of Continental customs enforcement. This raises accumulated pressure on British trade.',
          'tag = FRA '+guard,effect,25,180)

    add_effect(effects,'nap_fra_tighten_continental_customs_effect',
      'has_global_flag = continental_system_active NOT = { check_variable = { nap_treasury < 10 } }',
      f'{change("treasury",-10)} {change("legitimacy",-2)} {vadd("continental_pressure",10)}')
    add_decision(sections,loc,'nap_fra_continental_system','nap_fra_tighten_continental_customs','Tighten Continental Customs',
      'Increase inspections and customs enforcement. Treasury -10, legitimacy -2, Continental pressure +10.',
      'tag = FRA has_global_flag = continental_system_active NOT = { check_variable = { nap_treasury < 10 } }',
      'nap_fra_tighten_continental_customs_effect',30,90)

    add_effect(effects,'nap_fra_relax_continental_customs_effect','has_global_flag = continental_system_active',
      f'{change("legitimacy",3)} {vadd("continental_pressure",-12)} add_stability = 0.01')
    add_decision(sections,loc,'nap_fra_continental_system','nap_fra_relax_continental_customs','Permit Licensed Continental Trade',
      'Ease enforcement to reduce domestic and allied friction. Legitimacy +3, Continental pressure -12.',
      'tag = FRA has_global_flag = continental_system_active','nap_fra_relax_continental_customs_effect',20,90)

    # Foreign evasion / compliance decisions.
    foreign_guard='has_global_flag = continental_system_active has_idea = nap_continental_compliance NOT = { tag = FRA } NOT = { tag = ENG }'
    effects.append(f'''nap_continental_evade_customs_effect = {{
 if = {{ limit = {{ {foreign_guard} }}
  remove_ideas = nap_continental_compliance
  set_country_flag = {{ flag = nap_continental_smuggling days = 120 }}
  add_political_power = 20
  FRA = {{ if = {{ limit = {{ exists = yes }} {vadd("continental_pressure",-8)} nap_fra_decision_clamp = yes nap_fra_decision_refresh = yes }} }}
  ENG = {{ if = {{ limit = {{ exists = yes }} add_political_power = 10 }} }}
 }}
}}''')
    add_decision(sections,loc,'nap_continental_foreign','nap_continental_evade_customs','Tolerate Smuggling through the Blockade',
      'End formal compliance early, gain political room and reduce French Continental pressure. Britain benefits from the breach.',
      foreign_guard,'nap_continental_evade_customs_effect',25,120,visible=foreign_guard,ai=1)

    effects.append(f'''nap_continental_enforce_locally_effect = {{
 if = {{ limit = {{ {foreign_guard} }}
  add_political_power = -10
  add_stability = 0.01
  FRA = {{ if = {{ limit = {{ exists = yes }} {vadd("continental_pressure",4)} nap_fra_decision_clamp = yes nap_fra_decision_refresh = yes }} }}
 }}
}}''')
    add_decision(sections,loc,'nap_continental_foreign','nap_continental_enforce_locally','Enforce the French Customs Regime',
      'Accept the domestic enforcement cost of the blockade, strengthening French Continental pressure while marginally stabilizing policy.',
      foreign_guard,'nap_continental_enforce_locally_effect',20,90,visible=foreign_guard,ai=1)

    # Peninsular War.
    peninsula_launch='has_completed_focus = FRA_invade_iberia has_country_flag = empire_of_the_french NOT = { has_country_flag = nap_fra_peninsular_active } OR = { SPR = { exists = yes } POR = { exists = yes } }'
    add_effect(effects,'nap_fra_launch_peninsular_effect',peninsula_launch,
      f'''set_country_flag = nap_fra_peninsular_active {vset("peninsular_resistance",35)} add_ideas = nap_fra_peninsular_guerrilla_war
      if = {{ limit = {{ SPR = {{ exists = yes }} NOT = {{ has_war_with = SPR }} }} declare_war_on = {{ target = SPR type = annex_everything }} }}
      if = {{ limit = {{ POR = {{ exists = yes }} NOT = {{ has_war_with = POR }} }} declare_war_on = {{ target = POR type = annex_everything }} }}
      SPR = {{ if = {{ limit = {{ exists = yes }} }} add_ideas = spanish_ulcer }}
      {change("supply_pressure",8)}''')
    add_decision(sections,loc,'nap_fra_peninsular_war','nap_fra_launch_peninsular_intervention','Intervene in Iberia',
      'Begin the Peninsular War through a decision rather than the focus automatically declaring war. Resistance starts at 35 and immediately burdens French supply.',
      'tag = FRA '+peninsula_launch,'nap_fra_launch_peninsular_effect',50,once=True)

    add_effect(effects,'nap_fra_peninsular_depots_effect',
      'has_country_flag = nap_fra_peninsular_active NOT = { check_variable = { nap_treasury < 12 } }',
      f'{change("treasury",-12)} {change("supply_pressure",-10)} {vadd("peninsular_resistance",-4)} add_timed_idea = {{ idea = nap_funded_magazines days = 90 }}')
    add_decision(sections,loc,'nap_fra_peninsular_war','nap_fra_peninsular_depots','Fortify the Iberian Depots',
      'Spend 12 treasury to reduce supply pressure and make isolated garrisons less vulnerable. Resistance -4.',
      'tag = FRA has_country_flag = nap_fra_peninsular_active NOT = { check_variable = { nap_treasury < 12 } }',
      'nap_fra_peninsular_depots_effect',30,60)

    add_effect(effects,'nap_fra_peninsular_conciliate_effect','has_country_flag = nap_fra_peninsular_active',
      f'{change("legitimacy",3)} {change("fervor",-1)} {vadd("peninsular_resistance",-12)} add_political_power = -25')
    add_decision(sections,loc,'nap_fra_peninsular_war','nap_fra_peninsular_conciliate','Conciliate Spanish Elites',
      'Spend political capital on municipal, clerical and elite accommodation. Resistance -12 and legitimacy +3.',
      'tag = FRA has_country_flag = nap_fra_peninsular_active','nap_fra_peninsular_conciliate_effect',25,75)

    add_effect(effects,'nap_fra_peninsular_columns_effect','has_country_flag = nap_fra_peninsular_active',
      f'{vadd("peninsular_resistance",-18)} {change("war_exhaustion",5)} {change("legitimacy",-5)} {change("army_prestige",2)}')
    add_decision(sections,loc,'nap_fra_peninsular_war','nap_fra_peninsular_columns','Deploy Mobile Counter-Guerrilla Columns',
      'Reduce resistance by force at the cost of exhaustion and legitimacy. Resistance -18, exhaustion +5, legitimacy -5.',
      'tag = FRA has_country_flag = nap_fra_peninsular_active','nap_fra_peninsular_columns_effect',30,75)

    add_effect(effects,'nap_fra_peninsular_rotate_effect',
      'has_country_flag = nap_fra_peninsular_active NOT = { check_variable = { nap_treasury < 8 } }',
      f'{change("treasury",-8)} {change("war_exhaustion",-5)} {change("army_prestige",-2)} add_timed_idea = {{ idea = nap_army_rotation days = 45 }}')
    add_decision(sections,loc,'nap_fra_peninsular_war','nap_fra_peninsular_rotate','Rotate the Occupation Army',
      'Trade operational tempo and prestige for lower war exhaustion among dispersed garrisons.',
      'tag = FRA has_country_flag = nap_fra_peninsular_active NOT = { check_variable = { nap_treasury < 8 } }',
      'nap_fra_peninsular_rotate_effect',25,60)

    peninsula_win=f'has_country_flag = nap_fra_peninsular_active {at_most("peninsular_resistance",25)} {at_least("napoleon_prestige",55)} OR = {{ has_war_with = SPR has_war_with = POR }}'
    add_effect(effects,'nap_fra_peninsular_settlement_effect',peninsula_win,
      f'''set_country_flag = nap_fra_peninsular_victory clr_country_flag = nap_fra_peninsular_active remove_ideas = nap_fra_peninsular_guerrilla_war {vadd("napoleon_prestige",6)} {change("legitimacy",4)}
      if = {{ limit = {{ has_war_with = SPR }} white_peace = SPR }}
      if = {{ limit = {{ has_war_with = POR }} white_peace = POR }}''')
    add_decision(sections,loc,'nap_fra_peninsular_war','nap_fra_peninsular_settlement','Impose a Bounded Iberian Settlement',
      'When resistance has been reduced below 25 and Napoleon prestige is at least 55, end the Iberian war without annexing Spain or Portugal.',
      'tag = FRA '+peninsula_win,'nap_fra_peninsular_settlement_effect',40,once=True)

    peninsula_exit=f'has_country_flag = nap_fra_peninsular_active OR = {{ {at_least("peninsular_resistance",65)} check_variable = {{ nap_war_exhaustion > 59 }} }}'
    add_effect(effects,'nap_fra_peninsular_withdraw_effect',peninsula_exit,
      f'''set_country_flag = nap_fra_peninsular_withdrawal clr_country_flag = nap_fra_peninsular_active remove_ideas = nap_fra_peninsular_guerrilla_war {vadd("napoleon_prestige",-8)} {change("legitimacy",-5)} {change("war_exhaustion",-8)}
      if = {{ limit = {{ has_war_with = SPR }} white_peace = SPR }}
      if = {{ limit = {{ has_war_with = POR }} white_peace = POR }}''')
    add_decision(sections,loc,'nap_fra_peninsular_war','nap_fra_peninsular_withdraw','Abandon the Deep Iberian Occupation',
      'Cut losses when resistance or exhaustion becomes intolerable. The war ends without annexation, but prestige and legitimacy suffer.',
      'tag = FRA '+peninsula_exit,'nap_fra_peninsular_withdraw_effect',25,once=True)

    # Russian campaign.
    prep_guard='has_completed_focus = FRA_invade_russia has_country_flag = empire_of_the_french NOT = { has_country_flag = russian_campaign_active } NOT = { has_country_flag = nap_fra_russian_campaign_resolved }'
    add_effect(effects,'nap_fra_russia_magazines_effect',prep_guard+' NOT = { check_variable = { nap_treasury < 15 } }',
      f'{change("treasury",-15)} {vadd("russian_supply",20)} add_timed_idea = {{ idea = nap_fra_russian_prepared days = 180 }}')
    add_decision(sections,loc,'nap_fra_russian_campaign','nap_fra_russia_magazines','Build Polish Forward Magazines',
      'Spend 15 treasury to raise Russian-campaign supply preparation by 20.',
      'tag = FRA '+prep_guard+' NOT = { check_variable = { nap_treasury < 15 } }',
      'nap_fra_russia_magazines_effect',30,90)

    add_effect(effects,'nap_fra_russia_remounts_effect',prep_guard+' NOT = { check_variable = { nap_treasury < 10 } }',
      f'{change("treasury",-10)} {vadd("russian_supply",12)} {vadd("russian_cohesion",5)} {change("army_prestige",2)}')
    add_decision(sections,loc,'nap_fra_russian_campaign','nap_fra_russia_remounts','Accumulate Remounts and Wagons',
      'Prepare horses, wagons and replacement transport. Supply preparation +12, cohesion +5.',
      'tag = FRA '+prep_guard+' NOT = { check_variable = { nap_treasury < 10 } }',
      'nap_fra_russia_remounts_effect',25,75)

    add_effect(effects,'nap_fra_russia_allies_effect',prep_guard,
      f'add_political_power = -30 {vadd("russian_supply",8)} {vadd("russian_cohesion",8)} {change("legitimacy",1)}')
    add_decision(sections,loc,'nap_fra_russian_campaign','nap_fra_russia_allies','Coordinate Allied Contingents',
      'Spend political capital coordinating client and allied contingents. Supply preparation +8, cohesion +8.',
      'tag = FRA '+prep_guard,'nap_fra_russia_allies_effect',25,75)

    russia_launch=prep_guard+f' {at_least("russian_supply",45)} RUS = {{ exists = yes }} NOT = {{ has_war_with = RUS }}'
    add_effect(effects,'nap_fra_russia_launch_effect',russia_launch,
      f'set_country_flag = nap_fra_russian_launch_authorized add_ideas = nap_fra_russian_logistics {vadd("napoleon_prestige",5)} country_event = {{ id = napoleonic_wars.16 hours = 1 }}')
    add_decision(sections,loc,'nap_fra_russian_campaign','nap_fra_russia_launch','Cross the Niemen',
      'Open the Russian campaign council once supply preparation reaches 45. The guarded invasion event still lets France abandon the invasion at the final moment.',
      'tag = FRA '+russia_launch,'nap_fra_russia_launch_effect',50,once=True)

    add_effect(effects,'nap_fra_russia_forward_depots_effect',
      'has_country_flag = russian_campaign_active has_war_with = RUS NOT = { check_variable = { nap_treasury < 15 } }',
      f'{change("treasury",-15)} {vadd("russian_supply",20)} {vadd("russian_cohesion",5)} {change("supply_pressure",-8)}')
    add_decision(sections,loc,'nap_fra_russian_campaign','nap_fra_russia_forward_depots','Establish Forward Depots',
      'Spend 15 treasury to restore 20 campaign supply and 5 cohesion while reducing national supply pressure.',
      'tag = FRA has_country_flag = russian_campaign_active has_war_with = RUS NOT = { check_variable = { nap_treasury < 15 } }',
      'nap_fra_russia_forward_depots_effect',30,60)

    add_effect(effects,'nap_fra_russia_winter_quarters_effect','has_country_flag = russian_campaign_active has_war_with = RUS',
      f'{vadd("russian_supply",10)} {vadd("russian_cohesion",15)} {change("army_prestige",-4)} {change("war_exhaustion",-3)} add_timed_idea = {{ idea = nap_army_rotation days = 60 }}')
    add_decision(sections,loc,'nap_fra_russian_campaign','nap_fra_russia_winter_quarters','Halt for Winter Quarters',
      'Recover supply and cohesion at the cost of operational prestige. Supply +10, cohesion +15, army prestige -4.',
      'tag = FRA has_country_flag = russian_campaign_active has_war_with = RUS',
      'nap_fra_russia_winter_quarters_effect',25,75)

    add_effect(effects,'nap_fra_russia_press_on_effect','has_country_flag = russian_campaign_active has_war_with = RUS',
      f'{vadd("russian_supply",-20)} {vadd("russian_cohesion",-10)} {vadd("napoleon_prestige",8)} {change("war_exhaustion",4)}')
    add_decision(sections,loc,'nap_fra_russian_campaign','nap_fra_russia_press_on','Press Deeper into Russia',
      'Trade logistical safety for prestige and operational momentum. Supply -20, cohesion -10, Napoleon prestige +8.',
      'tag = FRA has_country_flag = russian_campaign_active has_war_with = RUS',
      'nap_fra_russia_press_on_effect',25,60)

    russia_win=f'has_country_flag = russian_campaign_active has_war_with = RUS {at_least("russian_supply",40)} {at_least("russian_cohesion",40)} {at_least("napoleon_prestige",65)}'
    add_effect(effects,'nap_fra_russia_settlement_effect',russia_win,
      f'set_country_flag = nap_fra_russian_victory {vadd("napoleon_prestige",8)} {change("legitimacy",5)} country_event = {{ id = napoleonic_wars.13 hours = 1 }}')
    add_decision(sections,loc,'nap_fra_russian_campaign','nap_fra_russia_settlement','Offer Russia a Continental Settlement',
      'A successful campaign can end through a bounded Tilsit-style settlement instead of a scripted French disaster. Requires supply/cohesion 40 and Napoleon prestige 65.',
      'tag = FRA '+russia_win,'nap_fra_russia_settlement_effect',45,once=True)

    russia_retreat=f'has_country_flag = russian_campaign_active has_war_with = RUS OR = {{ check_variable = {{ nap_fra_russian_supply < 35 }} check_variable = {{ nap_war_exhaustion > 54 }} }}'
    add_effect(effects,'nap_fra_russia_retreat_effect',russia_retreat,
      f'''set_country_flag = nap_fra_russian_organized_retreat clr_country_flag = russian_campaign_active remove_ideas = nap_fra_russian_logistics remove_ideas = nap_fra_russian_prepared
      white_peace = RUS {vadd("napoleon_prestige",-12)} {change("army_prestige",-8)} {change("legitimacy",-5)} {change("war_exhaustion",-8)}''')
    add_decision(sections,loc,'nap_fra_russian_campaign','nap_fra_russia_retreat','Order an Organized Retreat',
      'Withdraw before the army collapses. The war ends without territorial gain, but this avoids automatically destroying the Grande Armée.',
      'tag = FRA '+russia_retreat,'nap_fra_russia_retreat_effect',25,once=True)

    # Collapse, Restoration and Hundred Days.
    abdicate_guard='has_country_flag = empire_of_the_french OR = { has_country_flag = grande_armee_destroyed check_variable = { nap_war_exhaustion > 59 } } OR = { has_war_with = ENG has_war_with = PRU has_war_with = HAB has_war_with = RUS } NOT = { has_country_flag = napoleon_on_elba }'
    add_effect(effects,'nap_fra_fontainebleau_effect',abdicate_guard,'country_event = { id = napoleonic_collapse.5 hours = 1 }')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_fontainebleau','Convene the Fontainebleau Abdication Council',
      'When the imperial war position becomes untenable, open the guarded abdication event. France may still choose to fight on.',
      'tag = FRA '+abdicate_guard,'nap_fra_fontainebleau_effect',30,once=True)

    restore_guard='has_country_flag = napoleon_on_elba NOT = { has_country_flag = bourbon_restoration } NOT = { has_country_flag = nap_legacy_napoleonic_collapse_6_settled }'
    add_effect(effects,'nap_fra_restore_bourbons_effect',restore_guard,'country_event = { id = napoleonic_collapse.6 hours = 1 }')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_restore_bourbons','Restore Louis XVIII',
      'Complete the first Restoration deliberately after abdication rather than through a fixed delay.',
      'tag = FRA '+restore_guard,'nap_fra_restore_bourbons_effect',30,once=True)

    add_effect(effects,'nap_fra_restoration_charter_effect',
      'has_country_flag = bourbon_restoration NOT = { has_country_flag = nap_fra_restoration_charter }',
      f'set_country_flag = nap_fra_restoration_charter add_ideas = nap_fra_restoration_charter {change("legitimacy",6)} {change("reform",3)} add_stability = 0.04')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_restoration_charter','Grant a Constitutional Charter',
      'Bind the restored monarchy to a limited post-revolutionary settlement. Legitimacy +6, reform +3 and a permanent Charter spirit.',
      'tag = FRA has_country_flag = bourbon_restoration NOT = { has_country_flag = nap_fra_restoration_charter }',
      'nap_fra_restoration_charter_effect',40,once=True)

    elba_guard='has_completed_focus = FRA_return_from_elba has_country_flag = bourbon_restoration has_country_flag = napoleon_on_elba NOT = { has_country_flag = nap_legacy_napoleonic_collapse_8_settled }'
    add_effect(effects,'nap_fra_return_elba_effect',elba_guard,'country_event = { id = napoleonic_collapse.8 hours = 1 }')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_return_elba','Return from Elba',
      'Trigger the Hundred Days through the guarded return event when the restoration and focus conditions are present.',
      'tag = FRA '+elba_guard,'nap_fra_return_elba_effect',35,once=True)

    add_effect(effects,'nap_fra_hundred_days_rally_effect',
      'has_country_flag = hundred_days NOT = { has_country_flag = nap_fra_hundred_days_rallied }',
      f'set_country_flag = nap_fra_hundred_days_rallied add_ideas = nap_fra_hundred_days_mobilization {change("army_prestige",6)} {change("war_exhaustion",4)} add_command_power = 40')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_hundred_days_rally','Rally the Veterans of the Empire',
      'Rebuild an army quickly around veterans and loyal cadres. Army prestige +6 and a mobilization spirit, but exhaustion rises.',
      'tag = FRA has_country_flag = hundred_days NOT = { has_country_flag = nap_fra_hundred_days_rallied }',
      'nap_fra_hundred_days_rally_effect',30,once=True)

    add_effect(effects,'nap_fra_hundred_days_liberal_effect',
      'has_country_flag = hundred_days NOT = { has_country_flag = nap_fra_hundred_days_liberal_act }',
      f'set_country_flag = nap_fra_hundred_days_liberal_act {change("legitimacy",6)} {change("reform",4)} {vadd("napoleon_prestige",-3)} add_stability = 0.03')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_hundred_days_liberal','Issue an Additional Act',
      'Trade some imperial personal authority for constitutional support. Legitimacy +6, reform +4, Napoleon prestige -3.',
      'tag = FRA has_country_flag = hundred_days NOT = { has_country_flag = nap_fra_hundred_days_liberal_act }',
      'nap_fra_hundred_days_liberal_effect',30,once=True)

    waterloo_guard='has_country_flag = hundred_days OR = { has_war_with = ENG has_war_with = PRU } NOT = { has_global_flag = waterloo_fought }'
    add_effect(effects,'nap_fra_hundred_days_battle_effect',waterloo_guard,'news_event = { id = napoleonic_collapse.9 hours = 1 }')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_hundred_days_battle','Seek a Decisive Battle in Belgium',
      'Risk the restored Empire on a decisive campaign. This invokes the guarded Waterloo outcome event rather than firing it after a fixed 109-day timer.',
      'tag = FRA '+waterloo_guard,'nap_fra_hundred_days_battle_effect',40,once=True)

    second_abdication='has_global_flag = waterloo_fought NOT = { has_country_flag = napoleon_on_st_helena }'
    add_effect(effects,'nap_fra_second_abdication_effect',second_abdication,
      'remove_ideas = nap_fra_hundred_days_mobilization country_event = { id = napoleonic_collapse.10 hours = 1 }')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_second_abdication','Accept the Second Abdication',
      'After Waterloo, complete Napoleon’s second abdication and restore the Bourbons through the existing guarded event.',
      'tag = FRA '+second_abdication,'nap_fra_second_abdication_effect',20,once=True)

    hundred_survive='has_country_flag = hundred_days has_war = no NOT = { has_global_flag = waterloo_fought }'
    add_effect(effects,'nap_fra_hundred_days_survive_effect',hundred_survive,
      f'clr_country_flag = hundred_days set_country_flag = nap_fra_hundred_days_survived remove_ideas = nap_fra_hundred_days_mobilization add_ideas = liberal_empire {change("legitimacy",5)} add_stability = 0.05')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_hundred_days_survive','Consolidate a Surviving Hundred Days Regime',
      'If France reaches peace without Waterloo, convert the emergency return into a durable liberal-imperial settlement instead of forcing historical defeat.',
      'tag = FRA '+hundred_survive,'nap_fra_hundred_days_survive_effect',50,once=True)

    concert_guard='has_war = no OR = { has_country_flag = bourbon_restoration has_country_flag = nap_fra_hundred_days_survived } NOT = { has_global_flag = concert_of_europe_established }'
    add_effect(effects,'nap_fra_concert_effect',concert_guard,
      f'set_country_flag = nap_fra_postwar_settlement add_ideas = nap_fra_postwar_exhaustion {change("war_exhaustion",-12)} news_event = {{ id = napoleonic_collapse.12 hours = 1 }}')
    add_decision(sections,loc,'nap_fra_restoration_cycle','nap_fra_concert','Accept the European Postwar Settlement',
      'At peace after the Restoration or a surviving Hundred Days regime, close the campaign cycle with a deliberate postwar settlement and demobilisation burden.',
      'tag = FRA '+concert_guard,'nap_fra_concert_effect',45,once=True)

    decisions=[]
    for category,rows in sections.items():
        decisions.append(category+' = {\n '+' \n '.join(rows)+'\n}')
    category_script=[
      'nap_fra_revolutionary_crisis = { icon = generic_political_discourse allowed = { tag = FRA } visible = { tag = FRA has_completed_focus = FRA_convene_estates_general NOT = { has_country_flag = consulate_established } NOT = { has_country_flag = empire_of_the_french } } }',
      'nap_fra_napoleon_rise = { icon = generic_political_discourse allowed = { tag = FRA } visible = { tag = FRA OR = { has_completed_focus = FRA_italian_campaign has_country_flag = consulate_established has_country_flag = empire_of_the_french } NOT = { has_country_flag = bourbon_restoration } } }',
      'nap_fra_continental_system = { icon = generic_political_discourse allowed = { tag = FRA } visible = { tag = FRA OR = { has_completed_focus = FRA_continental_system_focus has_global_flag = continental_system_active } } }',
      'nap_fra_peninsular_war = { icon = generic_political_discourse allowed = { tag = FRA } visible = { tag = FRA OR = { has_completed_focus = FRA_invade_iberia has_country_flag = nap_fra_peninsular_active has_country_flag = nap_fra_peninsular_resolved } } }',
      'nap_fra_russian_campaign = { icon = generic_political_discourse allowed = { tag = FRA } visible = { tag = FRA OR = { has_completed_focus = FRA_invade_russia has_country_flag = russian_campaign_active has_country_flag = nap_fra_russian_campaign_resolved } } }',
      'nap_fra_restoration_cycle = { icon = generic_political_discourse allowed = { tag = FRA } visible = { tag = FRA OR = { has_country_flag = empire_of_the_french has_country_flag = napoleon_on_elba has_country_flag = bourbon_restoration has_country_flag = hundred_days has_country_flag = napoleon_on_st_helena has_country_flag = nap_fra_hundred_days_survived } } }',
      'nap_continental_foreign = { icon = generic_political_discourse allowed = { always = yes } visible = { has_global_flag = continental_system_active has_idea = nap_continental_compliance NOT = { tag = FRA } NOT = { tag = ENG } } }',
    ]

    on_actions='''on_actions = {
 on_startup = { effect = { every_country = { limit = { tag = FRA } nap_fra_decision_initialize = yes nap_fra_decision_refresh = yes } } }
 on_monthly = { effect = { if = { limit = { tag = FRA } nap_fra_decision_monthly = yes } } }
 on_army_leader_won_combat = { effect = { FROM = { if = { limit = { tag = FRA OR = { has_country_flag = nap_fra_italian_campaign_active has_country_flag = nap_fra_egyptian_expedition_active has_country_flag = russian_campaign_active } } add_to_variable = { nap_fra_napoleon_prestige = 0.35 } nap_fra_decision_clamp = yes } } } }
 on_army_leader_lost_combat = { effect = { FROM = { if = { limit = { tag = FRA OR = { has_country_flag = nap_fra_italian_campaign_active has_country_flag = nap_fra_egyptian_expedition_active has_country_flag = russian_campaign_active } } add_to_variable = { nap_fra_napoleon_prestige = -0.25 } nap_fra_decision_clamp = yes } } } }
}'''

    loc += [
      ' nap_fra_metric_vendee:0 "Vendée Unrest"',
      ' nap_fra_metric_assignats:0 "Assignat Inflation"',
      ' nap_fra_metric_factions:0 "Faction Tension"',
      ' nap_fra_metric_prestige:0 "Napoleon Prestige"',
      ' nap_fra_metric_continental:0 "Continental Pressure"',
      ' nap_fra_metric_peninsula:0 "Peninsular Resistance"',
      ' nap_fra_metric_russia_supply:0 "Russian Campaign Supply"',
      ' nap_fra_metric_russia_cohesion:0 "Russian Campaign Cohesion"',
    ]

    docs='''# France decision mechanics

The six large French historical arcs now use decisions and bounded variables rather than relying mainly on focus-completion effects or calendar timers.

## Revolutionary crisis
The Estates-General unlocks a government-management sequence for the National Assembly, Legislative Assembly and Convention. Girondin and Jacobin influence are repeatable political choices. Assignat issuance creates immediate treasury at the cost of inflation. Vendée unrest rises during revolutionary war and can be reduced through conciliation or coercion. The Committee of Public Safety, Terror, Thermidor and Directory are deliberate decisions that invoke the existing guarded narrative events.

## Bonaparte's ascent
The Italian and Egyptian focus nodes unlock campaign decisions instead of automatically marking their campaigns complete. Italy builds Napoleon prestige; Egypt tests supply and administrative investment. Brumaire requires a completed Egyptian expedition and sufficient prestige. The Empire requires further prestige. Coronation and creation of the Marshals are separate decisions.

## Continental System
The Continental System is activated by decision. France can pressure Russia, Prussia, Austria, Spain, Portugal, the Netherlands, Denmark and Sweden. Compliance applies a timed customs spirit; foreign countries can choose local enforcement or smuggling/evasion. Aggregate French Continental pressure dynamically applies or removes a British trade-pressure spirit.

## Peninsular War
The Iberian focus no longer automatically declares war. The intervention decision starts the conflict and a resistance meter. Resistance rises monthly while the conflict continues. France can fund depots, conciliate elites, use counter-guerrilla columns or rotate the army. A low-resistance prestige-based bounded settlement and a high-resistance/exhaustion withdrawal both end the war without scripted annexation.

## Russian campaign
The invasion focus unlocks preparation rather than immediate war. Magazines, remounts and allied coordination build campaign supply. Crossing the Niemen requires at least 45 supply preparation and invokes the existing guarded invasion event. Supply and cohesion fall monthly in Russia. Forward depots, winter quarters and pressing deeper trade resources for survival or prestige. France can earn a bounded Russian settlement, order an organised retreat, or suffer the existing Grande Armée collapse event when supply/cohesion become catastrophic.

## 1814–1815 state transitions
Abdication, the first Restoration, the Restoration Charter, return from Elba, Hundred Days mobilisation, the Additional Act, Waterloo, second abdication and the postwar settlement are explicit decisions. A Hundred Days regime that reaches peace without Waterloo has a supported non-historical survival settlement instead of being automatically forced into the historical defeat chain.

All major transition events retain their existing execution guards and one-time flags. The decision effects repeat their availability checks. The new variables are clamped to 0–100. Runtime balance remains provisional.
'''

    return {
      'common/decisions/nap_france_campaigns.txt':'\n\n'.join(decisions)+'\n',
      'common/decisions/categories/nap_france_campaigns.txt':'\n'.join(category_script)+'\n',
      'common/scripted_effects/nap_france_campaigns.txt':'\n\n'.join(effects)+'\n',
      'common/ideas/nap_france_campaigns.txt':'\n'.join(ideas)+'\n',
      'common/on_actions/nap_france_campaigns.txt':on_actions+'\n',
      'localisation/english/nap_france_campaigns_l_english.yml':'\n'.join(loc)+'\n',
      'docs/france-decision-mechanics.md':docs,
      'docs/france-decision-index.json':json.dumps(DECISION_META,indent=2)+'\n',
    }


def _focus_map(text):
    parsed=parse(text)
    result={}
    for node in walk(parsed):
        if node.key=='focus' and isinstance(node.value,list) and node.scalar('id'):
            result[node.scalar('id')]=node
    return parsed,result


def _strip_direct_event(focus,event_id):
    for reward in focus.children('completion_reward'):
        reward.value=[e for e in reward.value if not (e.key=='country_event' and isinstance(e.value,list) and e.scalar('id')==event_id)]


def _strip_direct_key(focus,key):
    for reward in focus.children('completion_reward'):
        reward.value=[e for e in reward.value if e.key!=key]


def _append_reward(focus,text):
    rewards=focus.children('completion_reward')
    if not rewards:
        focus.value.append(Entry('completion_reward',parse(text)))
    else:
        rewards[0].value += parse(text)


def _event_map(text):
    parsed=parse(text)
    return parsed,{node.scalar('id'):node for node in parsed if node.key in ('country_event','news_event') and node.scalar('id')}


def _make_triggered_only(event):
    event.value=[e for e in event.value if e.key not in ('trigger','mean_time_to_happen')]
    if not event.children('is_triggered_only'):
        event.value.append(Entry('is_triggered_only','yes'))


def _remove_called_event(event,event_id):
    for option in event.children('option'):
        def clean(entries):
            out=[]
            for e in entries:
                if e.key=='country_event' and isinstance(e.value,list) and e.scalar('id')==event_id:
                    continue
                if isinstance(e.value,list):
                    e.value=clean(e.value)
                out.append(e)
            return out
        option.value=clean(option.value)


def postprocess(outputs,root):
    updates={}
    focus_path='common/national_focus/FRA.txt'
    focus_text=outputs.get(focus_path)
    if focus_text is None:
        focus_text=(root/focus_path).read_text(encoding='utf-8-sig')
    if isinstance(focus_text,bytes):focus_text=focus_text.decode('utf-8-sig')
    parsed,focuses=_focus_map(focus_text)

    # Focuses now unlock decisions; they no longer execute the major transition automatically.
    transition_calls={
      'FRA_reign_of_terror_focus':'french_revolution.10',
      'FRA_brumaire_coup':'french_revolution.14',
      'FRA_proclaim_empire':'napoleonic_wars.3',
      'FRA_continental_system_focus':'napoleonic_wars.10',
      'FRA_invade_russia':'napoleonic_wars.16',
      'FRA_return_from_elba':'napoleonic_collapse.8',
    }
    for fid,eid in transition_calls.items():
        _strip_direct_event(focuses[fid],eid)

    # Italy/Egypt only unlock their campaign mechanics; completion comes from decisions.
    for key in ('FRA_italian_campaign','FRA_egyptian_expedition'):
        _strip_direct_key(focuses[key],'set_country_flag')
    _append_reward(focuses['FRA_italian_campaign'],'set_country_flag = nap_fra_italian_decisions_unlocked')
    _append_reward(focuses['FRA_egyptian_expedition'],'set_country_flag = nap_fra_egyptian_decisions_unlocked')
    _append_reward(focuses['FRA_reign_of_terror_focus'],'set_country_flag = nap_fra_terror_decisions_unlocked')
    _append_reward(focuses['FRA_brumaire_coup'],'set_country_flag = nap_fra_brumaire_decisions_unlocked')
    _append_reward(focuses['FRA_proclaim_empire'],'set_country_flag = nap_fra_empire_decisions_unlocked')
    _append_reward(focuses['FRA_continental_system_focus'],'set_country_flag = nap_fra_continental_decisions_unlocked')
    _append_reward(focuses['FRA_invade_russia'],'set_country_flag = nap_fra_russia_decisions_unlocked')
    _append_reward(focuses['FRA_return_from_elba'],'set_country_flag = nap_fra_elba_decisions_unlocked')

    # Iberia no longer auto-declares wars from focus completion.
    _strip_direct_key(focuses['FRA_invade_iberia'],'declare_war_on')
    for reward in focuses['FRA_invade_iberia'].children('completion_reward'):
        reward.value=[e for e in reward.value if e.key!='SPR']
    _append_reward(focuses['FRA_invade_iberia'],'set_country_flag = nap_fra_peninsular_decisions_unlocked')
    updates[focus_path]=dumps(parsed)

    # Revolutionary transition events.
    path='events/01_french_revolution.txt'
    text=outputs.get(path)
    if text is None:text=(root/path).read_text(encoding='utf-8-sig')
    if isinstance(text,bytes):text=text.decode('utf-8-sig')
    parsed,events=_event_map(text)
    _remove_called_event(events['french_revolution.10'],'french_revolution.11')
    _make_triggered_only(events['french_revolution.12'])
    _make_triggered_only(events['french_revolution.14'])
    updates[path]=dumps(parsed)

    # Empire, coronation, Tilsit-style Russian settlement and invasion are decision-triggered.
    path='events/02_napoleonic_wars.txt'
    text=outputs.get(path)
    if text is None:text=(root/path).read_text(encoding='utf-8-sig')
    if isinstance(text,bytes):text=text.decode('utf-8-sig')
    parsed,events=_event_map(text)
    _make_triggered_only(events['napoleonic_wars.3'])
    _remove_called_event(events['napoleonic_wars.3'],'napoleonic_wars.4')
    _make_triggered_only(events['napoleonic_wars.13'])
    _make_triggered_only(events['napoleonic_wars.16'])
    updates[path]=dumps(parsed)

    # Collapse/restoration sequence becomes decision-driven.
    path='events/03_collapse.txt'
    text=outputs.get(path)
    if text is None:text=(root/path).read_text(encoding='utf-8-sig')
    if isinstance(text,bytes):text=text.decode('utf-8-sig')
    parsed,events=_event_map(text)
    for eid in ('napoleonic_collapse.1','napoleonic_collapse.5','napoleonic_collapse.12'):
        _make_triggered_only(events[eid])
    _remove_called_event(events['napoleonic_collapse.5'],'napoleonic_collapse.6')
    _remove_called_event(events['napoleonic_collapse.8'],'napoleonic_collapse.9')
    _remove_called_event(events['napoleonic_collapse.9'],'napoleonic_collapse.10')
    updates[path]=dumps(parsed)

    return updates
