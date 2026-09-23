"""Complete Milestone 8 with distinct secondary-country campaign packs.

This module intentionally avoids unapproved territorial transfers, new cores and
formable borders. It adds political/military/diplomatic content around the
existing country map and systems.
"""
from __future__ import annotations
import json

DURATIONS = (35, 49, 70, 35, 49)

PROFILES = [
    dict(slug='spain', tags=('SPR',), name='Spain', root='The Bourbon Monarchy at a Crossroads',
         hist='Reform from the Crown', alt='Summon a National Cortes', majors=('FRA','ENG'),
         institutions=['Audit the Royal Councils','Reform Provincial Intendants','Rebuild Public Credit','A More Capable Monarchy'],
         military=['Inspect the Line Regiments','Reorganize the Artillery Train','Restore Naval Stores','A Reformed Spanish Army'],
         hist_steps=['Preserve Bourbon Authority','Floridablanca’s Programme','Protect the Atlantic Monarchy','Contain Revolutionary Contagion','A Reformed Royal State'],
         alt_steps=['Recall the Reforming Grandees','Open the Cortes','Limit Ministerial Absolutism','Guarantee Provincial Representation','A Constitutional Monarchy']),
    dict(slug='poland', tags=('POL','WAR'), name='Polish State', root='Preserve a Polish State',
         hist='The Reforming Commonwealth', alt='The Magnate Compromise', majors=('RUS','PRU'),
         institutions=['Empower the Sejm Committees','Regularize Crown Revenue','Reform the Local Dietines','A Functioning Commonwealth'],
         military=['Expand the Crown Army','Modernize the National Cavalry','Standardize Artillery Parks','An Army for the Commonwealth'],
         hist_steps=['Back the Reforming Deputies','Codify National Representation','Strengthen the Executive','Defend Civic Reform','A Reformed Commonwealth'],
         alt_steps=['Negotiate with the Magnates','Preserve Noble Privilege','Limit Central Demands','Trade Reform for Stability','A Conservative Settlement']),
    dict(slug='ottoman', tags=('TUR',), name='Ottoman Empire', root='The Porte in an Age of Reform',
         hist='Selim’s New Order', alt='Preserve the Old Establishment', majors=('FRA','ENG'),
         institutions=['Survey Provincial Revenue','Reassert the Imperial Treasury','Reform the Arsenal Administration','A Stronger Porte'],
         military=['Study European Drill','Expand the Imperial Artillery','Rebuild the Fleet','A New Military Establishment'],
         hist_steps=['Back the Reforming Sultan','Create New-Model Units','Train New Officers','Protect Reform from Reaction','The Nizam-i Cedid'],
         alt_steps=['Reconcile the Janissaries','Protect Established Privileges','Rely on Provincial Forces','Limit Foreign Methods','The Traditional Military Order']),
    dict(slug='sweden', tags=('SWE',), name='Sweden', root='The Gustavian Realm',
         hist='Preserve Gustavian Royalism', alt='Restore the Power of the Estates', majors=('ENG','RUS'),
         institutions=['Review the Royal Administration','Strengthen Provincial Government','Stabilize Crown Finance','An Efficient Northern State'],
         military=['Reform the Finnish Army','Modernize the Artillery','Restore Baltic Readiness','A Mobile Swedish Army'],
         hist_steps=['Defend the 1772 Settlement','Strengthen the Crown Council','Reward Loyal Officers','Protect Royal Initiative','A Durable Gustavian State'],
         alt_steps=['Recall the Estates','Restore Parliamentary Scrutiny','Balance Crown and Nobility','Protect Constitutional Guarantees','An Estates Constitution']),
    dict(slug='sardinia', tags=('SAR',), name='Sardinia-Piedmont', root='Guard the Alpine Monarchy',
         hist='The Savoyard Military State', alt='Piedmontese Constitutional Reform', majors=('HAB','FRA'),
         institutions=['Audit the Turin Ministries','Strengthen Provincial Intendants','Reform Customs Collection','A Disciplined Savoyard State'],
         military=['Fortify the Alpine Passes','Reform Piedmontese Infantry','Expand the Artillery Train','The Alpine Army'],
         hist_steps=['Back the House of Savoy','Defend the Alpine Frontier','Centralize the Royal Council','Prepare for Continental War','The Savoyard Monarchy Endures'],
         alt_steps=['Consult the Piedmontese Estates','Protect Municipal Liberties','Reform Royal Justice','Guarantee Representative Government','A Chartered Piedmont']),
    dict(slug='naples', tags=('NAP',), name='Kingdom of Naples', root='The Southern Bourbon Kingdom',
         hist='Strengthen the Bourbon Court', alt='A Neapolitan Constitutional Settlement', majors=('HAB','ENG'),
         institutions=['Reform the Neapolitan Ministries','Survey Feudal Obligations','Improve Crown Revenue','A More Capable Southern State'],
         military=['Inspect the Royal Army','Rebuild Coastal Defences','Strengthen the Sicilian Fleet','An Army for the Two Sicilies'],
         hist_steps=['Back the Royal Court','Contain Radical Societies','Reform without Revolution','Protect the Bourbon Connection','A Stronger Bourbon Kingdom'],
         alt_steps=['Call a Reform Commission','Curtail Feudal Privilege','Open Provincial Councils','Guarantee a Charter','A Constitutional Southern Kingdom']),
    dict(slug='papal', tags=('PAP',), name='Papal States', root='Temporal Power in a Revolutionary Age',
         hist='Defend the Temporal State', alt='Reform the Papal Administration', majors=('HAB','FRA'),
         institutions=['Audit the Apostolic Treasury','Reform Provincial Legations','Improve Grain Administration','A More Capable Papal State'],
         military=['Reorganize the Civic Guard','Strengthen Frontier Garrisons','Improve Military Stores','Defence of the Patrimony'],
         hist_steps=['Protect Papal Sovereignty','Rally Conservative Courts','Defend Ecclesiastical Privilege','Contain Revolutionary Clubs','The Temporal State Endures'],
         alt_steps=['Empower Reforming Cardinals','Rationalize Civil Justice','Consult Provincial Elites','Protect Limited Civic Reform','A Reformed Temporal Administration']),
    dict(slug='venice', tags=('VEN',), name='Republic of Venice', root='The Last Years of the Serenissima',
         hist='Preserve the Patrician Republic', alt='Broaden the Venetian Constitution', majors=('HAB','FRA'),
         institutions=['Audit the Magistracies','Reform the Arsenal Accounts','Protect Adriatic Commerce','A Restored Civic Administration'],
         military=['Refit the Arsenal','Reorganize the Schiavoni','Strengthen the Lagoon Defences','The Armed Neutrality of Venice'],
         hist_steps=['Defend the Great Council','Preserve Patrician Government','Maintain Armed Neutrality','Protect the Mainland Possessions','The Serenissima Preserved'],
         alt_steps=['Open the Reform Debate','Broaden Civic Participation','Reform the Mainland Administration','Limit Oligarchic Offices','A Renewed Republic']),
    dict(slug='tuscany', tags=('TUS',), name='Grand Duchy of Tuscany', root='The Leopoldine Experiment',
         hist='Continue Enlightened Reform', alt='Reconcile Crown, Church and Estates', majors=('HAB','FRA'),
         institutions=['Protect the Leopoldine Codes','Reform the Tax Farms','Expand Civil Administration','The Tuscan Reform State'],
         military=['Create a Territorial Militia','Improve the Coastal Watch','Professionalize the Officer Corps','A Defensive Tuscan Army'],
         hist_steps=['Continue Legal Reform','Protect Religious Toleration','Encourage Agricultural Improvement','Strengthen Civil Government','The Enlightened Grand Duchy'],
         alt_steps=['Slow the Reform Tempo','Restore Ecclesiastical Consultation','Protect Traditional Estates','Balance Reform and Custom','A Conservative Tuscan Compact']),
    dict(slug='german_princes', tags=('BAV','SAX','HAN','WUR','BAD','HES','MEC'), name='German Principalities', root='Between Emperor and Great Powers',
         hist='Defend Imperial Liberties', alt='A League of Reforming Princes', majors=('HAB','PRU'),
         institutions=['Reform the Court Chanceries','Standardize Provincial Accounts','Protect Estate Privileges','A Stronger Territorial State'],
         military=['Inspect the Contingents','Standardize Drill','Build Regional Magazines','A Reliable German Army'],
         hist_steps=['Affirm Imperial Law','Guard Dynastic Sovereignty','Coordinate with the Imperial Court','Resist External Absorption','The Old Imperial Balance'],
         alt_steps=['Convene Reforming Ministers','Coordinate Administrative Codes','Plan Joint Defence','Reduce Imperial Friction','A League of Reforming States']),
    dict(slug='portugal', tags=('POR',), name='Portugal', root='The Atlantic Monarchy',
         hist='Preserve the British Connection', alt='An Independent Reform Course', majors=('ENG','FRA'),
         institutions=['Protect Pombaline Institutions','Reform Colonial Accounts','Strengthen the Lisbon Treasury','An Atlantic Administrative State'],
         military=['Reorganize the Line Army','Strengthen the Tagus Defences','Modernize the Royal Navy','A Defensible Portugal'],
         hist_steps=['Renew the Ancient Alliance','Coordinate Maritime Defence','Protect Atlantic Trade','Prepare for Continental Pressure','The Anglo-Portuguese Connection'],
         alt_steps=['Limit Foreign Dependence','Cultivate Neutral Commerce','Reform the Royal Council','Balance the Great Powers','An Independent Portuguese Course']),
    dict(slug='netherlands', tags=('NET','BAT','HOL'), name='The Netherlands', root='A Republic Divided',
         hist='Stabilize the Orangist Order', alt='Revive the Patriot Programme', majors=('PRU','FRA'),
         institutions=['Reform the Provincial Accounts','Protect Amsterdam Credit','Rebuild Federal Coordination','A Functioning Dutch State'],
         military=['Reorganize the States Army','Protect the River Fortresses','Refit the Fleet','Defence of the Low Countries'],
         hist_steps=['Support the Stadtholder','Reconcile the Provinces','Protect Merchant Confidence','Defend the Restored Order','A Stable Orangist Republic'],
         alt_steps=['Recall Patriot Exiles','Reopen Constitutional Debate','Strengthen Representative Bodies','Limit Stadtholder Power','A Patriot Constitutional State']),
    dict(slug='usa', tags=('USA',), name='United States', root='The New Federal Republic',
         hist='Consolidate the Federal Constitution', alt='Guard Republican Decentralization', majors=('ENG','FRA'),
         institutions=['Organize the Federal Departments','Establish Public Credit','Clarify Federal Revenue','A Functioning Federal Government'],
         military=['Organize the War Department','Secure the Frontier Posts','Standardize the Militia System','A Small Professional Army'],
         hist_steps=['Support the Federal Administration','Fund the National Debt','Strengthen Federal Courts','Protect Neutral Commerce','A Durable Federal Republic'],
         alt_steps=['Protect State Authority','Limit the Permanent Establishment','Favor the Agrarian Republic','Resist Central Patronage','A Decentralized Republic']),
]

