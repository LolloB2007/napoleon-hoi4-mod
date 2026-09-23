"""Deep great-power focus expansion.

Adds 324 focuses to each of Britain, Austria, Prussia and Russia as three
long-running chains of twelve country-specific nine-focus programmes.  These
branches sit on top of the existing trees and programme pack; they do not create
new territorial awards or political routes.
"""
from __future__ import annotations
import json
import re
from pdx import Entry,parse,dumps

THEMES = {
 'ENG': """Public Credit and the Funded Debt|Bank of England Coordination|Customs and Excise Reform|Parliamentary Management|Irish Administration|The Scottish Highlands|East India Company Oversight|West Indian Administration|British North America|Mediterranean Stations|Channel Defence|Royal Dockyards|The Victualling Board|Officer Patronage|Naval Intelligence|Convoy Insurance|Militia and Volunteers|The Ordnance Board|The Army Purchase System|Expeditionary Logistics|Coalition Subsidies|Continental Intelligence|Relations with Austria|Relations with Prussia|Relations with Russia|Iberian Strategy|The Low Countries|Anti-Smuggling Enforcement|Industrial Workshops|Textile Exports|National Grain Supply|Radical Societies|Press and Public Opinion|Catholic Relief|The Regency Contingency|The Postwar Settlement""".split('|'),
 'HAB': """The Composite Monarchy|The Hungarian Diet|Bohemian Administration|Austrian Netherlands|Galician Government|Croatian Military Frontier|Transylvanian Estates|Tyrolean Administration|Imperial War Council|Archduke Charles's Reforms|The Artillery Arm|Grenzer Regiments|Cavalry Remounts|Fortress Command|Danube Magazines|Army Staff Colleges|The Hofkriegsrat|Reserve Mobilization|Imperial Finances|Cameral Administration|Tax Compromise|State Manufactures|Danube Commerce|Vienna Credit|Dynastic Diplomacy|The Holy Roman Empire|Relations with Prussia|Relations with Russia|Italian Interests|Balkan Strategy|Belgian Reconciliation|Josephine Reform Legacy|Church and Crown|Noble Service|Police and Censorship|A Federal Habsburg Settlement""".split('|'),
 'PRU': """The General Directory|East Prussian Administration|Silesian Government|West Prussian Integration|Royal Domains|Provincial Estates|Civil Service Examinations|Berlin Finance|Canton Recruitment|Regimental Schools|The Officer Corps|Artillery Reform|Cavalry Tradition|General Staff Practice|Magazine System|Fortress Network|Landwehr Planning|Mobilization Timetables|Agrarian Reform|Estate Obligations|Municipal Reform|Commercial Law|Roads and Canals|War Finance|Relations with Austria|Relations with Russia|Relations with Britain|Polish Policy|German Leadership|Rhine Strategy|The Reform Party|The Conservative Court|Religious Toleration|Education Reform|National Mobilization|The German Settlement""".split('|'),
 'RUS': """Imperial Chancelleries|Provincial Government|Service Nobility|Baltic Administration|Ukrainian Government|New Russia|Caucasus Frontier|Siberian Administration|Guards and Court Regiments|Artillery Parks|Cavalry and Cossacks|Army Inspection|Military Colonies Debate|Long-Distance Magazines|River Transport|General Staff Reform|Fortress Lines|Reserve Recruitment|Imperial Finances|State Credit|Serf Obligations|Commercial Ports|Black Sea Trade|Baltic Trade|Relations with Austria|Relations with Prussia|Relations with Britain|Ottoman Strategy|Polish Policy|Swedish Frontier|Court Factions|Orthodox Church|Education and Academies|Ministerial Reform|Provincial Justice|The European Settlement""".split('|'),
}

BASE_TOTALS={'ENG':44,'HAB':44,'PRU':40,'RUS':42}
ANCHORS={
 'ENG':['ENG_nap_parliament_08','ENG_nap_admiralty_08','ENG_nap_finance_allies_08'],
 'HAB':['HAB_nap_provinces_08','HAB_nap_charles_08','HAB_nap_dynastic_08'],
 'PRU':['PRU_nap_institutions_08','PRU_nap_reform_08','PRU_nap_liberation_08'],
 'RUS':['RUS_nap_court_08','RUS_nap_distance_08','RUS_nap_reformers_08'],
}
PATTERN=[
 (0,0,None),( -3,1,0),(3,1,0),(-3,2,1),(3,2,2),(0,3,(3,4)),
 (-3,4,5),(3,4,5),(0,5,(6,7)),
]

def slug(text):
    return re.sub('[^a-z0-9]+','_',text.lower()).strip('_')

def focus_id(tag,title,index):
    return f'{tag}_deep_{slug(title)}_{index:02d}'

def theme_category(index):
    if index < 8:return 'administration'
    if index < 18:return 'military'
    if index < 24:return 'economy'
    if index < 30:return 'diplomacy'
    return 'society'

