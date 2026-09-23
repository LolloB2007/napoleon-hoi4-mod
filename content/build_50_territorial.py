"""Territorial interfaces with explicit approval gates and ownership checks."""
import json
import re
from pdx import Entry,parse,dumps,walk
from build_00_contracts import COUNTRIES
from build_10_era import change

TAGS={line.split('|')[0]:line.split('|')[2] for line in COUNTRIES.splitlines()}
RHINE='BAV WUR BAD HES SAX'.split()


def validate_registry(data):
    if data.get('schema_version')!=1:raise ValueError('unsupported territorial registry schema')
    seen=set()
    for kind in ('integrations','formables'):
        for row in data[kind]:
            key=row['id']
            if not re.fullmatch('[a-z][a-z0-9_]*',key) or key in seen:raise ValueError('invalid or duplicate registry id')
            seen.add(key)
            if type(row['approved']) is not bool:raise ValueError('approval must be an explicit boolean')
            states=row['states'] if kind=='integrations' else row['required_states']
            if len(states)!=len(set(states)) or any(type(s) is not int or s<=0 for s in states):raise ValueError('invalid state set')
            tags=[row['country']] if kind=='integrations' else row['founders']
            if not tags or any(t not in TAGS for t in tags):raise ValueError('unknown country in territorial registry')
            if row['approved'] and (not states or not row['approved_by'].strip()):raise ValueError('approved entries require explicit borders and approval attribution')
            if kind=='formables' and not re.fullmatch('[A-Z][A-Z0-9_]*',row['cosmetic_tag']):raise ValueError('invalid cosmetic tag')
            if kind=='integrations':
                if row['country']!='FRA' or row['route'] not in ('constitutional','republican','royalist','imperial'):raise ValueError('unimplemented integration route')
                if row['approved'] and (row.get('approval')!='A04' or not row.get('basis','').strip()):raise ValueError('approved A04 integration requires explicit historical basis')
                if row['days']<180 or row['treasury']<=0 or not 0<=row['compliance']<=100 or not 0<=row['resistance_max']<=100:raise ValueError('invalid integration policy')
    for kind in ('releasables','clients'):
        if len(set(data[kind]))!=len(data[kind]) or any(t not in TAGS for t in data[kind]):raise ValueError('invalid country list')


def integration_eligible(row,*,owner,controller,route,compliance,resistance,at_war,already_core):
    return row['approved'] and owner==row['country'] and controller==owner and route==row['route'] and compliance>=row['compliance'] and resistance<=row['resistance_max'] and not at_war and not already_core


def integrate_model(row,history):
    # Every observed invalid state cancels the process, not merely the last day.
    elapsed=0
    for frame in history:
        if not integration_eligible(row,**frame):return False
        elapsed+=1
    return elapsed>=row['days']


def release_model(owner,target,states,existing):
    if target in existing:return dict(states)
    return {key: ({**value,'owner':target,'controller':target} if value['owner']==owner and value['controller']==owner and target in value['cores'] else dict(value)) for key,value in states.items()}


