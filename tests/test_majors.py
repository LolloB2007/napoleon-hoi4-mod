import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from pdx import parse,walk,dumps,validate_graph
from build_40_great_powers import build,postprocess,PROGRAMMES,NAMES,identity,option_guard

class MajorTests(unittest.TestCase):
    def test_108_named_focuses(self):
        self.assertEqual(len(PROGRAMMES),12)
        names=[n for row in PROGRAMMES for n in row[4].split('|')]
        self.assertEqual(len(names),108)
        self.assertEqual(len(set(names)),108)
    def test_scripts_parse(self):
        for path,text in build(ROOT).items():
            if path.endswith('.txt'):parse(text)
    def test_27_focuses_each(self):
        nodes=parse(build(ROOT)['common/national_focus/nap_major_programmes.txt'])
        for tag in NAMES:self.assertEqual(len([n for n in nodes if n.scalar('id').startswith(tag+'_')]),27)
    def test_existing_tree_integration(self):
        files=postprocess({},ROOT);graph={}
        for path,text in (build(ROOT)|files).items():
            if path.startswith('common/national_focus/'):
                for e in walk(parse(text)):
                    if e.key in ('focus','shared_focus') and isinstance(e.value,list):graph[e.scalar('id')]=e
        validate_graph(graph)
        for tag in NAMES:
            tree=parse(files[f'common/national_focus/{tag}.txt'])[0]
            self.assertEqual(len(tree.children('shared_focus')),3)
    def test_only_current_rulers_at_start(self):
        files=postprocess({},ROOT)
        for tag,(filename,initial) in NAMES.items():
            leaders=[e.scalar('name') for e in parse(files['history/countries/'+filename]) if e.key=='create_country_leader']
            self.assertEqual(leaders,[initial])
    def test_british_government_matches_subtype(self):
        self.assertIn('ruling_party = democratic',postprocess({},ROOT)['history/countries/ENG - Great Britain.txt'])
    def test_succession_does_not_overwrite_alternate_ruler(self):
        for e in parse(build(ROOT)['events/07_major_programmes.txt']):
            if e.key=='country_event' and int(e.scalar('id').split('.')[1])>=400:
                self.assertIn('has_country_leader',dumps(e.children('trigger')))
                self.assertIn('has_country_leader',dumps(e.children('immediate')))
    def test_russian_succession_focus_creates_ruler(self):
        text=postprocess({},ROOT)['common/national_focus/RUS.txt']
        self.assertIn('name = "Paul I"',text)
        self.assertIn('name = "Alexander I"',text)
    def test_no_new_territorial_awards(self):
        for path,text in build(ROOT).items():
            if path.endswith('.txt'):
                self.assertNotIn('transfer_state',text)
                self.assertNotIn('add_core_of',text)
    def test_every_policy_has_safe_deferral(self):
        for e in parse(build(ROOT)['events/07_major_programmes.txt']):
            if e.key=='country_event' and int(e.scalar('id').split('.')[1])<400:
                self.assertEqual(e.children('option')[-1].scalar('name'),'nap_major_defer')
    def test_loan_cannot_overflow_debt(self):
        self.assertIn('nap_debt > 75',option_guard({'treasury':20,'debt':25}))
        self.assertIn('nap_treasury > 80',option_guard({'treasury':20,'debt':25}))
    def test_option_resource_checks_repeated(self):
        for e in parse(build(ROOT)['events/07_major_programmes.txt']):
            if e.key=='country_event' and int(e.scalar('id').split('.')[1])<400:
                for option in e.children('option')[:2]:
                    self.assertEqual(option.children('trigger')[0].value,option.children('if')[0].children('limit')[0].value)
    def test_localisation(self):
        files=build(ROOT);loc=files['localisation/english/nap_major_programmes_l_english.yml']
        for path,text in files.items():
            if path.startswith('events/'):
                for e in parse(text):
                    if e.key=='country_event':
                        for field in ('title','desc'):self.assertIn(' '+e.scalar(field)+':0 ',loc)
                        for option in e.children('option'):self.assertIn(' '+option.scalar('name')+':0 ',loc)
    def test_three_programmes_per_country(self):
        for tag in NAMES:self.assertEqual(len([r for r in PROGRAMMES if r[0]==tag]),3)

if __name__=='__main__':unittest.main()
