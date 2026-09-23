"""Surgical, deterministic repairs to retained French event sources.

A01 policy: historical dates are minimum-date gates on focuses, not autonomous
event timers. Events advance from focus completion and state-machine conditions.
Guard execution as well as scheduling and preserve route safety.
"""
from pdx import Entry, parse, dumps, walk

RULES = {
 'french_revolution.1':'tag = FRA has_country_flag = bourbon_monarchy NOT = { has_country_flag = bastille_stormed } NOT = { has_country_flag = bourbon_crackdown }',
 'french_revolution.2':'tag = FRA has_country_flag = bastille_stormed NOT = { has_country_flag = french_royalist_path } NOT = { has_country_flag = french_bonapartist_path }',
 'french_revolution.4':'nap_fra_route_republican = yes NOT = { has_country_flag = french_republic }',
 'french_revolution.6':'nap_fra_route_republican = yes',
 'french_revolution.8':'nap_fra_route_republican = yes NOT = { has_country_flag = republic_proclaimed }',
 'french_revolution.9':'nap_fra_route_republican = yes has_country_flag = french_republic',
 'french_revolution.91':'NOT = { tag = FRA } FRA = { nap_fra_route_republican = yes has_country_flag = louis_xvi_executed }',
 'french_revolution.10':'nap_fra_route_republican = yes NOT = { has_country_flag = nap_fra_girondins_programme }',
 'french_revolution.11':'nap_fra_route_republican = yes has_country_flag = reign_of_terror_active',
 'french_revolution.12':'nap_fra_route_republican = yes has_country_flag = french_republic has_country_flag = nap_fra_thermidor_settled NOT = { has_country_flag = directory_active }',
 'french_revolution.14':'nap_fra_route_republican = yes has_country_flag = directory_active',
 'napoleonic_wars.3':'nap_fra_route_consular = yes has_country_flag = consulate_established',
 'napoleonic_wars.4':'nap_fra_route_imperial = yes',
 'napoleonic_wars.6':'nap_fra_route_imperial = yes has_war_with = HAB',
 'napoleonic_wars.61':'tag = HAB has_war_with = FRA FRA = { nap_fra_route_imperial = yes }',
 'napoleonic_wars.7':'nap_fra_route_imperial = yes',
 'napoleonic_wars.8':'nap_fra_route_imperial = yes has_country_flag = rheinbund_established',
 'napoleonic_wars.9':'nap_fra_route_imperial = yes has_war_with = PRU',
 'napoleonic_wars.91':'tag = PRU has_war_with = FRA FRA = { nap_fra_route_imperial = yes }',
 'napoleonic_wars.10':'nap_fra_route_imperial = yes',
 'napoleonic_wars.13':'nap_fra_route_imperial = yes has_war_with = RUS',
 'napoleonic_wars.16':'nap_fra_route_imperial = yes NOT = { has_war_with = RUS }',
 'napoleonic_collapse.1':'nap_fra_route_imperial = yes has_country_flag = russian_campaign_active',
 'napoleonic_collapse.2':'tag = PRU FRA = { has_country_flag = grande_armee_destroyed }',
 'napoleonic_collapse.5':'nap_fra_route_imperial = yes',
 'napoleonic_collapse.6':'tag = FRA has_country_flag = napoleon_on_elba',
 'napoleonic_collapse.8':'tag = FRA has_country_flag = bourbon_restoration has_country_flag = napoleon_on_elba',
 'napoleonic_collapse.10':'tag = FRA has_global_flag = waterloo_fought NOT = { has_country_flag = napoleon_on_st_helena }',
}
FOCUS_DATE_GATES = {
 'FRA_convene_estates_general':'1789.5.5',
 'FRA_adopt_declaration':'1789.8.26',
 'FRA_vive_la_revolution':'1791.6.20',
 'FRA_war_on_tyrants':'1792.4.20',
 'FRA_vive_la_republique':'1792.9.22',
 'FRA_trial_of_the_king':'1793.1.21',
 'FRA_reign_of_terror_focus':'1793.9.5',
 'FRA_italian_campaign':'1796.3.1',
 'FRA_egyptian_expedition':'1798.7.1',
 'FRA_brumaire_coup':'1799.11.9',
 'FRA_proclaim_empire':'1804.5.18',
 'FRA_confederation_rhine':'1806.7.12',
 'FRA_continental_system_focus':'1806.11.21',
 'FRA_invade_russia':'1812.6.24',
 'FRA_return_from_elba':'1815.3.1',
}
FOCUS_TRIGGERED_EVENTS = {
 'french_revolution.1','french_revolution.2','french_revolution.4',
 'french_revolution.6','french_revolution.8','french_revolution.9',
 'french_revolution.10','french_revolution.14','napoleonic_wars.3',
 'napoleonic_wars.7','napoleonic_wars.10','napoleonic_wars.16',
 'napoleonic_collapse.8',
}
META = {'name','trigger','ai_chance','highlighted','original_tag','ai_will_do'}

def apply_focus_date_gates(entries):
    """Attach approved A01 minimum dates to focuses while preserving other availability."""
    for node in walk(entries):
        if node.key not in ('focus','shared_focus') or not isinstance(node.value,list):
            continue
        gate=FOCUS_DATE_GATES.get(node.scalar('id'))
        if not gate:
            continue
        condition=Entry('date',gate,'>')
        available=node.children('available')
        if available:
            if not any(e.key=='date' for e in available[0].value):
                available[0].value.append(condition)
        else:
            node.value.append(Entry('available',[condition]))
    return entries

