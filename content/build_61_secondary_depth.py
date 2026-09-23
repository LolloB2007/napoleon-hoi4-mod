"""Deep secondary-country focus expansion.

Every secondary country with existing content receives an effective 175-focus
campaign.  Two 19-focus branches are country-specific (38 personalised focuses);
six additional 19-focus branches provide administrative, fiscal, military,
infrastructure, diplomatic and social depth.

The German-principality regional tree is special: its six generic branches are
shared, while Bavaria, Saxony, Hanover, Wurttemberg, Baden, Hesse and
Mecklenburg each receive their own two 19-focus branches.  The file therefore
contains more than 175 definitions, but each playable principality has exactly
175 applicable focuses: 23 baseline + 114 shared depth + 38 tag-specific.
"""
from __future__ import annotations
import json
import re
from pdx import parse,dumps
from build_60_secondary import PROFILES,tag_trigger

PERSONALISED={
 'spain':[('Council of Castile and the Intendants','the Council of Castile and provincial intendants'),('Atlantic Monarchy and Royal Navy','Spain\'s Atlantic monarchy, naval bases and colonial communications')],
 'poland':[('The Reforming Commonwealth','the Sejm, crown administration and Commonwealth reform'),('Crown Army and National Cavalry','the Crown Army, national cavalry and frontier defence')],
 'ottoman':[('Nizam-i Cedid','Selim III\'s New Order and the reformed military establishment'),('Provincial Notables and the Porte','the Porte, provincial notables and imperial taxation')],
 'sweden':[('The Gustavian State','the Gustavian monarchy, Riksdag and royal administration'),('Finnish and Baltic Defence','Finland, the Baltic approaches and Swedish coastal defence')],
 'sardinia':[('The Savoyard State','Savoyard administration, Piedmont and the island kingdom'),('Alpine Army and Fortresses','the Alpine army, frontier fortresses and mountain logistics')],
 'naples':[('The Bourbon Court and Reformers','the Bourbon court, Neapolitan reformers and provincial government'),('Mediterranean Defence','the Neapolitan fleet, coastal fortresses and southern military establishment')],
 'papal':[('Temporal Government of the Papal States','the temporal administration, legations and provincial government'),('Curia, Reform and Public Order','the Roman Curia, reforming officials and public order')],
 'venice':[('The Patrician Republic','the Great Council, patrician government and mainland administration'),('The Arsenal and Adriatic Commerce','the Venetian Arsenal, Adriatic fleet and maritime commerce')],
 'tuscany':[('The Leopoldine State','Leopoldine legal reform, administration and civic government'),('Agriculture and Public Works','Tuscan agriculture, drainage, roads and public works')],
 'portugal':[('The Pombaline State','Pombaline institutions, royal administration and Lisbon finance'),('Atlantic Empire and the Tagus','the Tagus defences, Atlantic trade and imperial communications')],
 'netherlands':[('States General and Provincial Estates','the States General, provincial estates and federal government'),('Amsterdam Credit and Maritime Trade','Amsterdam credit, merchant shipping and Dutch maritime commerce')],
 'usa':[('The Federal Institutions','the presidency, Congress, Treasury and the new federal departments'),('Frontier Republic and Neutral Commerce','the western frontier, militia system and neutral Atlantic commerce')],
}

