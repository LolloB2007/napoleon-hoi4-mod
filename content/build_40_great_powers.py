"""Great-power institutions: branches and country-specific policy dilemmas.
Builds on existing paths rather than inventing dynastic or territorial routes.
"""
import json
from pdx import Entry,parse,dumps,walk
from build_10_era import change

PROGRAMMES=[
('ENG','parliament','Parliament and Public Credit','ENG_pitt_ministry',
 'Examine the Parliamentary Accounts|Strengthen Treasury Supervision|Broaden Committee Scrutiny|Regularize the Sinking Fund|Publish the Revenue Estimates|Debate the War Budget|Inspect Government Contracts|Protect Parliamentary Petitions|A Parliamentary Financial Settlement',
 'Financing a Continental Commitment','Fund a durable financial establishment',{'treasury':-15,'debt':-8,'reform':5},'Preserve immediate political flexibility',{'treasury':-5,'legitimacy':5},'political_power_factor = 0.035'),
('ENG','admiralty','The Admiralty and Maritime Trade','ENG_expand_royal_navy',
 'Survey the Admiralty Stores|Concentrate the Battle Fleet|Protect the Convoy Routes|Prepare the Fleet Anchorage|Expand the Escort Stations|Set the Maritime Priority|Inspect Naval Victualling|Train the Petty Officers|An Admiralty That Sustains Its Fleet',
 'Ships for Battle or Commerce','Fund the concentrated fleet',{'treasury':-18,'army_prestige':7,'war_exhaustion':2},'Prioritize convoy protection',{'treasury':-12,'supply_pressure':-8,'legitimacy':3},'navy_org_factor = 0.04'),
('ENG','finance_allies','Financing the Allies','ENG_subsidies_to_coalitions',
 'Audit the Subsidy Commitments|Tie Payments to Field Armies|Support Allied Recovery|Standardize Military Accounts|Inspect the Allied Treasury Offices|The Subsidy Negotiation|Coordinate the Coalition Couriers|Maintain a Reserve of Public Credit|A Sustainable Subsidy Policy',
 'The Allies Request Another Advance','Expand the financial reserve',{'treasury':20,'debt':25,'legitimacy':-2},'Limit commitments to funded obligations',{'treasury':-8,'debt':-6,'reform':4},'political_power_factor = 0.025'),
('HAB','provinces','The Habsburg Provincial Settlement','HAB_emperor_dying',
 'Hear the Provincial Estates|Pursue Uniform Administration|Negotiate Provincial Compacts|Inspect the Crown Offices|Guarantee Local Consultation|The Estates and the Ministries|Reconcile Provincial Tax Returns|Protect Administrative Continuity|A Workable Composite Monarchy',
 'The Provinces Seek a Settlement','Finance coordinated reform',{'treasury':-14,'reform':7,'legitimacy':-3},'Negotiate gradual provincial cooperation',{'treasury':-10,'legitimacy':6,'reform':2},'stability_factor = 0.035'),
('HAB','charles','Charles and the Field Army','HAB_charles_takes_command',
 'Inspect the Imperial Field Commands|Concentrate the General Staff|Develop Army-Level Initiative|Establish Staff Examinations|Strengthen Liaison Officers|Command in a Composite Army|Standardize Artillery Reporting|Rehearse the Reserve Deployment|A Reformed Imperial Field Army',
 'The Field Command Reform','Pay for a professional staff system',{'treasury':-16,'reform':6,'army_prestige':3},'Prioritize experienced field cadres',{'treasury':-12,'army_prestige':6,'reform':1},'max_planning_factor = 0.04'),
('HAB','dynastic','The Habsburg Diplomatic Network','HAB_suppress_belgian_revolt',
 'Review the Dynastic Commitments|Emphasize Imperial Guarantees|Prioritize Bilateral Diplomacy|Improve the Imperial Courier Service|Consult the Border Courts|The Cost of the Dynastic Network|Audit Diplomatic Subsidies|Keep Channels Open to Rivals|A Defined Habsburg Security Policy',
 'Diplomacy and Military Capacity','Fund diplomatic coordination',{'treasury':-12,'legitimacy':4,'reform':3},'Reserve resources for the frontier',{'treasury':-8,'supply_pressure':-6,'army_prestige':2},'political_power_factor = 0.03'),
('PRU','institutions','Prussian State Institutions','PRU_kingdom_of_drill',
 'Audit the General Directory|Protect Central Discipline|Consult the Provincial Estates|Examine Crown Revenue|Publish Provincial Obligations|The Cost of Administrative Reform|Inspect State Domains|Train Professional Administrators|A State Beyond the Parade Ground',
 'A More Capable Prussian Administration','Centralize professional administration',{'treasury':-14,'reform':6,'legitimacy':-2},'Secure a negotiated reform compact',{'treasury':-10,'reform':3,'legitimacy':4},'political_power_factor = 0.03'),
('PRU','reform','Rebuilding the Prussian Army','PRU_consider_reform',
 'Review the Lessons of Defeat|Expand the Training Reserve|Prioritize the Standing Cadres|Organize Rotating Training Cohorts|Inspect the Regimental Schools|The Army Reform Programme|Open Advancement to Demonstrated Merit|Coordinate the Staff Colleges|An Army Capable of Learning',
 'Cadres or a Wider Training Reserve','Expand a trained reserve',{'treasury':-18,'reform':8,'war_exhaustion':3},'Rebuild the professional cadres first',{'treasury':-12,'army_prestige':5,'reform':3},'army_org_factor = 0.035'),
('PRU','liberation','Mobilization and Liberation','PRU_war_of_liberation',
 'Assess the National Mobilization|Concentrate the Field Establishment|Preserve the Local Reserve|Coordinate the Army Columns|Improve the Provincial Depots|The Burden of Liberation|Protect Civil Supply Contracts|Prepare Postwar Demobilization|A Mobilized State That Can Recover',
 'The Price of Sustained Mobilization','Fund the field establishment',{'treasury':-18,'army_prestige':6,'war_exhaustion':4},'Relieve the mobilized communities',{'treasury':-14,'war_exhaustion':-7,'legitimacy':3},'army_morale_factor = 0.035'),
('RUS','court','Court and Provincial Administration','RUS_empress_in_majesty',
 'Survey the Imperial Provinces|Rely on the Service Nobility|Expand Professional Administration|Audit Provincial Service Records|Train the Civil Chancelleries|The Provinces and the Imperial Court|Inspect State Supply Contracts|Improve Long-Distance Correspondence|An Administration for a Continental Empire',
 'Service, Privilege and Administration','Fund a professional reform programme',{'treasury':-18,'reform':7,'legitimacy':-3},'Negotiate with established provincial institutions',{'treasury':-10,'legitimacy':5,'reform':2},'political_power_factor = 0.03'),
('RUS','distance','Sustaining Distant Armies','RUS_finish_ottoman_war',
 'Survey the Army Magazines|Plan a Concentrated Advance|Prepare for a Long Campaign|Improve the March Tables|Construct Redundant Supply Plans|The Distance Problem|Inspect Horse and Wagon Reserves|Coordinate the Field Hospitals|An Army Supported Across the Distances',
 'Concentration or Strategic Depth','Fund a rapid concentration',{'treasury':-18,'army_prestige':6,'supply_pressure':3},'Invest in magazines and depth',{'treasury':-16,'supply_pressure':-10,'reform':3},'supply_consumption_factor = -0.035'),
('RUS','reformers','The Imperial Reform Debate','RUS_speransky_reforms',
 'Examine the Ministerial System|Pursue a Coherent Reform Plan|Negotiate a Gradual Settlement|Codify Ministerial Responsibilities|Consult the Service Institutions|The Pace of Imperial Reform|Protect the Civil Service Examinations|Review the Costs of Administration|An Imperial Programme with Institutions',
 'The Reformers and Established Interests','Finance institutional restructuring',{'treasury':-20,'reform':9,'legitimacy':-4},'Broaden the reform coalition',{'treasury':-12,'reform':4,'legitimacy':4},'research_speed_factor = 0.025'),
]
NAMES={
 'ENG':('ENG - Great Britain.txt','William Pitt the Younger'),
 'HAB':('HAB - Habsburg Austria.txt','Joseph II'),
 'PRU':('PRU - Prussia.txt','Friedrich Wilhelm II'),
 'RUS':('RUS - Russian Empire.txt','Catherine II'),
}
SUCCESSIONS=[
 (401,'HAB','1790.2.19','Joseph II','Leopold II'),
 (402,'HAB','1792.2.29','Leopold II','Franz II'),
 (403,'PRU','1797.11.15','Friedrich Wilhelm II','Friedrich Wilhelm III'),
]
PARENTS={0:[],1:[[0]],2:[[0]],3:[[1]],4:[[2]],5:[[3,4]],6:[[5]],7:[[5]],8:[[6],[7]]}
COORDS=[(6,0),(3,1),(9,1),(3,2),(9,2),(6,3),(3,4),(9,4),(6,5)]