def strip_date_conditions(entries):
    result=[]
    for entry in entries:
        if entry.key=='date':
            continue
        if isinstance(entry.value,list):
            entry.value=strip_date_conditions(entry.value)
        result.append(entry)
    return result


def leader(name, subtype, traits=''):
    return parse('create_country_leader = { name = "'+name+'" ideology = '+subtype+' traits = { '+traits+' } }')


def skip_matching(entries, predicate):
    result = []
    for entry in entries:
        if predicate(entry):
            continue
        if isinstance(entry.value,list):
            entry.value = skip_matching(entry.value,predicate)
        result.append(entry)
    return result


def guard_war(entries):
    """A triggered invitation must not attempt to declare an already active war."""
    result = []
    for entry in entries:
        if entry.key == 'declare_war_on':
            target = entry.scalar('target')
            result.append(Entry('if',[Entry('limit',parse(f'NOT = {{ has_war_with = {target} }}')),entry]))
        else:
            if isinstance(entry.value,list):
                entry.value = guard_war(entry.value)
            result.append(entry)
    return result


def guard_options(event, condition):
    identifier = event.scalar('id')
    token = 'nap_legacy_'+identifier.replace('.','_')+'_settled'
    valid = f'{condition} NOT = {{ has_country_flag = {token} }}'
    for option in event.children('option'):
        meta = [e for e in option.value if e.key in META]
        effects = guard_war([e for e in option.value if e.key not in META])
        old_trigger = next((e for e in meta if e.key=='trigger'),None)
        if old_trigger:
            old_trigger.value += parse(valid)
        else:
            meta.append(Entry('trigger',parse(valid)))
        option.value = meta + [Entry('if',[Entry('limit',parse(valid)),Entry('set_country_flag',token),*effects])]
    event.value.append(Entry('option',parse(f'name = nap_fra_legacy_superseded trigger = {{ NOT = {{ {valid} }} }} ai_chance = {{ factor = 100 }}')))


def patch_legacy(root):
    output = {}
    for filename in ('01_french_revolution.txt','02_napoleonic_wars.txt','03_collapse.txt'):
        entries = parse((root/'content/legacy'/filename).read_text(encoding='utf-8-sig'))
        for event in entries:
            if event.key != 'country_event':
                continue
            identifier = event.scalar('id')
            if identifier not in RULES:
                raise ValueError(f'Unreviewed legacy country event: {identifier}')
            for trigger in event.children('trigger'):
                trigger.value=strip_date_conditions(trigger.value)
            if identifier in FOCUS_TRIGGERED_EVENTS:
                event.value=[e for e in event.value if e.key!='mean_time_to_happen']
                if not event.children('is_triggered_only'):
                    event.value.append(Entry('is_triggered_only','yes'))
            options = event.children('option')
            first = options[0]
            if identifier in ('french_revolution.9','french_revolution.11'):
                first.value = [e for e in first.value if e.key!='retire_country_leader']
            if identifier=='french_revolution.8':
                first.value += leader('National Convention','marxism')
            elif identifier=='french_revolution.10':
                first.value += leader('Maximilien Robespierre','marxism','incorruptible')
                options[1].value.append(Entry('set_country_flag','nap_fra_terror_restrained'))
                event.children('trigger')[0].value += parse('NOT = { has_country_flag = nap_fra_girondins_programme }')
            elif identifier=='french_revolution.11':
                first.value = skip_matching(first.value,lambda e:e.key=='country_event' and e.scalar('id')=='french_revolution.12')
                first.value += leader('Thermidorian Convention','marxism')
                first.value.append(Entry('set_country_flag','nap_fra_thermidor_settled'))
            elif identifier=='french_revolution.12':
                event.value = [e for e in event.value if e.key not in ('is_triggered_only','trigger','mean_time_to_happen')]
                event.value += parse('trigger = { nap_fra_route_republican = yes has_country_flag = french_republic has_country_flag = nap_fra_thermidor_settled NOT = { has_country_flag = directory_active } NOT = { has_country_flag = nap_legacy_french_revolution_12_settled } } mean_time_to_happen = { days = 30 }')
                first.value += parse('clr_country_flag = reign_of_terror_active remove_ideas = reign_of_terror')
                first.value += leader('Executive Directory','marxism')
            elif identifier=='french_revolution.14':
                first.value += parse('clr_country_flag = french_revolutionary_path')
                first.value += leader('Napoleon Bonaparte','fascism_ideology','military_genius')
            elif identifier=='napoleonic_collapse.6':
                first.value += leader('Louis XVIII','despotism')
            elif identifier=='napoleonic_collapse.8':
                first.value += parse('set_country_flag = french_bonapartist_path clr_country_flag = french_constitutional_path clr_country_flag = french_royalist_path clr_country_flag = french_revolutionary_path')
                first.value += leader('Napoleon Bonaparte','fascism_ideology','military_genius')
            elif identifier=='napoleonic_collapse.10':
                first.value = [e for e in first.value if e.key not in ('retire_country_leader','country_event')]
                first.value += parse('set_country_flag = bourbon_restoration clr_country_flag = hundred_days clr_country_flag = empire_of_the_french remove_ideas = liberal_empire remove_ideas = empire_of_the_french add_ideas = bourbon_restoration_idea set_politics = { ruling_party = neutrality elections_allowed = no }')
                first.value += leader('Louis XVIII','despotism')
            guard_options(event,RULES[identifier])
        output['events/'+filename] = '# Generated from retained source; A01 uses focus date floors, route state and repeat guards rather than autonomous historical dates.\n'+dumps(entries)
    return output