GERMAN_PERSONALISED={
 'BAV':[('The Bavarian Electorate','Bavarian central administration and the Munich court'),('Bavarian Army and Isar Defence','the Bavarian army, arsenals and Isar approaches')],
 'SAX':[('The Saxon Electorate','Saxon estates, Dresden administration and crown finances'),('Saxon Army and Manufactures','Saxon military reform, artillery and manufacturing towns')],
 'HAN':[('Hanover and the British Connection','Hanoverian administration and the personal union with Britain'),('Hanoverian Army and North German Defence','the Hanoverian army, cavalry and North German defence')],
 'WUR':[('Wurttemberg State Reform','Wurttemberg estates, Stuttgart administration and ducal reform'),('Wurttemberg Army and Swabian Defence','the Wurttemberg army and Swabian military organization')],
 'BAD':[('Badenese State Reform','Baden administration, Karlsruhe reform and territorial consolidation'),('Baden Army and Upper Rhine Defence','Baden contingents and Upper Rhine defence')],
 'HES':[('The Hessian Fiscal State','Hessian estates, Kassel administration and subsidy finance'),('Hessian Army and Subsidy Tradition','the Hessian army, officer corps and subsidy tradition')],
 'MEC':[('Mecklenburg Estates and Ducal Government','Mecklenburg estates and ducal administration'),('Mecklenburg Army and Baltic Defence','Mecklenburg contingents and Baltic coastal defence')],
}

GENERIC=[
 ('administration','State Administration'),
 ('finance','Revenue and Public Credit'),
 ('military','Army Reform'),
 ('infrastructure','Infrastructure and Supply'),
 ('diplomacy','Foreign Policy'),
 ('society','Social and Institutional Settlement'),
]

STAGES=[
 'Survey {s}','Map the Existing {s} Institutions','Hear the Provincial Reports on {s}',
 'Define a Reform Mandate for {s}','Secure the First Appropriation for {s}',
 'Train a Permanent {s} Cadre','Publish {s} Regulations','Coordinate Local {s} Practice',
 'Inspect {s} Performance','Correct the First {s} Failures','Expand {s} Capacity',
 'Debate the Burden of {s}','Protect Essential {s} Functions','Standardize {s} Records',
 'Create a National {s} Board','Review the Cost of {s}','Prepare the Next {s} Programme',
 'Audit the {s} Settlement','Institutionalize {s}',
]

def slug(text):
    return re.sub('[^a-z0-9]+','_',text.lower()).strip('_')

def focus_id(profile,branch_title,index,personal_tag=None):
    extra=f'_{personal_tag}' if personal_tag else ''
    return f'NAP_{profile["slug"].upper()}{extra}_DEPTH_{slug(branch_title)}_{index+1:02d}'

def reward(kind,index):
    if kind=='military': return 'army_experience = 4 add_war_support = 0.002'
    if kind=='infrastructure': return 'add_political_power = 4'
    if kind=='finance': return 'add_political_power = 5'
    if kind=='diplomacy': return 'add_political_power = 6'
    if kind=='society': return 'add_stability = 0.003'
    if kind=='personalised': return 'add_political_power = 5'
    return 'add_political_power = 4'

def generated(profile):
    items=[];meta=[]
    settlement=f'NAP_{profile["slug"].upper()}_SETTLEMENT'

    def emit_branch(kind,title,subject,bx,by,available,anchor,personal_tag=None):
        previous=anchor
        for i,template in enumerate(STAGES):
            identifier=focus_id(profile,title,i,personal_tag)
            label=template.format(s=subject)
            cost=(2,3,4,5,3,4,5)[i%7]
            final=' add_stability = 0.01' if i==18 else ''
            visibility=f' allow_branch = {{ tag = {personal_tag} }}' if personal_tag and i==0 else ''
            text=f'''focus = {{
 id = {identifier}
 icon = GFX_focus_generic_treaty
 x = {bx} y = {by+i}
 cost = {cost}
 prerequisite = {{ focus = {previous} }}
{visibility}
 available = {{ {available} }}
 completion_reward = {{ {reward(kind,i)}{final} }}
 ai_will_do = {{ factor = 1 }}
}}'''
            items.append((text,identifier,label,kind,title))
            meta.append({'id':identifier,'slug':profile['slug'],'branch':title,'kind':kind,'personalised':kind=='personalised','personalised_tag':personal_tag,'days':cost*7})
            previous=identifier
        return previous

    # Six common depth branches = 114 focuses.
    previous_by_chain=[None,None,None,None]
    for bi,(kind,title) in enumerate(GENERIC):
        branch_title=f'{profile["name"]}: {title}'
        subject=f'{profile["name"]} {title.lower()}'
        chain=bi%4;tier=bi//4
        anchor=previous_by_chain[chain] or settlement
        previous_by_chain[chain]=emit_branch(kind,branch_title,subject,26+chain*12,10+tier*24,tag_trigger(profile['tags']),anchor)

    if profile['slug']=='german_princes':
        # Seven distinct principalities each get two 19-focus branches.
        for ti,tag in enumerate(profile['tags']):
            first_end=None
            for bi,(title,subject) in enumerate(GERMAN_PERSONALISED[tag]):
                anchor=first_end or settlement
                first_end=emit_branch('personalised',title,subject,110+ti*14,10+bi*24,f'tag = {tag}',anchor,tag)
    else:
        first_end=None
        for bi,(title,subject) in enumerate(PERSONALISED[profile['slug']]):
            anchor=first_end or settlement
            first_end=emit_branch('personalised',title,subject,110,10+bi*24,tag_trigger(profile['tags']),anchor)
    return items,meta

