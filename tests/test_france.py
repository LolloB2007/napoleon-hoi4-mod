import json
import re
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'content'))
from pdx import Entry,parse,dumps,walk,validate_graph
from build_20_france import build,CHAPTERS,COSTS,PARENTS,ROUTES,fid,event_id
from france_legacy import RULES,FOCUS_DATE_GATES

class FranceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files=build(ROOT)
        cls.nodes={}
        for path,text in cls.files.items():
            if path.startswith('common/national_focus/'):
                for node in walk(parse(text)):
                    if node.key in ('focus','shared_focus') and isinstance(node.value,list):
                        identifier=node.scalar('id')
                        if identifier in cls.nodes: raise ValueError('duplicate '+identifier)
                        cls.nodes[identifier]=node
        cls.events={}
        for path,text in cls.files.items():
            if path.startswith('events/'):
                for node in parse(text):
                    if node.key in ('country_event','news_event'):
                        if node.scalar('id') in cls.events: raise ValueError('duplicate event')
                        cls.events[node.scalar('id')]=node
        cls.loc=cls.files['localisation/english/nap_french_development_l_english.yml']
    def test_450_distinct_foci(self):
        self.assertEqual(len(self.nodes),450)
    def test_named_chapters(self):
        names=[name for ch in CHAPTERS for name in ch['names']]
        self.assertEqual(len(names),420)
        self.assertEqual(len(set(names)),420)
        self.assertTrue(all(len(ch['questions'])==3 for ch in CHAPTERS))
    def test_generated_scripts_parse(self):
        for path,text in self.files.items():
            if path.endswith('.txt'): parse(text)
    def test_graph_no_cycles_or_missing_refs(self):
        validate_graph(self.nodes)
    def test_forks_rejoin_without_requiring_exclusions(self):
        for chapter in CHAPTERS:
            for n in (5,13):
                blocks=self.nodes[fid(chapter,n)].children('prerequisite')
                self.assertEqual(len(blocks),1)
                self.assertEqual(len(blocks[0].children('focus')),2)
            self.assertEqual(len(self.nodes[fid(chapter,10)].children('prerequisite')),2)
    def test_unique_new_coordinates(self):
        nodes=[n for key,n in self.nodes.items() if key.startswith('FRA_nap_')]
        coords=[(n.scalar('x'),n.scalar('y')) for n in nodes]
        self.assertEqual(len(coords),len(set(coords)))
    def test_six_focus_durations(self):
        days={7*int(n.scalar('cost')) for key,n in self.nodes.items() if key.startswith('FRA_nap_')}
        self.assertEqual(days,{14,21,28,35,49,70})
    def test_all_chapter_roots_imported(self):
        tree=parse(self.files['common/national_focus/FRA.txt'])[0]
        imports={str(e.value) for e in tree.children('shared_focus')}
        self.assertEqual(len(imports),29)
        for chapter in CHAPTERS:
            self.assertIn(fid(chapter,0),imports)
    def test_84_new_events(self):
        self.assertEqual(len([e for e in self.events if e.startswith('nap_fra_development.')]),84)
    def test_events_have_localisation(self):
        for key,e in self.events.items():
            if not key.startswith('nap_fra_development.'): continue
            for suffix in ('.t','.d','.a','.b'):
                self.assertIn(' '+key+suffix+':0 ',self.loc)
    def test_new_focus_names_and_descriptions(self):
        for key in self.nodes:
            if not key.startswith('FRA_nap_'): continue
            self.assertIn(' '+key+':0 ',self.loc)
            self.assertIn(' '+key+'_desc:0 ',self.loc)
    def test_policy_events_have_execution_guards(self):
        for key,e in self.events.items():
            if not key.startswith('nap_fra_development.'): continue
            for option in e.children('option')[:2]:
                self.assertTrue(option.children('trigger'))
                guarded=option.children('if')[0]
                self.assertTrue(guarded.children('limit'))
                self.assertEqual(guarded.value[1].key,'set_country_flag')
    def test_reward_idempotency(self):
        for e in parse(self.files['common/scripted_effects/nap_france_rewards.txt']):
            guarded=e.children('if')[0]
            self.assertEqual(guarded.value[1].key,'set_country_flag')
            self.assertIn('NOT',dumps(guarded.children('limit')))
    def test_legacy_options_execution_guarded(self):
        for key in RULES:
            event=self.events[key]
            for option in event.children('option')[:-1]:
                self.assertTrue(option.children('if'),key)
                self.assertTrue(option.children('trigger'),key)
    def test_trial_does_not_retire_current_republican_leader(self):
        self.assertNotIn('retire_country_leader',[e.key for e in walk(self.events['french_revolution.9'].value)])
    def test_brumaire_clears_old_route(self):
        entries=list(walk(self.events['french_revolution.14'].children('option')[0].value))
        self.assertTrue(any(e.key=='clr_country_flag' and e.value=='french_revolutionary_path' for e in entries))
    def test_a01_dates_are_focus_gates(self):
        for focus_id,gate in FOCUS_DATE_GATES.items():
            available=dumps(self.nodes[focus_id].children('available'))
            self.assertIn(f'date > {gate}',available,focus_id)
        for key in RULES:
            self.assertNotIn('date >',dumps(self.events[key].children('trigger')),key)
    def test_directory_without_terror(self):
        event=self.events['french_revolution.12']
        trigger=dumps(event.children('trigger'))
        self.assertNotIn('date >',trigger)
        self.assertIn('nap_fra_thermidor_settled',trigger)
        self.assertNotIn('reign_of_terror_active',trigger)
        self.assertNotIn('french_revolution.12',dumps(self.events['french_revolution.11'].children('option')))
    def test_restoration_not_replaying_once_event(self):
        entries=list(walk(self.events['napoleonic_collapse.10'].value))
        self.assertFalse(any(e.key=='country_event' and e.scalar('id')=='napoleonic_collapse.6' for e in entries))
        self.assertTrue(any(e.key=='create_country_leader' and e.scalar('name')=='Louis XVIII' for e in entries))
    def test_foreign_events_not_french_scope(self):
        self.assertIn('tag = HAB',dumps(self.events['napoleonic_wars.61'].children('option')[0].children('if')[0].children('limit')))
        self.assertIn('tag = PRU',dumps(self.events['napoleonic_wars.91'].children('option')[0].children('if')[0].children('limit')))
    def test_ideas_count(self):
        ideas=parse(self.files['common/ideas/nap_france_programmes.txt'])[0].children('country')[0]
        self.assertEqual(len(ideas.value),56)
    def test_programmes_do_not_transfer_or_core_territory(self):
        text=self.files['common/scripted_effects/nap_france_rewards.txt']
        self.assertNotIn('transfer_state',text)
        self.assertNotIn('add_core_of',text)
    def test_quote_roundtrip(self):
        text='title = "A \\"quote\\" and { brace } # text"'
        self.assertEqual(parse(text),parse(dumps(parse(text))))
    def test_legacy_roundtrip(self):
        for p in (ROOT/'content/legacy').glob('*.txt'):
            parsed=parse(p.read_text(encoding='utf-8-sig'))
            self.assertEqual(parsed,parse(dumps(parsed)))
    def test_all_event_calls_target_defined_ids(self):
        for path,text in self.files.items():
            if not path.endswith('.txt'): continue
            for e in walk(parse(text)):
                if e.key in ('country_event','news_event') and isinstance(e.value,list):
                    self.assertIn(e.scalar('id'),self.events, (path,e.scalar('id')))

if __name__=='__main__': unittest.main()
