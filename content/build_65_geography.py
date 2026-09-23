"""Approved A07 geographic boundary and overseas abstraction."""
import json
from build_00_contracts import COUNTRIES

EUROPE = "FRA ENG HAB RUS PRU SPR POR TUR SWE DEN POL NET SAR NAP PAP VEN GEN TUS MOD PAR LUC MAL HRE BAV SAX HAN WUR BAD HES MEC HAM BRE LUB TYR SWI RAG MTN WLD ITA BAT HOL WES RHC WAR NOR GER".split()

def build(root):
    data=json.loads((root/'content/geographic_scope.json').read_text())
    meaningful=EUROPE[:]
    for tags in data['meaningful_groups'].values(): meaningful += tags
    meaningful=list(dict.fromkeys(meaningful))
    trigger='nap_geography_meaningful_country = { OR = { '+' '.join('original_tag = '+t for t in meaningful)+' } }\n'
    trigger+='nap_geography_outside_scope_country = { NOT = { nap_geography_meaningful_country = yes } }\n'
    setup=['nap_geography_initialize = {']
    for row in data['colonial_subjects']:
        setup.append(f' {row["overlord"]} = {{ if = {{ limit = {{ exists = yes {row["subject"]} = {{ exists = yes is_subject = no }} }} puppet = {row["subject"]} }} }}')
    setup += [' every_country = { limit = { nap_geography_outside_scope_country = yes } set_country_flag = nap_outside_scope add_ideas = nap_outside_scope_inert }','}']
    ideas='''ideas = { country = {
 nap_outside_scope_inert = {
  picture = generic_disjointed_gov
  allowed = { always = yes }
  removal_cost = -1
  modifier = {
   political_power_factor = -0.90
   research_speed_factor = -0.90
   industrial_capacity_factory = -0.75
   industrial_capacity_dockyard = -0.75
   training_time_factor = 1.00
   conscription_factor = -0.90
  }
 }
} }
'''
    loc='''\ufeffl_english:
 nap_outside_scope_inert:0 "Outside the Campaign Scope"
 nap_outside_scope_inert_desc:0 "This country lies outside the approved detailed campaign scope and is deliberately abstracted. It should not behave like a fully developed 1789 campaign state."
'''
    docs={'meaningful_tags':meaningful,'groups':data['meaningful_groups'],'colonial_subjects':data['colonial_subjects'],'outside_scope_policy':'Countries outside the approved scope receive an abstraction spirit at startup rather than fabricated country content.'}
    return {
      'common/scripted_triggers/nap_geography.txt':trigger,
      'common/scripted_effects/nap_geography.txt':'\n'.join(setup)+'\n',
      'common/ideas/nap_geography.txt':ideas,
      'common/on_actions/nap_geography.txt':'on_actions = { on_startup = { effect = { nap_geography_initialize = yes } } }\n',
      'localisation/english/nap_geography_l_english.yml':loc,
      'docs/geographic-scope.json':json.dumps(docs,indent=2)+'\n',
      'docs/geographic-scope.md':'''# Approved geographic scope (A07)

Europe remains the detailed core theatre. The approved additional meaningful scope is North Africa, the United States and Canada, the colonial Americas required for the principal European empires, and the major Indian polities represented by this mod.

The runtime layer includes these tags in shared era mechanics. Saint-Domingue, New Spain, Brazil and British North America are normal puppet relationships when both overlord and subject exist. Other countries are deliberately marked as outside-scope and receive an abstraction spirit rather than fabricated 1789 campaign depth.

This policy does not guess unverified state IDs. Colonial ownership/state reconstruction still follows the repository rule that map-facing changes require the installed 1.19.x map to be audited before state transfers are added.
'''
    }
