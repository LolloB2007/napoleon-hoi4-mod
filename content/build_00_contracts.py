"""Country namespace restored from the uploaded mod; artwork remains placeholder."""
import re
import struct

COUNTRIES = '''FRA|France|France|49 99 180
ENG|Great_Britain|Great Britain|180 49 49
HAB|Habsburg_Austria|Habsburg Monarchy|220 200 80
RUS|Russian_Empire|Russian Empire|45 110 65
PRU|Prussia|Prussia|60 60 70
SPR|Spain|Spain|200 60 60
POR|Portugal|Portugal|60 130 70
TUR|Ottoman_Empire|Ottoman Empire|150 40 60
SWE|Sweden|Sweden|80 130 200
DEN|Denmark_Norway|Denmark-Norway|180 70 80
POL|Poland_Lithuania|Polish-Lithuanian Commonwealth|180 80 90
NET|Dutch_Republic|Dutch Republic|200 130 60
SAR|Sardinia_Piedmont|Sardinia-Piedmont|70 70 140
NAP|Naples|Kingdom of Naples|220 220 200
PAP|Papal_States|Papal States|240 220 160
VEN|Venice|Republic of Venice|180 50 70
GEN|Genoa|Republic of Genoa|180 180 180
TUS|Tuscany|Grand Duchy of Tuscany|220 200 130
MOD|Modena|Duchy of Modena|140 90 80
PAR|Parma|Duchy of Parma|100 110 140
LUC|Lucca|Republic of Lucca|180 180 200
MAL|Malta|Order of Malta|220 220 220
HRE|Holy_Roman_Empire|Holy Roman Empire|180 160 60
BAV|Bavaria|Electorate of Bavaria|110 150 220
SAX|Saxony|Electorate of Saxony|150 200 150
HAN|Hanover|Electorate of Hanover|220 180 70
WUR|Wurttemberg|Duchy of Wurttemberg|160 70 70
BAD|Baden|Baden|220 140 70
HES|Hesse|Hesse|150 90 140
MEC|Mecklenburg|Mecklenburg|140 140 180
HAM|Hamburg|Hamburg|180 180 180
BRE|Bremen|Bremen|170 170 170
LUB|Lubeck|Lubeck|160 160 170
TYR|Tyrol|Tyrol|180 150 110
SWI|Switzerland|Swiss Confederacy|200 60 60
RAG|Ragusa|Republic of Ragusa|200 180 180
MTN|Montenegro|Montenegro|130 130 160
MOR|Morocco|Morocco|150 50 50
TUN|Tunis|Tunis|140 140 90
ALG|Algiers|Algiers|130 110 80
TRP|Tripoli|Tripoli|160 140 90
EGY|Egypt|Egypt|180 180 110
ETH|Ethiopia|Ethiopia|110 130 90
PRS|Persia|Persia|180 130 60
QIN|Qing_China|Qing Empire|220 180 60
JAP|Japan|Tokugawa Japan|220 180 180
KOR|Korea|Joseon Korea|200 200 180
SIA|Siam|Siam|200 150 100
BUR|Burma|Burma|140 110 70
VIE|Vietnam|Vietnam|150 80 100
MUG|Mughal_India|Mughal Empire|130 150 100
MYS|Mysore|Mysore|180 130 110
MAR|Maratha|Maratha Confederacy|200 130 130
HYD|Hyderabad|Hyderabad|180 150 130
SIK|Sikh_Empire|Sikh Confederacy|180 140 80
USA|United_States|United States|80 110 180
MEX|Mexico|New Spain|140 180 110
BRA|Brazil|Brazil|110 160 100
HAI|Haiti|Saint-Domingue|140 100 140
WLD|Wilderness|Wilderness|120 120 110
ITA|Italy|Kingdom of Italy|130 180 130
BAT|Batavian_Republic|Batavian Republic|220 140 70
HOL|Kingdom_of_Holland|Kingdom of Holland|220 150 80
WES|Westphalia|Kingdom of Westphalia|160 160 200
RHC|Confederation_of_the_Rhine|Confederation of the Rhine|180 180 140
WAR|Duchy_of_Warsaw|Duchy of Warsaw|200 100 110
NOR|Norway|Norway|150 180 220
GER|German_Confederation|German Confederation|140 140 160'''