def build(root):
    loc=['\ufeffl_english:'];index=[]
    for profile in PROFILES:
        items,meta=generated(profile);index.extend(meta)
        for _,identifier,label,kind,title in items:
            loc += [f' {identifier}:0 "{label}"',f' {identifier}_desc:0 "This focus develops {title.lower()} within the {profile["name"]} campaign. It is part of the deep campaign expansion and remains subject to the mod\'s bounded territorial rules."']
    summary=[]
    for profile in PROFILES:
        rows=[x for x in index if x['slug']==profile['slug']]
        if profile['slug']=='german_princes':
            summary.append({
              'slug':profile['slug'],'name':profile['name'],'existing_focuses':23,
              'shared_new_focuses':sum(1 for x in rows if not x['personalised']),
              'personalised_focuses_per_tag':38,
              'effective_total_focuses_per_tag':{tag:175 for tag in profile['tags']},
              'raw_tree_definitions':23+len(rows),
            })
        else:
            summary.append({'slug':profile['slug'],'name':profile['name'],'existing_focuses':23,'new_focuses':len(rows),'personalised_focuses':sum(1 for x in rows if x['personalised']),'total_focuses':23+len(rows)})
    return {
      'localisation/english/nap_secondary_depth_l_english.yml':'\n'.join(loc)+'\n',
      'docs/secondary-depth-index.json':json.dumps(index,indent=2)+'\n',
      'docs/secondary-depth-summary.json':json.dumps(summary,indent=2)+'\n',
      'docs/secondary-depth-expansion.md':'''# Deep secondary-country expansion

Every secondary country with existing content now has an effective **175-focus campaign**: 23 baseline focuses, 114 shared depth focuses and 38 country-specific focuses.

Spain, Poland/Warsaw, the Ottoman Empire, Sweden, Sardinia-Piedmont, Naples, the Papal States, Venice, Tuscany, Portugal, the Netherlands/Batavian/Holland tags and the United States each receive two dedicated 19-focus branches.

The German-principality regional tree keeps 114 common regional focuses but contains separate 38-focus subsets for Bavaria, Saxony, Hanover, Wurttemberg, Baden, Hesse and Mecklenburg. Each principality therefore sees an effective 175-focus campaign rather than receiving merely regional personalization.

New rewards are deliberately modest and no branch transfers states, creates cores, annexes countries, forces factions or bypasses the territorial registries.
''',
    }

def postprocess(outputs,root):
    result={}
    for profile in PROFILES:
        path=f'common/national_focus/secondary_{profile["slug"]}.txt'
        text=outputs.get(path)
        if text is None:text=(root/path).read_text(encoding='utf-8-sig')
        if isinstance(text,bytes):text=text.decode('utf-8-sig')
        tree=parse(text)
        ft=next(e for e in tree if e.key=='focus_tree')
        for focus_text,_,_,_,_ in generated(profile)[0]:
            ft.value.append(parse(focus_text)[0])
        result[path]=dumps(tree)
    return result