def identity(row,n):return f'{row[0]}_nap_{row[1]}_{n:02d}'


def option_guard(deltas):
    guards=[f'NOT = {{ check_variable = {{ nap_{key} < {-value} }} }}' for key,value in deltas.items() if key=='treasury' and value<0]
    guards += [f'NOT = {{ check_variable = {{ nap_{key} > {100-value} }} }}' for key,value in deltas.items() if key in ('debt','treasury') and value>0]
    return ' '.join(guards)


def build(root):
    output={};focuses=[];events=['add_namespace = nap_major'];ideas=['ideas = { country = {'];loc=['\ufeffl_english:'];index=[]
    for pi,row in enumerate(PROGRAMMES):
        tag,key,title,anchor,names,issue,alabel,adelta,blabel,bdelta,modifier=row
        names=names.split('|')
        if len(names)!=9:raise ValueError(key)
        for n,name in enumerate(names):
            identifier=identity(row,n);x,y=COORDS[n];x+=(pi%3)*20;y+=15
            parents=[[anchor]] if n==0 else [[identity(row,p) for p in group] for group in PARENTS[n]]
            prereq=' '.join('prerequisite = { '+' '.join('focus = '+p for p in group)+' }' for group in parents)
            exclusive=f'mutually_exclusive = {{ focus = {identity(row,3-n)} }}' if n in (1,2) else ''
            cost=[2,3,3,4,4,2,5,5,7][n]
            guard=f'tag = {tag} is_subject = no NOT = {{ has_country_flag = {identifier}_paid }}'
            reward=change('reform',2)+(' navy_experience = 5' if key=='admiralty' else ' army_experience = 3' if key in ('charles','reform','liberation','distance') else ' add_political_power = 12')
            if n in (5,8):reward=f'country_event = {{ id = nap_major.{pi*10+(1 if n==5 else 2)} hours = 6 }}'
            if n==8:reward+=f' add_ideas = nap_major_{tag}_{key}'
            focuses.append(f'shared_focus = {{ id = {identifier} icon = GFX_goal_generic_political_pressure x = {x} y = {y} cost = {cost} {prereq} {exclusive} available = {{ tag = {tag} is_subject = no }} cancel_if_invalid = yes completion_reward = {{ if = {{ limit = {{ {guard} }} set_country_flag = {identifier}_paid nap_era_initialize = yes {reward} nap_era_clamp = yes nap_era_refresh = yes }} }} ai_will_do = {{ factor = 1 }} }}')
            loc += [f' {identifier}:0 "{name}"',f' {identifier}_desc:0 "Advance the {title.lower()} programme. Its policy choices balance state capacity, public acceptance and the finite resources available to this government. This branch builds on the existing national path rather than overriding its government or territorial settlement."']
            index.append({'id':identifier,'tag':tag,'title':name,'days':cost*7,'anchor':anchor})
        idea=f'nap_major_{tag}_{key}'
        ideas.append(f'{idea} = {{ picture = generic_morale_bonus allowed = {{ original_tag = {tag} }} removal_cost = -1 modifier = {{ {modifier} }} }}')
        loc += [f' {idea}:0 "{title}"',f' {idea}_desc:0 "Institutional improvements from the completed {title.lower()} programme. Numeric balance remains provisional."']
        for slot in (1,2):
            eid=f'nap_major.{pi*10+slot}';token=f'nap_major_{tag}_{key}_{slot}_settled'
            valid=f'tag = {tag} is_subject = no NOT = {{ has_country_flag = {token} }}'
            options=[]
            for letter,label,delta in [('a',alabel,adelta),('b',blabel,bdelta)]:
                guard=valid+' '+option_guard(delta)
                changes=' '.join(change(k,v) for k,v in delta.items())
                options.append(f'option = {{ name = {eid}.{letter} trigger = {{ {guard} }} ai_chance = {{ factor = 50 }} if = {{ limit = {{ {guard} }} set_country_flag = {token} {changes} nap_era_clamp = yes nap_era_refresh = yes }} }}')
                loc.append(f' {eid}.{letter}:0 "{label}."')
            options.append(f'option = {{ name = nap_major_defer ai_chance = {{ factor = 1 }} if = {{ limit = {{ {valid} }} set_country_flag = {token} }} }}')
            events.append(f'country_event = {{ id = {eid} title = {eid}.t desc = {eid}.d picture = GFX_report_event_generic_assembly is_triggered_only = yes fire_only_once = yes '+' '.join(options)+' }')
            deltas_text='; '.join(f'{k.replace("_"," ")} {v:+}' for k,v in adelta.items())+' versus '+'; '.join(f'{k.replace("_"," ")} {v:+}' for k,v in bdelta.items())
            loc += [f' {eid}.t:0 "{issue if slot==1 else title+": Reviewing the Settlement"}"',f' {eid}.d:0 "The {title.lower()} programme requires an explicit allocation of resources. Neither course is free of trade-offs: {deltas_text}. The second review concerns sustaining the programme, not a duplicate of the first authorization. Deferring imposes no resource change."']
    for eid,tag,date,previous,next_name in SUCCESSIONS:
        valid=f'tag = {tag} has_government = neutrality date > {date} has_country_leader = {{ name = "{previous}" ruling_only = yes }} NOT = {{ has_country_flag = nap_major_succession_{eid} }}'
        events.append(f'country_event = {{ id = nap_major.{eid} title = nap_major.{eid}.t desc = nap_major.{eid}.d picture = GFX_report_event_generic_assembly fire_only_once = yes trigger = {{ {valid} }} mean_time_to_happen = {{ days = 1 }} immediate = {{ if = {{ limit = {{ {valid} }} set_country_flag = nap_major_succession_{eid} create_country_leader = {{ name = "{next_name}" ideology = despotism }} }} }} option = {{ name = nap_major_succession_ack }} }}')
        loc += [f' nap_major.{eid}.t:0 "{next_name} Succeeds to the Crown"',f' nap_major.{eid}.d:0 "The crown passes from {previous} to {next_name}. This succession applies only if the prior monarch is still the reigning leader; it does not overwrite an alternate government."']
    loc += [' nap_major_defer:0 "Defer this additional commitment."',' nap_major_succession_ack:0 "The institutions of the state continue."']
    ideas.append('} }')
    output['common/national_focus/nap_major_programmes.txt']='\n'.join(focuses)+'\n'
    output['events/07_major_programmes.txt']='\n'.join(events)+'\n'
    output['common/ideas/nap_major_programmes.txt']='\n'.join(ideas)+'\n'
    output['localisation/english/nap_major_programmes_l_english.yml']='\n'.join(loc)+'\n'
    output['docs/major-focus-index.json']=json.dumps(index,indent=2)+'\n'
    output['docs/great-power-programmes.md']='''# Great-power programmes (Milestone 5 slice)

108 focuses extend the existing British, Austrian, Prussian and Russian trees: 27 each, split into three distinct institutional programmes. Twenty-four policy reviews offer country-specific resource trade-offs, and twelve permanent spirits conclude the programmes. The shared era meters make choices interact with coalition funding and campaign exhaustion.

The existing trees and paths remain. This is not four content-complete campaigns: wider colonial systems, bespoke wars and full alternate branches still need development. No new territorial acquisition is awarded here.

Starting histories now create only the 1789 ruler for these four powers, instead of also creating future rulers in the same ideology slot at startup. Britain's political slot is aligned with its constitutional-government leader subtype. Austrian and Prussian succession events require the previous monarch still to rule. Russian succession focuses create their named leaders and require continued monarchy.

The two Austrian succession dates follow the Habsburg historical collection: Joseph II died 20 February 1790; Leopold II died 1 March 1792. The Prussian change follows the 16 November 1797 accession recorded in the historical literature. Britain is initialized under Pitt, whose first ministry began in 1783. Future British ministerial transitions are not all modeled by this slice.

Sources: https://www.habsburger.net/en/persons/habsburg-emperor/joseph-ii ; https://www.habsburger.net/en/persons/habsburg-emperor/leopold-ii ; https://en.wikisource.org/wiki/1911_Encyclop%C3%A6dia_Britannica/Frederick_William_III._of_Prussia ; https://www.gov.uk/government/history/past-prime-ministers/william-pitt

No HOI4 executable was run. Unit tests validate structure, not native leader/focus behavior.
'''
    return output