def reward(category,index):
    base='nap_era_initialize = yes '
    if category=='military':
        return base+('navy_experience = 4 ' if index%3==0 else 'army_experience = 4 ')+'nap_era_refresh = yes'
    if category=='economy':
        return base+'add_political_power = 6 nap_era_refresh = yes'
    if category=='diplomacy':
        return base+'add_political_power = 8 nap_era_refresh = yes'
    if category=='society':
        return base+'add_stability = 0.005 add_political_power = 4 nap_era_refresh = yes'
    return base+'add_political_power = 5 nap_era_refresh = yes'

def titles(theme):
    return [
      f'Survey {theme}',f'Fund {theme}',f'Negotiate {theme}',f'Professionalize {theme}',
      f'Preserve Local Practice in {theme}',f'The {theme} Review',f'Extend {theme}',
      f'Audit {theme}',f'Institutionalize {theme}',
    ]

def build(root):
    focuses=[];loc=['\ufeffl_english:'];index=[]
    for tag,themes in THEMES.items():
        if len(themes)!=36:raise ValueError(f'{tag}: expected 36 deep programmes')
        chain_last=[None,None,None]
        for pi,theme in enumerate(themes):
            chain=pi%3;level=pi//3;category=theme_category(pi)
            anchor=chain_last[chain] or ANCHORS[tag][chain]
            names=titles(theme)
            ids=[focus_id(tag,theme,i) for i in range(9)]
            bx=110+chain*18;by=12+level*8
            for i,name in enumerate(names):
                ox,oy,parent=PATTERN[i]
                if i==0:
                    prereqs=[anchor]
                elif isinstance(parent,tuple):
                    prereqs=[ids[p] for p in parent]
                else:
                    prereqs=[ids[parent]]
                pre='prerequisite = { '+' '.join('focus = '+p for p in prereqs)+' }'
                exclusive=''
                if i==1: exclusive=f'mutually_exclusive = {{ focus = {ids[2]} }}'
                if i==2: exclusive=f'mutually_exclusive = {{ focus = {ids[1]} }}'
                final=(' set_country_flag = '+ids[i]+'_complete' if i==8 else '')
                focuses.append(f'''shared_focus = {{
 id = {ids[i]}
 icon = GFX_goal_generic_political_pressure
 x = {bx+ox} y = {by+oy}
 cost = {2+(i%5)}
 {pre}
 {exclusive}
 available = {{ tag = {tag} is_subject = no }}
 cancel_if_invalid = yes
 completion_reward = {{ {reward(category,i)}{final} }}
 ai_will_do = {{ factor = 1 }}
}}''')
                loc += [f' {ids[i]}:0 "{name}"',f' {ids[i]}_desc:0 "{name} develops the {theme.lower()} programme as part of {tag} state-building. The branch is deliberately incremental and does not create territorial awards."']
                index.append({'id':ids[i],'tag':tag,'programme':theme,'category':category,'days':(2+(i%5))*7,'chain':chain,'level':level})
            chain_last[chain]=ids[-1]
    docs={
      'generated_focuses':len(index),
      'per_major':{tag:sum(1 for x in index if x['tag']==tag) for tag in THEMES},
      'estimated_total_focuses':{tag:BASE_TOTALS[tag]+324 for tag in THEMES},
      'themes':THEMES,
    }
    return {
      'common/national_focus/nap_major_deep_programmes.txt':'\n\n'.join(focuses)+'\n',
      'localisation/english/nap_major_deep_l_english.yml':'\n'.join(loc)+'\n',
      'docs/major-deep-focus-index.json':json.dumps(index,indent=2)+'\n',
      'docs/major-deep-expansion.md':'''# Deep great-power focus expansion

Britain, Austria, Prussia and Russia each receive **324 additional focuses**, arranged as three long-running chains of twelve nine-focus country-specific programmes.

Combined with the retained and existing programme trees, the resulting approximate totals are:
- Britain: **368**
- Habsburg Austria: **368**
- Prussia: **364**
- Russia: **366**

The branches cover administration, armed forces, finance, diplomacy and domestic politics using country-specific institutions and strategic problems. Rewards are deliberately modest because the purpose is campaign depth rather than 300 stacked permanent buffs. These branches do not transfer states, add cores, annex countries or create new political routes.
''',
    }

def postprocess(outputs,root):
    result={}
    for tag,themes in THEMES.items():
        path=f'common/national_focus/{tag}.txt'
        text=outputs.get(path)
        if text is None:
            text=(root/path).read_text(encoding='utf-8-sig')
        if isinstance(text,bytes):text=text.decode('utf-8-sig')
        tree=parse(text)
        ft=next(e for e in tree if e.key=='focus_tree')
        existing={str(e.value) for e in ft.children('shared_focus')}
        for theme in themes:
            root_id=focus_id(tag,theme,0)
            if root_id not in existing:
                ft.value.append(Entry('shared_focus',root_id))
        result[path]=dumps(tree)
    return result