IDEOLOGIES = {
    'neutrality': ('Absolutism', ['despotism','oligarchism','moderatism','centrism'], '100 30 30'),
    'democratic': ('Constitutionalism', ['conservatism','liberalism','socialism','social_democracy'], '40 90 170'),
    'communism': ('Republicanism', ['marxism','leninism','stalinism','anti_revisionism'], '140 30 30'),
    'fascism': ('Bonapartism', ['fascism_ideology','nazism','falangism','rexism'], '100 100 100'),
}
TRAITS = {
    'silver_tongued': 'political_power_factor = 0.10',
    'the_cloak_n_dagger_schemer': 'political_power_factor = 0.05 stability_factor = 0.05',
    'indecisive_leader': 'political_power_factor = -0.10 stability_factor = -0.05',
    'incorruptible': 'stability_factor = -0.05 war_support_factor = 0.10',
    'military_genius': 'army_org_factor = 0.05 army_morale_factor = 0.05 army_attack_factor = 0.05',
    'reformer': 'stability_factor = 0.05 research_speed_factor = 0.05',
    'weak_willed': 'political_power_factor = -0.10',
    'paranoia': 'stability_factor = -0.10 political_power_factor = -0.05',
}


def tga(width, height, rgb):
    header = struct.pack('<BBBHHBHHHHBB', 0,0,2,0,0,0,0,0,width,height,24,0)
    pixel = bytes(reversed(rgb))
    return header + pixel * width * height


def build(root):
    outputs, tags = {}, []
    names = ['\ufeffl_english:']
    for row in COUNTRIES.splitlines():
        tag, filename, name, colour = row.split('|')
        tags.append(f'{tag} = "countries/{filename}.txt"')
        outputs[f'common/countries/{filename}.txt'] = f'graphical_culture = western_european_gfx\ngraphical_culture_2d = western_european_2d\ncolor = {{ {colour} }}\n'
        for suffix in ('','_DEF','_ADJ','_neutrality','_democratic','_communism','_fascism'):
            names.append(f' {tag}{suffix}:0 "{name}"')
        for directory, width, height in (('',82,52),('medium/',41,26),('small/',10,7)):
            outputs[f'gfx/flags/{directory}{tag}.tga'] = tga(width,height,tuple(map(int,colour.split())))
    outputs['common/country_tags/00_napoleonic_countries.txt'] = '# Restored namespace. See docs/source-contracts.md for vanilla-tag collision risks.\n' + '\n'.join(tags) + '\n'
    outputs['localisation/english/replace/nap_countries_l_english.yml'] = '\n'.join(names) + '\n'
    ideology = ['ideologies = {']
    loc = ['\ufeffl_english:']
    for slot, (name, subtypes, colour) in IDEOLOGIES.items():
        ideology += [f' {slot} = {{', '  types = {']
        ideology += [f'   {subtype} = {{ can_be_randomly_selected = yes }}' for subtype in subtypes]
        ideology += ['  }', f'  color = {{ {colour} }}', '  rules = { can_puppet = yes can_send_volunteers = yes can_lower_tension = yes }', '  can_be_boosted = yes', '  war_impact_on_world_tension = 1.0', '  faction_impact_on_world_tension = 1.0', ' }']
        loc.append(f' {slot}:0 "{name}"')
        loc.append(f' {slot}_desc:0 "Political alignment used by the Napoleonic campaign."')
    ideology.append('}')
    outputs['common/ideologies/00_ideologies.txt'] = '\n'.join(ideology) + '\n'
    outputs['localisation/english/replace/nap_ideology_slots_l_english.yml'] = '\n'.join(loc) + '\n'
    outputs['common/country_leader/napoleonic_leader_traits.txt'] = 'leader_traits = {\n' + '\n'.join(f' {key} = {{ {value} }}' for key,value in TRAITS.items()) + '\n}\n'
    outputs['gfx/interface/select_date_napoleonic.tga'] = tga(384,152,(49,99,180))
    outputs['interface/napoleonic_bookmark.gfx'] = 'spriteTypes = { spriteType = { name = "GFX_select_date_napoleonic" texturefile = "gfx/interface/select_date_napoleonic.tga" } }\n'
    return outputs
