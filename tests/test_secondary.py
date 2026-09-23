import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from pdx import parse,walk,dumps
from build_60_secondary import build,PROFILES

class SecondaryCampaignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs=build(ROOT)
        cls.loc=cls.outputs['localisation/english/nap_secondary_campaigns_l_english.yml']

    def test_profile_count(self):
        self.assertEqual(len(PROFILES),13)

    def test_roadmap_families_covered(self):
        tags={t for p in PROFILES for t in p['tags']}
        for tag in ('SPR','POL','WAR','TUR','SWE','SAR','NAP','PAP','VEN','TUS','BAV','SAX','HAN','WUR','POR','NET','BAT','HOL','USA'):
            self.assertIn(tag,tags)

    def test_focus_count(self):
        texts=[v for k,v in self.outputs.items() if k.startswith('common/national_focus/secondary_')]
        self.assertEqual(len(texts),13)
        self.assertEqual(sum(t.count('focus = {') for t in texts),299)

    def test_focus_ids_unique(self):
        ids=[]
        for path,text in self.outputs.items():
            if not path.startswith('common/national_focus/secondary_'):continue
            for node in walk(parse(text)):
                if node.key=='focus' and isinstance(node.value,list) and node.scalar('id'):ids.append(node.scalar('id'))
        self.assertEqual(len(ids),299)
        self.assertEqual(len(ids),len(set(ids)))

    def test_route_roots_are_exclusive(self):
        for p in PROFILES:
            pre='NAP_'+p['slug'].upper()
            tree=parse(self.outputs[f'common/national_focus/secondary_{p["slug"]}.txt'])
            nodes={n.scalar('id'):n for n in walk(tree) if n.key=='focus' and isinstance(n.value,list) and n.scalar('id')}
            h=nodes[f'{pre}_HIST_1'];a=nodes[f'{pre}_ALT_1']
            self.assertIn(f'{pre}_ALT_1',dumps(h.children('mutually_exclusive')))
            self.assertIn(f'{pre}_HIST_1',dumps(a.children('mutually_exclusive')))

    def test_event_count(self):
        events=[n for n in parse(self.outputs['events/09_secondary_campaigns.txt']) if n.key=='country_event']
        self.assertEqual(len(events),52)
        self.assertEqual(len({e.scalar('id') for e in events}),52)

    def test_decision_count(self):
        root=parse(self.outputs['common/decisions/nap_secondary_campaigns.txt'])[0]
        self.assertEqual(root.key,'nap_secondary_policy')
        self.assertEqual(len(root.value),39)

    def test_idea_count(self):
        entries=parse(self.outputs['common/ideas/nap_secondary_campaigns.txt'])
        country=entries[0].children('country')[0]
        self.assertEqual(len(country.value),65)

    def test_all_generated_scripts_parse(self):
        for path,text in self.outputs.items():
            if path.endswith('.txt'):parse(text)

    def test_localisation_covers_focus_event_idea_decision_keys(self):
        for path,text in self.outputs.items():
            if path.startswith('common/national_focus/secondary_'):
                for node in walk(parse(text)):
                    if node.key=='focus' and isinstance(node.value,list) and node.scalar('id'):self.assertIn(' '+node.scalar('id')+':0 ',self.loc)
        for event in [n for n in parse(self.outputs['events/09_secondary_campaigns.txt']) if n.key=='country_event']:
            self.assertIn(' '+event.scalar('id')+'.t:0 ',self.loc)
        ideas=parse(self.outputs['common/ideas/nap_secondary_campaigns.txt'])[0].children('country')[0].value
        for idea in ideas:self.assertIn(' '+idea.key+':0 ',self.loc)
        for p in PROFILES:
            for suffix in ('administrative_review','mobilization_review','foreign_mission'):
                self.assertIn(f' nap_{p["slug"]}_{suffix}:0 ',self.loc)

    def test_major_power_links_are_bounded(self):
        events=self.outputs['events/09_secondary_campaigns.txt']
        for p in PROFILES:
            for major in p['majors']:self.assertIn(f'target = {major} modifier = nap_1789_close_ties',events)
        self.assertNotIn('create_faction',events)
        self.assertNotIn('declare_war_on',events)

    def test_dynamic_tags_inherit_campaigns(self):
        self.assertIn('tag = WAR',self.outputs['common/national_focus/secondary_poland.txt'])
        self.assertIn('tag = BAT',self.outputs['common/national_focus/secondary_netherlands.txt'])
        self.assertIn('tag = HOL',self.outputs['common/national_focus/secondary_netherlands.txt'])

    def test_usa_has_character_and_1789_political_baseline(self):
        text=self.outputs['history/countries/USA - United States.txt']
        self.assertIn('George Washington',text);self.assertIn('Anthony Wayne',text)
        self.assertIn('capital = 358',text);self.assertIn('ruling_party = democratic',text)

    def test_no_unapproved_territorial_effects(self):
        forbidden=('transfer_state','add_core_of','annex_country','puppet =','create_faction =','declare_war_on')
        for path,text in self.outputs.items():
            if not path.endswith('.txt'):continue
            for token in forbidden:self.assertNotIn(token,text,f'{path} contains {token}')

if __name__=='__main__':unittest.main()