def build(root):
    data=json.loads((root/'content/territorial_registry.json').read_text());validate_registry(data)
    output={};decisions=['nap_territorial_council = {'];effects=[];loc=['\ufeffl_english:',' nap_territorial_council:0 "Territorial and Client Administration"',' nap_territorial_council_desc:0 "Restore countries only from existing cores, support existing clients, or carry out explicitly approved integration programmes. Pending territorial proposals are not enabled in the game."',' nap_client_offer.t:0 "A Proposed Rhine Client Charter"',' nap_client_offer.d:0 "France offers membership of its dependent-state network. Acceptance makes this state a French subject under the existing client design. Refusal preserves independence and imposes no territorial transfer. Neither option can replace an unrelated faction or an existing overlord."',' nap_client_offer.a:0 "Accept the dependent-state charter."',' nap_client_offer.b:0 "Retain our present independence."']
    for target in data['releasables']:
        name=TAGS[target];key='nap_restore_'+target
        guard=f'nap_era_country = yes is_subject = no has_war = no {target} = {{ exists = no }} any_owned_state = {{ is_core_of = {target} is_controlled_by = ROOT }} NOT = {{ any_owned_state = {{ is_core_of = {target} NOT = {{ is_controlled_by = ROOT }} }} }} NOT = {{ check_variable = {{ nap_treasury < 12 }} }}'
        effects.append(f'{key}_effect = {{ if = {{ limit = {{ {guard} }} release = {target} if = {{ limit = {{ {target} = {{ exists = yes }} }} puppet = {target} {change("treasury",-12)} nap_era_clamp = yes }} else = {{ add_political_power = 35 }} }} }}')
        decisions.append(f'{key} = {{ icon = generic_political_discourse cost = 35 days_re_enable = 365 visible = {{ nap_era_country = yes {target} = {{ exists = no }} any_owned_state = {{ is_core_of = {target} }} }} available = {{ {guard} }} complete_effect = {{ {key}_effect = yes }} ai_will_do = {{ factor = 0 }} }}')
        loc += [f' {key}:0 "Restore {name} as a Client"',f' {key}_desc:0 "Release this country from only its existing cores that we own, then establish the standard HOI4 puppet relationship under A06. It must not already exist, and releasable states must be under our control while we are at peace. Costs 12 treasury after a successful release. No cores are invented and no third-party land is transferred."']
    for target in data['clients']:
        name=TAGS[target];key='nap_client_aid_'+target
        guard=f'tag = FRA has_country_flag = nap_era_initialized NOT = {{ check_variable = {{ nap_treasury < 12 }} }} {target} = {{ exists = yes is_subject_of = FRA has_country_flag = nap_era_initialized NOT = {{ check_variable = {{ nap_treasury > 88 }} }} }}'
        effects.append(f'{key}_effect = {{ if = {{ limit = {{ {guard} }} {change("treasury",-12)} {target} = {{ {change("treasury",12)} {change("legitimacy",2)} {change("reform",2)} nap_era_clamp = yes nap_era_refresh = yes }} nap_era_clamp = yes }} }}')
        decisions.append(f'{key} = {{ icon = generic_political_discourse cost = 25 days_re_enable = 180 visible = {{ tag = FRA {target} = {{ is_subject_of = FRA }} }} available = {{ {guard} }} complete_effect = {{ {key}_effect = yes }} ai_will_do = {{ factor = 1 }} }}')
        loc += [f' {key}:0 "Support the Administration of {name}"',f' {key}_desc:0 "Transfer 12 treasury to this existing French client. Its legitimacy and administrative reform each improve by 2. This does not create a subject, change borders, or annex a client."']
    for row in data['integrations']:
        if not row['approved']:continue
        for sid in row['states']:
            key=f'nap_integrate_{row["id"]}_{sid}';flag=key+'_active'
            valid=f'nap_fra_route_{row["route"]} = yes has_war = no {sid} = {{ is_owned_by = FRA is_controlled_by = FRA NOT = {{ is_core_of = FRA }} NOT = {{ compliance < {row["compliance"]} }} NOT = {{ resistance > {row["resistance_max"]} }} }}'
            money=f'NOT = {{ check_variable = {{ nap_treasury < {row["treasury"]} }} }}'
            decisions.append(f'''{key} = {{ icon = generic_political_discourse cost = 75 days_remove = {row['days']} days_re_enable = 365
 visible = {{ tag = FRA {sid} = {{ is_owned_by = FRA NOT = {{ is_core_of = FRA }} }} }}
 available = {{ {valid} {money} NOT = {{ has_country_flag = {flag} }} }}
 complete_effect = {{ if = {{ limit = {{ {valid} {money} NOT = {{ has_country_flag = {flag} }} }} {change('treasury',-row['treasury'])} set_country_flag = {flag} nap_era_clamp = yes }} }}
 cancel_trigger = {{ NOT = {{ {valid} }} }}
 cancel_effect = {{ clr_country_flag = {flag} }}
 remove_effect = {{ if = {{ limit = {{ {valid} has_country_flag = {flag} }} clr_country_flag = {flag} {sid} = {{ add_core_of = FRA }} }} else = {{ clr_country_flag = {flag} }} }}
 ai_will_do = {{ factor = 1 }}
}}''')
            loc += [f' {key}:0 "Integrate {row["title"]}: State {sid}"',f' {key}_desc:0 "An approved, paid {row["days"]}-day programme. France must retain ownership and control, remain at peace, keep compliance at least {row["compliance"]}, and resistance at most {row["resistance_max"]}. Losing these conditions cancels the programme without a core. The {row["treasury"]} treasury investment is not refunded."']
    for row in data['formables']:
        if not row['approved']:continue
        key='nap_form_'+row['id'];flag=key+'_settled'
        founders='OR = { '+' '.join('tag = '+t for t in row['founders'])+' }'
        land=' '.join(f'{sid} = {{ is_owned_by = ROOT is_controlled_by = ROOT }}' for sid in row['required_states'])
        cores=' '.join(f'{sid} = {{ add_core_of = ROOT }}' for sid in row['core_states'])
        guard=f'{founders} is_subject = no has_war = no NOT = {{ has_country_flag = {flag} }} {land}'
        decisions.append(f'{key} = {{ icon = generic_political_discourse cost = 100 fire_only_once = yes visible = {{ {founders} }} available = {{ {guard} }} complete_effect = {{ if = {{ limit = {{ {guard} }} set_country_flag = {flag} set_cosmetic_tag = {row["cosmetic_tag"]} {cores} }} }} ai_will_do = {{ factor = 1 }} }}')
        loc += [f' {key}:0 "Proclaim {row["title"]}"',f' {key}_desc:0 "This approved formation requires independent, peaceful ownership and control of its required state set. On proclamation it grants cores on the explicitly audited core-state set associated with the formable, while preserving the original country tag, leaders and focus tree and annexing no country."']
        for suffix in ('','_DEF','_ADJ','_neutrality','_democratic','_communism','_fascism'):
            loc.append(f' {row["cosmetic_tag"]}{suffix}:0 "{row["title"]}"')
    decisions.append('}')
    candidate='OR = { '+' '.join('tag = '+t for t in RHINE)+' } exists = yes is_subject = no NOT = { has_war_with = FRA } NOT = { has_country_flag = nap_rhine_declined } OR = { is_in_faction = no is_in_faction_with = FRA } FRA = { nap_fra_route_imperial = yes }'
    output['common/scripted_triggers/nap_clients.txt']='nap_rhine_client_candidate = { '+candidate+' }\n'
    accepted='nap_rhine_client_candidate = yes has_country_flag = nap_rhine_offer'
    output['events/08_clients.txt']=f'''add_namespace = nap_clients
country_event = {{ id = nap_clients.10 title = nap_client_offer.t desc = nap_client_offer.d picture = GFX_report_event_generic_assembly is_triggered_only = yes
 option = {{ name = nap_client_offer.a trigger = {{ {accepted} }} ai_chance = {{ factor = 65 }}
  if = {{ limit = {{ {accepted} }} clr_country_flag = nap_rhine_offer FRA = {{ puppet = ROOT }} if = {{ limit = {{ is_subject_of = FRA }} set_country_flag = nap_rhine_charter_accepted }} }}
 }}
 option = {{ name = nap_client_offer.b ai_chance = {{ factor = 35 }} clr_country_flag = nap_rhine_offer set_country_flag = {{ flag = nap_rhine_declined days = 365 }} }}
}}
'''
    output['common/scripted_effects/nap_territorial.txt']='\n'.join(effects)+'\n'
    output['common/decisions/nap_territorial.txt']='\n'.join(decisions)+'\n'
    output['common/decisions/categories/nap_territorial.txt']='nap_territorial_council = { icon = generic_political_discourse allowed = { always = yes } visible = { nap_era_country = yes has_country_flag = nap_era_initialized } }\n'
    templates=[]
    for key,title in [('constitutional_alliance','League of Constitutional Powers'),('sister_republics_league','League of Sister Republics'),('holy_league_of_kings','Holy League of Kings')]:
        templates.append(f'nap_fra_{key} = {{ name = {key} icon = GFX_faction_logo_generic_16 manifest = nap_partner_manifest visible = {{ always = no }} }}')
        loc.append(f' {key}:0 "{title}"')
    output['common/factions/templates/nap_french_partners.txt']='\n'.join(templates)+'\n'
    output['common/factions/goals/nap_french_partners.txt']='nap_partner_manifest = { name = nap_partner_manifest_name description = nap_partner_manifest_desc is_manifest = yes ratio_progress = { total_amount = 1 completed_amount = 0 } }\n'
    loc += [' nap_partner_manifest_name:0 "A Defined Political Partnership"',' nap_partner_manifest_desc:0 "The members retain their existing states and governments unless a separate, explicit agreement provides otherwise."']
    output['localisation/english/nap_territorial_l_english.yml']='\n'.join(loc)+'\n'
    output['docs/territorial-registry.json']=json.dumps(data,indent=2)+'\n'
    output['docs/territorial-systems.md']='''# Territorial and client interfaces (Milestone 8 slice)

A06 standardises clients on native HOI4 puppet relationships. Sixteen restoration decisions release only existing cores owned/controlled by the releasing country and then make the restored state its puppet; twelve paid aid decisions operate only on existing French subjects. The Rhine charter remains an explicit acceptance/refusal event. No path overwrites a living country, annexes a client, or transfers unrelated third-party land.

A04 activates only the two explicitly catalogued, historically grounded French integration programmes: Savoy and the Austrian Netherlands. Both remain paid, cancellable 180+ day programmes with route, peace, ownership, control, compliance and resistance checks. Generic conquest receives no route to coring. A05 activates the six audited formables with explicit state sets derived from the mod's 1789 ownership map.

Approved integration requires continued ownership, control, peace, route eligibility, high compliance and low resistance. Cancellation clears progress; reacquiring the territory does not finish an old programme. The cost is paid once at the beginning, and the completion effect repeats the non-financial checks before adding a core.

Each approved formable preserves the base tag, leaders and focus tree and never annexes an existing country. On formation it grants cores on the explicit core_states catalogue for that formable. Required states and core states are both audited in content/territorial_registry.json so the territorial meaning of formation remains reviewable rather than inferred.

The original three French diplomatic focuses now use dedicated native faction templates and refuse to replace an unrelated existing faction. Their political names and existing route intent are retained.

This does not finish Milestone 8's deep secondary-country campaigns. Release-era leaders/OOB reconstruction, unique country trees, broader client autonomy and the approved territorial maps remain future work. Runtime scope, decision cancellation and subject/faction interaction still require a HOI4 test.
'''
    return output