def postprocess(outputs,root):
    result={}
    for tag,(filename,initial) in NAMES.items():
        entries=parse((root/'content/legacy'/f'{tag}_history.txt').read_text(encoding='utf-8-sig'))
        entries=[e for e in entries if e.key!='create_country_leader' or e.scalar('name')==initial]
        if tag=='ENG':
            for e in entries:
                if e.key=='set_politics':
                    for p in e.children('ruling_party'):p.value='democratic'
                if e.key=='set_popularities':
                    for p in e.value:
                        if p.key=='neutrality':p.value='38'
                        if p.key=='democratic':p.value='55'
        result['history/countries/'+filename]=dumps(entries)
        path=f'common/national_focus/{tag}.txt'
        text=outputs.get(path)
        if text is None:text=(root/'content/legacy'/f'{tag}.txt').read_text(encoding='utf-8-sig')
        if isinstance(text,bytes):text=text.decode('utf-8-sig')
        tree=parse(text);ft=next(e for e in tree if e.key=='focus_tree')
        for row in PROGRAMMES:
            if row[0]==tag:ft.value.append(Entry('shared_focus',identity(row,0)))
        if tag=='RUS':
            for focus in ft.children('focus'):
                if focus.scalar('id') in ('RUS_paul_succeeds','RUS_alexander_succeeds'):
                    name='Paul I' if focus.scalar('id')=='RUS_paul_succeeds' else 'Alexander I'
                    available=focus.children('available')
                    if available:available[0].value+=parse('has_government = neutrality')
                    else:focus.value.append(Entry('available',parse('has_government = neutrality')))
                    focus.children('completion_reward')[0].value+=parse(f'if = {{ limit = {{ has_government = neutrality }} create_country_leader = {{ name = "{name}" ideology = despotism }} }}')
        result[path]=dumps(tree)
    return result
