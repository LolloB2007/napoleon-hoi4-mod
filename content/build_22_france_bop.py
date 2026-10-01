"""France: Napoleon versus institutions / marshalate balance of power.

The same bar persists through the Bonapartist regime. Napoleon is always the
left side (negative values). The right side begins as the post-revolutionary
assemblies and changes to the marshalate once the Marshals of the Empire are
created. Restoration removes the BoP; the Hundred Days restores it against the
marshalate.
"""
from __future__ import annotations
from pdx import parse

BOP_ID = 'nap_fra_personal_rule'
NAPOLEON = 'nap_fra_bop_napoleon'
ASSEMBLIES = 'nap_fra_bop_assemblies'
MARSHALS = 'nap_fra_bop_marshals'
CATEGORY = 'nap_fra_personal_rule_decisions'


def build(root):
    bop = f'''{BOP_ID} = {{
 initial_value = -0.05
 left_side = {NAPOLEON}
 right_side = {ASSEMBLIES}
 decision_category = {CATEGORY}

 range = {{
  id = nap_fra_bop_equilibrium
  min = -0.2
  max = 0.2
  modifier = {{
   stability_factor = 0.05
   political_power_factor = 0.03
   supply_consumption_factor = -0.03
  }}
 }}

 side = {{
  id = {NAPOLEON}
  icon = GFX_goal_generic_political_pressure
  range = {{
   id = nap_fra_bop_napoleon_supremacy
   min = -1
   max = -0.6
   modifier = {{
    political_power_factor = 0.15
    army_attack_factor = 0.05
    planning_speed = 0.10
    war_support_factor = 0.05
    supply_consumption_factor = 0.08
    stability_factor = -0.03
   }}
  }}
  range = {{
   id = nap_fra_bop_napoleon_ascendant
   min = -0.6
   max = -0.2
   modifier = {{
    political_power_factor = 0.08
    army_attack_factor = 0.03
    planning_speed = 0.05
    supply_consumption_factor = 0.03
   }}
  }}
 }}

 side = {{
  id = {ASSEMBLIES}
  icon = GFX_goal_generic_self_management
  range = {{
   id = nap_fra_bop_assemblies_influential
   min = 0.2
   max = 0.6
   modifier = {{
    stability_factor = 0.06
    political_power_factor = -0.05
    research_speed_factor = 0.03
    war_support_factor = -0.02
   }}
  }}
  range = {{
   id = nap_fra_bop_assemblies_constrain_napoleon
   min = 0.6
   max = 1
   modifier = {{
    stability_factor = 0.10
    political_power_factor = -0.12
    research_speed_factor = 0.05
    war_support_factor = -0.05
   }}
  }}
 }}

 side = {{
  id = {MARSHALS}
  icon = GFX_goal_generic_army_doctrines
  range = {{
   id = nap_fra_bop_marshals_influential
   min = 0.2
   max = 0.6
   modifier = {{
    army_org_factor = 0.05
    army_morale_factor = 0.03
    planning_speed = 0.05
    supply_consumption_factor = -0.05
    political_power_factor = -0.04
   }}
  }}
  range = {{
   id = nap_fra_bop_marshals_constrain_napoleon
   min = 0.6
   max = 1
   modifier = {{
    army_org_factor = 0.08
    army_morale_factor = 0.05
    planning_speed = 0.05
    supply_consumption_factor = -0.08
    army_attack_factor = -0.05
    political_power_factor = -0.10
   }}
  }}
 }}
}}
'''

    triggers = f'''nap_fra_bop_active = {{
 has_power_balance = {{ id = {BOP_ID} }}
}}

nap_fra_bop_napoleon_supreme = {{
 has_power_balance = {{ id = {BOP_ID} }}
 power_balance_value = {{ id = {BOP_ID} value < -0.59 }}
}}

nap_fra_bop_counterweight_dominant = {{
 has_power_balance = {{ id = {BOP_ID} }}
 power_balance_value = {{ id = {BOP_ID} value > 0.59 }}
}}

nap_fra_bop_marshals_dominant = {{
 has_power_balance = {{ id = {BOP_ID} }}
 is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }}
 power_balance_value = {{ id = {BOP_ID} value > 0.59 }}
}}

nap_fra_bop_can_force_major_campaign = {{
 OR = {{
  NOT = {{ has_power_balance = {{ id = {BOP_ID} }} }}
  AND = {{
   has_power_balance = {{ id = {BOP_ID} }}
   OR = {{
    NOT = {{ is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} }}
    power_balance_value = {{ id = {BOP_ID} value < 0.6 }}
    has_country_flag = nap_fra_bop_override_marshals
    check_variable = {{ nap_fra_napoleon_prestige > 79 }}
   }}
  }}
 }}
}}

nap_fra_bop_marshals_can_force_abdication = {{
 has_power_balance = {{ id = {BOP_ID} }}
 is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }}
 power_balance_value = {{ id = {BOP_ID} value > 0.59 }}
 has_country_flag = empire_of_the_french
 NOT = {{ has_country_flag = napoleon_on_elba }}
 OR = {{
  has_country_flag = grande_armee_destroyed
  check_variable = {{ nap_war_exhaustion > 59 }}
 }}
}}
'''

    effects = f'''nap_fra_bop_refresh = {{
 if = {{
  limit = {{
   tag = FRA
   OR = {{ has_country_flag = napoleon_on_elba has_country_flag = bourbon_restoration }}
   NOT = {{ has_country_flag = hundred_days }}
   has_power_balance = {{ id = {BOP_ID} }}
  }}
  remove_power_balance = {{ id = {BOP_ID} }}
 }}
 if = {{
  limit = {{
   tag = FRA
   has_country_flag = hundred_days
   NOT = {{ has_power_balance = {{ id = {BOP_ID} }} }}
  }}
  set_power_balance = {{
   id = {BOP_ID}
   left_side = {NAPOLEON}
   right_side = {MARSHALS}
   set_value = 0.10
  }}
 }}
 if = {{
  limit = {{
   tag = FRA
   has_country_flag = empire_of_the_french
   NOT = {{ has_country_flag = bourbon_restoration }}
   NOT = {{ has_power_balance = {{ id = {BOP_ID} }} }}
  }}
  set_power_balance = {{
   id = {BOP_ID}
   left_side = {NAPOLEON}
   right_side = {ASSEMBLIES}
   set_value = -0.05
  }}
 }}
 if = {{
  limit = {{
   tag = FRA
   has_country_flag = consulate_established
   NOT = {{ has_country_flag = empire_of_the_french }}
   NOT = {{ has_country_flag = bourbon_restoration }}
   NOT = {{ has_power_balance = {{ id = {BOP_ID} }} }}
  }}
  set_power_balance = {{
   id = {BOP_ID}
   left_side = {NAPOLEON}
   right_side = {ASSEMBLIES}
   set_value = -0.05
  }}
 }}
 if = {{
  limit = {{
   tag = FRA
   has_power_balance = {{ id = {BOP_ID} }}
   has_country_flag = empire_of_the_french
   has_country_flag = nap_fra_marshals_appointed
   is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }}
  }}
  set_power_balance = {{
   id = {BOP_ID}
   left_side = {NAPOLEON}
   right_side = {MARSHALS}
  }}
  if = {{
   limit = {{ NOT = {{ has_country_flag = nap_fra_bop_marshalate_transition }} }}
   set_country_flag = nap_fra_bop_marshalate_transition
   add_power_balance_value = {{ id = {BOP_ID} value = -0.10 tooltip_side = {NAPOLEON} }}
  }}
 }}
}}

nap_fra_bop_monthly = {{
 if = {{ limit = {{ tag = FRA }} nap_fra_bop_refresh = yes }}
 if = {{
  limit = {{ tag = FRA has_power_balance = {{ id = {BOP_ID} }} }}

  if = {{
   limit = {{ check_variable = {{ nap_fra_napoleon_prestige > 69 }} }}
   add_power_balance_value = {{ id = {BOP_ID} value = -0.01 tooltip_side = {NAPOLEON} }}
  }}
  if = {{
   limit = {{ check_variable = {{ nap_fra_napoleon_prestige > 84 }} }}
   add_power_balance_value = {{ id = {BOP_ID} value = -0.01 tooltip_side = {NAPOLEON} }}
  }}
  if = {{
   limit = {{ check_variable = {{ nap_war_exhaustion > 49 }} }}
   add_power_balance_value = {{ id = {BOP_ID} value = 0.01 }}
  }}
  if = {{
   limit = {{ check_variable = {{ nap_war_exhaustion > 74 }} }}
   add_power_balance_value = {{ id = {BOP_ID} value = 0.01 }}
  }}

  if = {{
   limit = {{ has_country_flag = nap_legacy_napoleonic_wars_6_settled NOT = {{ has_country_flag = nap_fra_bop_austerlitz_credit }} }}
   set_country_flag = nap_fra_bop_austerlitz_credit
   add_power_balance_value = {{ id = {BOP_ID} value = -0.12 tooltip_side = {NAPOLEON} }}
  }}
  if = {{
   limit = {{ has_country_flag = nap_legacy_napoleonic_wars_9_settled NOT = {{ has_country_flag = nap_fra_bop_prussia_credit }} }}
   set_country_flag = nap_fra_bop_prussia_credit
   add_power_balance_value = {{ id = {BOP_ID} value = -0.08 tooltip_side = {NAPOLEON} }}
  }}
  if = {{
   limit = {{ has_country_flag = nap_legacy_napoleonic_wars_13_settled NOT = {{ has_country_flag = nap_fra_bop_tilsit_credit }} }}
   set_country_flag = nap_fra_bop_tilsit_credit
   add_power_balance_value = {{ id = {BOP_ID} value = -0.08 tooltip_side = {NAPOLEON} }}
  }}
  if = {{
   limit = {{ has_global_flag = trafalgar_fought NOT = {{ has_country_flag = nap_fra_bop_trafalgar_reaction }} }}
   set_country_flag = nap_fra_bop_trafalgar_reaction
   add_power_balance_value = {{ id = {BOP_ID} value = 0.05 }}
  }}
  if = {{
   limit = {{ has_country_flag = grande_armee_destroyed NOT = {{ has_country_flag = nap_fra_bop_russia_shock }} }}
   set_country_flag = nap_fra_bop_russia_shock
   add_power_balance_value = {{ id = {BOP_ID} value = 0.35 }}
   add_stability = -0.05
   add_to_variable = {{ nap_legitimacy = -4 }}
  }}
  if = {{
   limit = {{ has_global_flag = waterloo_fought NOT = {{ has_country_flag = nap_fra_bop_waterloo_shock }} }}
   set_country_flag = nap_fra_bop_waterloo_shock
   add_power_balance_value = {{ id = {BOP_ID} value = 0.25 }}
  }}

  if = {{
   limit = {{
    has_country_flag = russian_campaign_active
    nap_fra_bop_napoleon_supreme = yes
   }}
   add_to_variable = {{ nap_fra_russian_supply = -4 }}
   add_to_variable = {{ nap_fra_russian_cohesion = -3 }}
   add_to_variable = {{ nap_war_exhaustion = 1 }}
  }}
  if = {{
   limit = {{
    has_country_flag = russian_campaign_active
    is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }}
    power_balance_value = {{ id = {BOP_ID} value > 0.2 }}
   }}
   add_to_variable = {{ nap_fra_russian_supply = 2 }}
   add_to_variable = {{ nap_fra_russian_cohesion = 2 }}
   add_to_variable = {{ nap_fra_napoleon_prestige = -1 }}
  }}

  nap_era_clamp = yes
  nap_fra_decision_clamp = yes
 }}
}}

nap_fra_bop_govern_by_decree_effect = {{
 if = {{
  limit = {{
   tag = FRA
   has_power_balance = {{ id = {BOP_ID} }}
   is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }}
  }}
  add_power_balance_value = {{ id = {BOP_ID} value = -0.08 tooltip_side = {NAPOLEON} }}
  add_to_variable = {{ nap_legitimacy = -3 }}
  add_to_variable = {{ nap_reform = 2 }}
  add_stability = -0.01
  nap_era_clamp = yes
 }}
}}

nap_fra_bop_consult_assemblies_effect = {{
 if = {{
  limit = {{
   tag = FRA
   has_power_balance = {{ id = {BOP_ID} }}
   is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }}
  }}
  add_power_balance_value = {{ id = {BOP_ID} value = 0.08 tooltip_side = {ASSEMBLIES} }}
  add_to_variable = {{ nap_legitimacy = 3 }}
  add_stability = 0.02
  nap_era_clamp = yes
 }}
}}

nap_fra_bop_plebiscite_effect = {{
 if = {{
  limit = {{
   tag = FRA
   has_power_balance = {{ id = {BOP_ID} }}
   is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }}
   power_balance_value = {{ id = {BOP_ID} value > 0.59 }}
   check_variable = {{ nap_fra_napoleon_prestige > 49 }}
  }}
  add_power_balance_value = {{ id = {BOP_ID} value = -0.20 tooltip_side = {NAPOLEON} }}
  add_to_variable = {{ nap_legitimacy = -4 }}
  add_to_variable = {{ nap_fra_napoleon_prestige = 3 }}
  add_stability = -0.03
  nap_era_clamp = yes
  nap_fra_decision_clamp = yes
 }}
}}

nap_fra_bop_centralize_command_effect = {{
 if = {{
  limit = {{
   tag = FRA
   has_power_balance = {{ id = {BOP_ID} }}
   is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }}
  }}
  add_power_balance_value = {{ id = {BOP_ID} value = -0.08 tooltip_side = {NAPOLEON} }}
  add_to_variable = {{ nap_army_prestige = -2 }}
  add_to_variable = {{ nap_fra_napoleon_prestige = 3 }}
  add_command_power = 20
  nap_era_clamp = yes
  nap_fra_decision_clamp = yes
 }}
}}

nap_fra_bop_reward_marshalate_effect = {{
 if = {{
  limit = {{
   tag = FRA
   has_power_balance = {{ id = {BOP_ID} }}
   is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }}
   NOT = {{ check_variable = {{ nap_treasury < 8 }} }}
  }}
  add_power_balance_value = {{ id = {BOP_ID} value = 0.08 tooltip_side = {MARSHALS} }}
  add_to_variable = {{ nap_treasury = -8 }}
  add_to_variable = {{ nap_army_prestige = 4 }}
  add_to_variable = {{ nap_legitimacy = 1 }}
  nap_era_clamp = yes
 }}
}}

nap_fra_bop_delegate_theatres_effect = {{
 if = {{
  limit = {{
   tag = FRA
   has_power_balance = {{ id = {BOP_ID} }}
   is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }}
  }}
  add_power_balance_value = {{ id = {BOP_ID} value = 0.08 tooltip_side = {MARSHALS} }}
  add_to_variable = {{ nap_fra_napoleon_prestige = -2 }}
  add_to_variable = {{ nap_supply_pressure = -3 }}
  army_experience = 10
  nap_era_clamp = yes
  nap_fra_decision_clamp = yes
 }}
}}

nap_fra_bop_override_marshals_effect = {{
 if = {{
  limit = {{
   tag = FRA
   nap_fra_bop_marshals_dominant = yes
   check_variable = {{ nap_fra_napoleon_prestige > 69 }}
  }}
  set_country_flag = {{ flag = nap_fra_bop_override_marshals days = 120 }}
  add_power_balance_value = {{ id = {BOP_ID} value = -0.18 tooltip_side = {NAPOLEON} }}
  add_to_variable = {{ nap_army_prestige = -6 }}
  add_to_variable = {{ nap_legitimacy = -5 }}
  add_to_variable = {{ nap_war_exhaustion = 4 }}
  nap_era_clamp = yes
 }}
}}

nap_fra_bop_marshal_council_effect = {{
 if = {{
  limit = {{
   tag = FRA
   has_power_balance = {{ id = {BOP_ID} }}
   is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }}
   check_variable = {{ nap_war_exhaustion > 39 }}
  }}
  add_power_balance_value = {{ id = {BOP_ID} value = 0.10 tooltip_side = {MARSHALS} }}
  add_to_variable = {{ nap_war_exhaustion = -6 }}
  add_to_variable = {{ nap_supply_pressure = -4 }}
  add_to_variable = {{ nap_fra_napoleon_prestige = -3 }}
  nap_era_clamp = yes
  nap_fra_decision_clamp = yes
 }}
}}

nap_fra_bop_marshals_demand_abdication_effect = {{
 if = {{
  limit = {{ tag = FRA nap_fra_bop_marshals_can_force_abdication = yes }}
  country_event = {{ id = napoleonic_collapse.5 hours = 1 }}
 }}
}}

nap_fra_bop_fight_on_effect = {{
 if = {{
  limit = {{
   tag = FRA
   nap_fra_bop_marshals_can_force_abdication = yes
   check_variable = {{ nap_fra_napoleon_prestige > 59 }}
  }}
  set_country_flag = {{ flag = nap_fra_bop_rejected_abdication days = 180 }}
  add_power_balance_value = {{ id = {BOP_ID} value = -0.25 tooltip_side = {NAPOLEON} }}
  add_manpower = 75000
  add_war_support = 0.10
  add_stability = -0.08
  add_to_variable = {{ nap_legitimacy = -8 }}
  add_to_variable = {{ nap_war_exhaustion = 6 }}
  nap_era_clamp = yes
 }}
}}
'''

    decisions = f'''{CATEGORY} = {{
 nap_fra_bop_govern_by_decree = {{
  icon = generic_political_discourse
  cost = 35
  days_re_enable = 120
  visible = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }} }}
  available = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }} }}
  complete_effect = {{ nap_fra_bop_govern_by_decree_effect = yes }}
  ai_will_do = {{ factor = 1.2 }}
 }}
 nap_fra_bop_consult_assemblies = {{
  icon = generic_political_discourse
  cost = 30
  days_re_enable = 120
  visible = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }} }}
  available = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }} }}
  complete_effect = {{ nap_fra_bop_consult_assemblies_effect = yes }}
  ai_will_do = {{ factor = 1 }}
 }}
 nap_fra_bop_appeal_plebiscite = {{
  icon = generic_political_discourse
  cost = 60
  days_re_enable = 365
  visible = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }} }}
  available = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {ASSEMBLIES} }} power_balance_value = {{ id = {BOP_ID} value > 0.59 }} check_variable = {{ nap_fra_napoleon_prestige > 49 }} }}
  complete_effect = {{ nap_fra_bop_plebiscite_effect = yes }}
  ai_will_do = {{ factor = 1.4 }}
 }}
 nap_fra_bop_centralize_command = {{
  icon = generic_political_discourse
  cost = 35
  days_re_enable = 120
  visible = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} }}
  available = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} }}
  complete_effect = {{ nap_fra_bop_centralize_command_effect = yes }}
  ai_will_do = {{ factor = 1.2 }}
 }}
 nap_fra_bop_reward_marshalate = {{
  icon = generic_political_discourse
  cost = 30
  days_re_enable = 120
  visible = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} }}
  available = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} NOT = {{ check_variable = {{ nap_treasury < 8 }} }} }}
  complete_effect = {{ nap_fra_bop_reward_marshalate_effect = yes }}
  ai_will_do = {{ factor = 1 }}
 }}
 nap_fra_bop_delegate_theatres = {{
  icon = generic_political_discourse
  cost = 35
  days_re_enable = 150
  visible = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} }}
  available = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} }}
  complete_effect = {{ nap_fra_bop_delegate_theatres_effect = yes }}
  ai_will_do = {{ factor = 1 }}
 }}
 nap_fra_bop_override_marshal_veto = {{
  icon = generic_political_discourse
  cost = 55
  days_re_enable = 180
  visible = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} }}
  available = {{ tag = FRA nap_fra_bop_marshals_dominant = yes check_variable = {{ nap_fra_napoleon_prestige > 69 }} NOT = {{ has_country_flag = nap_fra_bop_override_marshals }} }}
  complete_effect = {{ nap_fra_bop_override_marshals_effect = yes }}
  ai_will_do = {{ factor = 1.5 modifier = {{ factor = 2 has_completed_focus = FRA_invade_russia }} }}
 }}
 nap_fra_bop_convene_marshal_council = {{
  icon = generic_political_discourse
  cost = 30
  days_re_enable = 120
  visible = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} }}
  available = {{ tag = FRA is_power_balance_side_active = {{ id = {BOP_ID} side = {MARSHALS} }} check_variable = {{ nap_war_exhaustion > 39 }} }}
  complete_effect = {{ nap_fra_bop_marshal_council_effect = yes }}
  ai_will_do = {{ factor = 1.3 }}
 }}
 nap_fra_bop_marshals_demand_abdication = {{
  icon = generic_political_discourse
  cost = 15
  visible = {{ tag = FRA nap_fra_bop_marshals_dominant = yes }}
  available = {{ tag = FRA nap_fra_bop_marshals_can_force_abdication = yes }}
  complete_effect = {{ nap_fra_bop_marshals_demand_abdication_effect = yes }}
  ai_will_do = {{ factor = 1 }}
  fire_only_once = yes
 }}
 nap_fra_bop_fight_on = {{
  icon = generic_political_discourse
  cost = 50
  visible = {{ tag = FRA nap_fra_bop_marshals_dominant = yes }}
  available = {{ tag = FRA nap_fra_bop_marshals_can_force_abdication = yes check_variable = {{ nap_fra_napoleon_prestige > 59 }} }}
  complete_effect = {{ nap_fra_bop_fight_on_effect = yes }}
  ai_will_do = {{ factor = 0.4 }}
  fire_only_once = yes
 }}
}}
'''

    category = f'''{CATEGORY} = {{
 icon = generic_political_discourse
 allowed = {{ tag = FRA }}
 visible = {{ tag = FRA has_power_balance = {{ id = {BOP_ID} }} }}
}}
'''

    on_actions = '''on_actions = {
 on_startup = {
  effect = {
   every_country = {
    limit = { tag = FRA }
    nap_fra_bop_refresh = yes
   }
  }
 }
 on_monthly = {
  effect = {
   if = {
    limit = { tag = FRA }
    nap_fra_bop_monthly = yes
   }
  }
 }
}
'''

    loc = '''﻿l_english:
 nap_fra_personal_rule:0 "Personal Rule and Its Counterweights"
 nap_fra_personal_rule_desc:0 "Napoleon's regime derives enormous strength from concentrated authority, but France also depends on institutions and commanders capable of restraining disastrous personal rule. The counterweight begins with the representative institutions descended from the Estates-General and changes to the Marshalate after the senior imperial command is created."
 nap_fra_bop_napoleon:0 "Napoleon"
 nap_fra_bop_napoleon_desc:0 "Personal authority, plebiscitary legitimacy and centralized command."
 nap_fra_bop_assemblies:0 "The Assemblies"
 nap_fra_bop_assemblies_desc:0 "The representative and constitutional institutions descended from the Estates-General, including the legislature, Tribunate, Senate and political notables."
 nap_fra_bop_marshals:0 "The Marshalate"
 nap_fra_bop_marshals_desc:0 "The senior military establishment whose prestige, independent judgement and accumulated interests can support or constrain the Emperor."
 nap_fra_bop_equilibrium:0 "Managed Equilibrium"
 nap_fra_bop_equilibrium_desc:0 "Personal authority and institutional restraint remain mutually dependent. France gains stability and administrative resilience without surrendering strategic initiative."
 nap_fra_bop_napoleon_supremacy:0 "The Emperor Commands Alone"
 nap_fra_bop_napoleon_supremacy_desc:0 "Napoleon can act with exceptional speed and offensive concentration, but logistics and political resilience suffer because the state has become dangerously dependent on one man's judgement."
 nap_fra_bop_napoleon_ascendant:0 "Personal Ascendancy"
 nap_fra_bop_napoleon_ascendant_desc:0 "Napoleon clearly dominates the regime while still receiving some institutional and military feedback."
 nap_fra_bop_assemblies_influential:0 "Legislative Influence"
 nap_fra_bop_assemblies_influential_desc:0 "Representative institutions can restrain executive excess. Policy is slower, but legitimacy, stability and intellectual life benefit."
 nap_fra_bop_assemblies_constrain_napoleon:0 "Napoleon Constrained"
 nap_fra_bop_assemblies_constrain_napoleon_desc:0 "The assemblies can obstruct the First Consul or Emperor. France is politically resilient but the executive struggles to mobilize the state rapidly for war."
 nap_fra_bop_marshals_influential:0 "Marshalate Influence"
 nap_fra_bop_marshals_influential_desc:0 "Senior commanders retain enough independence to improve staff work, supply discipline and army cohesion, though political control becomes less personal."
 nap_fra_bop_marshals_constrain_napoleon:0 "The Marshalate Dictates Strategy"
 nap_fra_bop_marshals_constrain_napoleon_desc:0 "The marshals can resist strategic demands. The army is resilient and professionally managed, but Napoleon cannot freely impose major campaigns without extraordinary prestige or an explicit confrontation."
 nap_fra_personal_rule_decisions:0 "Personal Rule"
 nap_fra_personal_rule_decisions_desc:0 "Actions here change who can say no to Napoleon. Negative movement strengthens Napoleon; positive movement strengthens the currently active counterweight."
 nap_fra_bop_govern_by_decree:0 "Govern by Decree"
 nap_fra_bop_govern_by_decree_desc:0 "Bypass representative resistance and concentrate administration around the First Consul. Reform advances, but legitimacy and stability pay the price."
 nap_fra_bop_consult_assemblies:0 "Consult the Assemblies"
 nap_fra_bop_consult_assemblies_desc:0 "Accept legislative bargaining and institutional scrutiny. It strengthens legitimacy and stability while shifting political weight away from Napoleon."
 nap_fra_bop_appeal_plebiscite:0 "Appeal to the Nation"
 nap_fra_bop_appeal_plebiscite_desc:0 "Use Napoleon's personal prestige to break legislative obstruction through a plebiscitary appeal. It restores executive authority, but weakens constitutional legitimacy."
 nap_fra_bop_centralize_command:0 "Centralize Operational Command"
 nap_fra_bop_centralize_command_desc:0 "Reassert Napoleon's direct control over strategy. Command becomes faster and more personal, but the independent prestige of the Marshalate declines."
 nap_fra_bop_reward_marshalate:0 "Reward the Marshalate"
 nap_fra_bop_reward_marshalate_desc:0 "Titles, money and recognition strengthen the senior command as an institution. The army gains prestige, but the marshals acquire greater political weight."
 nap_fra_bop_delegate_theatres:0 "Delegate Theatre Commands"
 nap_fra_bop_delegate_theatres_desc:0 "Give senior commanders genuine operational autonomy. Staff capacity and supply management improve while Napoleon's personal prestige yields some ground."
 nap_fra_bop_override_marshal_veto:0 "Override the Marshal Council"
 nap_fra_bop_override_marshal_veto_desc:0 "When the Marshalate can veto a major campaign, Napoleon may force the issue for 120 days. The confrontation damages military prestige, legitimacy and war endurance."
 nap_fra_bop_convene_marshal_council:0 "Convene a Marshal Council"
 nap_fra_bop_convene_marshal_council_desc:0 "Let the senior commanders slow the operational tempo and repair an exhausted army. War exhaustion and supply pressure fall, but Napoleon concedes political ground."
 nap_fra_bop_marshals_demand_abdication:0 "The Marshals Demand Abdication"
 nap_fra_bop_marshals_demand_abdication_desc:0 "After military disaster or extreme war exhaustion, a dominant Marshalate can force the Fontainebleau question onto the Emperor."
 nap_fra_bop_fight_on:0 "Dismiss the Marshals and Fight On"
 nap_fra_bop_fight_on_desc:0 "Reject the demand for abdication and mobilize an emergency army. Napoleon recovers personal authority, but legitimacy, stability and exhaustion deteriorate sharply."
'''

    docs = '''# France balance of power: Napoleon and the counterweights

France gains one continuous Balance of Power after Brumaire. Napoleon is always the negative/left side. The positive/right side changes with the regime.

## Consulate and early Empire: Napoleon vs. the Assemblies
The counterweight represents the institutional line descending from the Estates-General through the revolutionary legislatures, Tribunate, Senate and political notables. Napoleon can govern by decree or use plebiscitary prestige to break obstruction; consultation improves legitimacy and stability while slowing concentrated executive action.

## Marshalate transition
Once the Empire exists and the Marshals of the Empire have been created, the right side changes in-place from the Assemblies to the Marshalate. The numerical position is preserved and Napoleon receives a one-time centralizing shift when he creates the new senior command.

## Imperial balance
Napoleonic dominance improves political throughput, attack and planning but worsens supply consumption and, at the extreme, stability. Marshal influence improves organisation, morale, planning and logistics while reducing political throughput. At extreme Marshal influence, major strategic adventures can be vetoed.

A dominant Marshalate can block Crossing the Niemen and Press Deeper into Russia unless Napoleon has prestige above 79 or uses Override the Marshal Council. Napoleon-heavy command also worsens Russian supply and cohesion each month; marshal influence improves both at the cost of personal prestige.

## Historical shocks
Austerlitz, victory over Prussia and a Tilsit-style Russian settlement strengthen Napoleon. Trafalgar shifts authority toward the counterweight. Destruction of the Grande Armée produces a severe one-time shift toward the Marshalate and damages stability/legitimacy. Waterloo produces another major shock.

High Napoleon prestige creates monthly drift toward personal rule. High war exhaustion creates monthly drift toward the active counterweight.

## 1814 and the Hundred Days
If the Marshalate dominates after the Russian disaster or extreme exhaustion, it can explicitly demand abdication. Napoleon may instead dismiss the marshals and fight on, receiving emergency manpower and war support at severe political cost.

Restoration removes the BoP. The Hundred Days recreates it as Napoleon versus the Marshalate with a slight initial marshal advantage.

The range design is deliberately asymmetric rather than good-versus-bad: personal dominance offers a higher offensive ceiling but greater fragility, while institutional/marshal influence sacrifices executive freedom for resilience.
'''

    return {
      'common/bop/nap_france_personal_rule.txt': bop,
      'common/scripted_triggers/nap_france_bop.txt': triggers,
      'common/scripted_effects/nap_france_bop.txt': effects,
      'common/decisions/nap_france_bop.txt': decisions,
      'common/decisions/categories/nap_france_bop.txt': category,
      'common/on_actions/nap_france_bop.txt': on_actions,
      'localisation/english/nap_france_bop_l_english.yml': loc,
      'docs/france-balance-of-power.md': docs,
    }