def postprocess(outputs,root):
    result={}
    path='events/02_napoleonic_wars.txt';entries=parse(outputs[path])
    event=next(e for e in entries if e.key=='country_event' and e.scalar('id')=='napoleonic_wars.7')
    def replace_puppet(nodes):
        result=[]
        for node in nodes:
            if node.key=='FRA' and isinstance(node.value,list) and any(e.key=='puppet' for e in node.value):
                result+=parse('if = { limit = { nap_rhine_client_candidate = yes } set_country_flag = { flag = nap_rhine_offer days = 60 } country_event = { id = nap_clients.10 days = 1 } }')
            else:
                if isinstance(node.value,list):node.value=replace_puppet(node.value)
                result.append(node)
        return result
    event.value=replace_puppet(event.value);result[path]=dumps(entries)
    path='common/national_focus/FRA.txt';entries=parse(outputs[path])
    names={'constitutional_alliance','sister_republics_league','holy_league_of_kings'}
    def factions(nodes):
        result=[]
        for node in nodes:
            if node.key=='create_faction' and node.value in names:
                result+=parse('if = { limit = { is_in_faction = no } create_faction_from_template = { template = nap_fra_'+node.value+' name = '+node.value+' } }')
            else:
                if isinstance(node.value,list):node.value=factions(node.value)
                result.append(node)
        return result
    result[path]=dumps(factions(entries))
    data=json.loads((root/'content/territorial_registry.json').read_text())
    rows=[]
    for kind in ('integrations','formables'):
        for row in data[kind]:
            states=row.get('states',row.get('required_states',[]))
            rows.append(f'| {row["id"]} | {row["title"]} | {states or "Not specified"} | {"Approved" if row["approved"] else "Awaiting approval"} ({row["approval"]}) |')
    result['to ask lollo.md']=outputs['to ask lollo.md']+'\n## Territorial registry status\n\nThe registry below is implementation data under approved A04/A05 policy. Approved entries require explicit borders and attribution in source.\n\n| ID | Proposal | State IDs | Status |\n|---|---|---|---|\n'+'\n'.join(rows)+'\n'
    return result