def tag_trigger(tags):
    return f'tag = {tags[0]}' if len(tags)==1 else 'OR = { '+' '.join(f'tag = {tag}' for tag in tags)+' }'

def allowed_trigger(tags):
    return f'original_tag = {tags[0]}' if len(tags)==1 else 'OR = { '+' '.join(f'original_tag = {tag}' for tag in tags)+' }'

def focus(identifier,x,y,cost,prereq=None,reward='',exclusive=None,available=''):
    parts=[f'focus = {{ id = {identifier} icon = GFX_focus_generic_treaty x = {x} y = {y} cost = {cost}']
    if prereq:parts.append(f' prerequisite = {{ focus = {prereq} }}')
    if exclusive:parts.append(f' mutually_exclusive = {{ focus = {exclusive} }}')
    if available:parts.append(f' available = {{ {available} }}')
    parts.append(f' completion_reward = {{ {reward} }} }}')
    return ''.join(parts)

def build_tree(profile,event_base):
    slug=profile['slug'];prefix='NAP_'+slug.upper()
    modifiers=' '.join(f'modifier = {{ add = 10 tag = {tag} }}' for tag in profile['tags'])
    nodes=[];loc=[]
    def add(fid,title,x,y,cost,**kw):
        nodes.append(focus(fid,x,y,cost,**kw))
        loc.extend([f' {fid}:0 "{title}"',f' {fid}_desc:0 "{title} advances the {profile["name"]} campaign while preserving the bounded territorial rules of the mod."'])
    root=f'{prefix}_ROOT'
    add(root,profile['root'],10,0,5,reward=f'set_country_flag = nap_{slug}_campaign_started add_political_power = 50')
    prev=root
    for i,title in enumerate(profile['institutions'],1):
        fid=f'{prefix}_INST_{i}';reward='add_political_power = 35 add_stability = 0.01'
        if i==4:reward+=f' add_ideas = nap_{slug}_institutions'
        add(fid,title,3,i,DURATIONS[(i-1)%5]//7,prereq=prev,reward=reward);prev=fid
    inst_end=prev;prev=root
    for i,title in enumerate(profile['military'],1):
        fid=f'{prefix}_MIL_{i}';reward='army_experience = 10 add_war_support = 0.01'
        if i==3:reward+=f' country_event = {{ id = nap_secondary.{event_base+3} days = 1 }}'
        if i==4:reward+=f' add_ideas = nap_{slug}_military'
        add(fid,title,7,i,DURATIONS[i%5]//7,prereq=prev,reward=reward);prev=fid
    mil_end=prev;prev=root
    for i,title in enumerate(profile['hist_steps'],1):
        fid=f'{prefix}_HIST_{i}';reward='add_political_power = 30'
        if i==1:reward=f'set_country_flag = nap_{slug}_historical clr_country_flag = nap_{slug}_alternate add_ideas = nap_{slug}_historical_course country_event = {{ id = nap_secondary.{event_base+1} days = 1 }}'
        elif i==3:reward='add_stability = 0.03 add_political_power = 40'
        elif i==5:reward='add_war_support = 0.04 add_political_power = 50'
        add(fid,title,11,i,DURATIONS[(i+1)%5]//7,prereq=prev,reward=reward,exclusive=(f'{prefix}_ALT_1' if i==1 else None));prev=fid
    prev=root
    for i,title in enumerate(profile['alt_steps'],1):
        fid=f'{prefix}_ALT_{i}';reward='add_political_power = 30'
        if i==1:reward=f'set_country_flag = nap_{slug}_alternate clr_country_flag = nap_{slug}_historical add_ideas = nap_{slug}_alternate_course country_event = {{ id = nap_secondary.{event_base+2} days = 1 }}'
        elif i==3:reward='add_stability = 0.02 add_political_power = 50'
        elif i==5:reward='add_stability = 0.04 add_political_power = 40'
        add(fid,title,15,i,DURATIONS[(i+2)%5]//7,prereq=prev,reward=reward,exclusive=(f'{prefix}_HIST_1' if i==1 else None));prev=fid
    prev=root
    for i,title in enumerate(['Define the Foreign Priority','Send the Diplomatic Mission','A Place in the European Balance'],1):
        fid=f'{prefix}_DIP_{i}';reward='add_political_power = 35'
        if i==2:reward+=f' country_event = {{ id = nap_secondary.{event_base+4} days = 1 }}'
        add(fid,title,19,i,DURATIONS[(i+3)%5]//7,prereq=prev,reward=reward);prev=fid
    dip_end=prev;settle=f'{prefix}_SETTLEMENT'
    available=f'OR = {{ has_country_flag = nap_{slug}_historical has_country_flag = nap_{slug}_alternate }}'
    nodes.append(f'focus = {{ id = {settle} icon = GFX_focus_generic_the_council_of_europe x = 10 y = 7 cost = 10 prerequisite = {{ focus = {inst_end} }} prerequisite = {{ focus = {mil_end} }} prerequisite = {{ focus = {dip_end} }} available = {{ {available} }} completion_reward = {{ add_ideas = nap_{slug}_national_settlement add_stability = 0.04 add_political_power = 75 }} }}')
    loc += [f' {settle}:0 "A National Settlement"',f' {settle}_desc:0 "The institutions, armed forces and foreign policy of {profile["name"]} have been brought into a coherent settlement."']
    return f'focus_tree = {{ id = nap_secondary_{slug}_tree country = {{ factor = 0 {modifiers} }} default = no continuous_focus_position = {{ x = 30 y = 1000 }}\n'+chr(10).join(nodes)+'\n}\n',loc

def build_events(profile,event_base):
    slug=profile['slug'];major_a,major_b=profile['majors'];trig=tag_trigger(profile['tags']);events=[];loc=[]
    def ev(num,title,desc,options):
        eid=f'nap_secondary.{num}';body=' '.join(f'option = {{ name = {eid}.{letter} {effect} }}' for letter,effect in options)
        events.append(f'country_event = {{ id = {eid} title = {eid}.t desc = {eid}.d picture = GFX_report_event_generic_assembly is_triggered_only = yes trigger = {{ {trig} }} {body} }}')
        loc.extend([f' {eid}.t:0 "{title}"',f' {eid}.d:0 "{desc}"'])
        names={'a':'Adopt the stronger programme.','b':'Proceed cautiously.','c':'Preserve room for manoeuvre.'}
        loc.extend(f' {eid}.{letter}:0 "{names[letter]}"' for letter,_ in options)
    ev(event_base+1,profile['hist'],f'The historical course for {profile["name"]} still leaves choices about the pace and cost of reform.',[('a','add_political_power = -25 add_stability = 0.03'),('b','add_political_power = 25')])
    ev(event_base+2,profile['alt'],f'The alternate settlement for {profile["name"]} must reconcile reform with institutions that did not vanish merely because a focus was clicked.',[('a','add_political_power = -25 add_stability = 0.02 add_war_support = 0.02'),('b','add_political_power = 30')])
    ev(event_base+3,'The Military Commission',f'Officers of {profile["name"]} disagree over whether scarce resources belong in readiness now or professional reform for later.',[('a','army_experience = 20 add_war_support = 0.02'),('b','army_experience = 10 add_stability = 0.02')])
    ev(event_base+4,'The Foreign Mission',f'{profile["name"]} can lean toward one great power without surrendering its sovereignty or joining a faction automatically.',[('a',f'add_opinion_modifier = {{ target = {major_a} modifier = nap_1789_close_ties }} set_country_flag = nap_{slug}_alignment_{major_a}'),('b',f'add_opinion_modifier = {{ target = {major_b} modifier = nap_1789_close_ties }} set_country_flag = nap_{slug}_alignment_{major_b}'),('c','add_political_power = 35')])
    return '\n'.join(events)+'\n',loc

def build_ideas(profile):
    slug=profile['slug'];allowed=allowed_trigger(profile['tags'])
    rows=[('institutions','generic_research_bonus','political_power_factor = 0.03 stability_factor = 0.03'),('military','generic_army_bonus','army_org_factor = 0.03 experience_gain_army_factor = 0.05'),('historical_course','generic_morale_bonus','stability_factor = 0.04 war_support_factor = 0.02'),('alternate_course','generic_research_bonus','research_speed_factor = 0.03 political_power_factor = 0.03'),('national_settlement','generic_morale_bonus','stability_factor = 0.05 army_org_factor = 0.02 political_power_factor = 0.02')]
    out=[];loc=[]
    for suffix,picture,modifier in rows:
        iid=f'nap_{slug}_{suffix}';out.append(f'{iid} = {{ picture = {picture} allowed = {{ {allowed} }} allowed_civil_war = {{ always = yes }} removal_cost = -1 modifier = {{ {modifier} }} }}')
        loc += [f' {iid}:0 "{profile["name"]}: {suffix.replace("_"," ").title()}"',f' {iid}_desc:0 "A durable institutional effect from the {profile["name"]} campaign."']
    return '\n'.join(out),loc

def build_decisions(profile,event_base):
    slug=profile['slug'];trig=tag_trigger(profile['tags']);base=f'nap_{slug}'
    text=f'''{base}_administrative_review = {{ icon = generic_political_discourse cost = 35 days_re_enable = 180 visible = {{ {trig} has_country_flag = nap_{slug}_campaign_started }} available = {{ has_war = no }} complete_effect = {{ add_political_power = 45 add_stability = 0.01 }} ai_will_do = {{ factor = 1 }} }}
{base}_mobilization_review = {{ icon = generic_political_discourse cost = 40 days_re_enable = 180 visible = {{ {trig} has_country_flag = nap_{slug}_campaign_started }} available = {{ has_war = yes }} complete_effect = {{ army_experience = 12 add_manpower = 10000 add_war_support = 0.02 }} ai_will_do = {{ factor = 1 }} }}
{base}_foreign_mission = {{ icon = generic_political_discourse cost = 25 days_re_enable = 180 visible = {{ {trig} has_country_flag = nap_{slug}_campaign_started }} available = {{ always = yes }} complete_effect = {{ country_event = {{ id = nap_secondary.{event_base+4} days = 1 }} }} ai_will_do = {{ factor = 1 }} }}'''
    loc=[f' {base}_administrative_review:0 "Review the {profile["name"]} Administration"',f' {base}_administrative_review_desc:0 "A periodic domestic review trades political attention for administrative stability."',f' {base}_mobilization_review:0 "Review Wartime Mobilization"',f' {base}_mobilization_review_desc:0 "While at war, examine manpower, readiness and the officer corps without creating territory or bypassing the coalition framework."',f' {base}_foreign_mission:0 "Dispatch a Foreign Mission"',f' {base}_foreign_mission_desc:0 "Reconsider relations with the great powers without automatically entering a faction or war."']
    return text,loc

def build(root):
    output={};events=['add_namespace = nap_secondary'];ideas=['ideas = {',' country = {'];decisions=['nap_secondary_policy = {'];loc=['\ufeffl_english:',' nap_secondary_policy:0 "Secondary-Power Government"',' nap_secondary_policy_desc:0 "Country-specific administrative, military and diplomatic actions for the expanded Napoleonic campaigns."'];registry=[]
    for index,profile in enumerate(PROFILES):
        base=1000+index*10
        tree,l=build_tree(profile,base);output[f'common/national_focus/secondary_{profile["slug"]}.txt']=tree;loc+=l
        ev,l=build_events(profile,base);events.append(ev);loc+=l
        idea,l=build_ideas(profile);ideas.append(idea);loc+=l
        dec,l=build_decisions(profile,base);decisions.append(dec);loc+=l
        registry.append({'slug':profile['slug'],'tags':list(profile['tags']),'name':profile['name'],'focuses':23,'events':4,'decisions':3,'ideas':5,'historical_route':profile['hist'],'alternate_route':profile['alt'],'major_links':list(profile['majors'])})
    ideas += [' }','}'];decisions.append('}')
    output['events/09_secondary_campaigns.txt']='\n'.join(events)
    output['common/ideas/nap_secondary_campaigns.txt']='\n'.join(ideas)+'\n'
    output['common/decisions/nap_secondary_campaigns.txt']='\n'.join(decisions)+'\n'
    output['common/decisions/categories/nap_secondary_campaigns.txt']='nap_secondary_policy = { icon = generic_political_discourse allowed = { always = yes } visible = { OR = { '+' '.join('tag = '+t for p in PROFILES for t in p['tags'])+' } } }\n'
    output['localisation/english/nap_secondary_campaigns_l_english.yml']='\n'.join(loc)+'\n'
    output['docs/secondary-campaigns.json']=json.dumps(registry,indent=2)+'\n'
    output['docs/secondary-campaigns.md']='''# Secondary-country campaigns — Milestone 8 completion

This pack completes the implementation checklist for Spain, Poland / the Duchy of Warsaw, the Ottoman Empire, Sweden, the principal Italian states, represented German principalities, Portugal, the Netherlands and the United States.

Each campaign has a dedicated or regional focus tree, four events, three recurring decisions, five spirits, a military-development branch, a historical route, a bounded alternate route, great-power diplomacy and English localisation. Existing 1789 histories and OOBs remain the starting military layer for the European countries. Dynamic tags (WAR, BAT and HOL) inherit the relevant Polish or Dutch campaign tree when they exist.

No focus, event or decision in this pack transfers a state, adds a core, annexes a country, creates a formable or forces faction membership. Those choices remain behind the territorial/approval registries. Coalition-eligible tags continue to interact with the existing seven-round coalition framework.

The United States receives campaign content without changing the Europe-first geographic policy. Its detailed 1789 territorial reconstruction and overseas balance remain part of approval A07 rather than being silently inferred here.

Implementation-complete does not mean runtime-certified. Tree rendering, AI pacing, dynamic-tag inheritance, decision visibility and the interaction of these campaigns with real HOI4 diplomacy still require a fresh in-game test.
'''
    output['history/countries/USA - United States.txt']='''# United States — 1789 political baseline. Territorial reconstruction is A07.
capital = 358
set_research_slots = 3
set_stability = 0.75
set_war_support = 0.20
set_convoys = 80
set_technology = { musket_research_1 = 1 bayonet_drill = 1 cavalry_research_1 = 1 artillery_research_1 = 1 support_research_1 = 1 courier_corps_1 = 1 frigate_1 = 1 sloop_1 = 1 }
set_politics = { ruling_party = democratic last_election = "1789.1.7" election_frequency = 48 elections_allowed = yes }
set_popularities = { democratic = 80 neutrality = 15 communism = 3 fascism = 2 }
set_country_flag = american_federal_republic
create_country_leader = { name = "George Washington" ideology = conservatism traits = { popular_figurehead } }
create_corps_commander = { name = "Anthony Wayne" skill = 3 attack_skill = 4 defense_skill = 2 planning_skill = 3 logistics_skill = 3 }
'''
    for filename,capital,ruler,label in [('BAD - Baden.txt',978,'Charles Frederick','Baden'),('HES - Hesse.txt',55,'William IX','Hesse-Kassel'),('MEC - Mecklenburg.txt',61,'Frederick Francis I','Mecklenburg-Schwerin')]:
        output['history/countries/'+filename]=f'''# {label} — 1789 baseline for the shared German-principality campaign.
capital = {capital}
set_research_slots = 2
set_stability = 0.65
set_war_support = 0.20
set_convoys = 5
set_technology = {{ musket_research_1 = 1 bayonet_drill = 1 cavalry_research_1 = 1 artillery_research_1 = 1 support_research_1 = 1 courier_corps_1 = 1 }}
set_politics = {{ ruling_party = neutrality election_frequency = 0 elections_allowed = no }}
set_popularities = {{ neutrality = 86 democratic = 10 communism = 2 fascism = 2 }}
set_country_flag = hre_member_1789
create_country_leader = {{ name = "{ruler}" ideology = despotism }}
'''
    return output

def postprocess(outputs,root):
    suggestions=outputs.get('suggestions.md','')
    addition='''

## Secondary-campaign follow-up ideas

- Replace the reusable four-event policy skeleton with bespoke multi-event crisis chains once in-game pacing is measured.
- Add dynamic transition events for WAR, BAT and HOL so their inherited Polish/Dutch campaigns acknowledge the regime change explicitly.
- Give the represented German principalities differentiated diplomacy panels after the shared regional campaign proves stable in play.
- Reconstruct the United States' 1789 territorial and military map only after geographic-scope decision A07 is answered.
'''
    if '## Secondary-campaign follow-up ideas' not in suggestions:suggestions+=addition
    return {'suggestions.md':suggestions}
