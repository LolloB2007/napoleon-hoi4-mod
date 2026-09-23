import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from pdx import parse,walk
from build_60_secondary import build as base_build,PROFILES
from build_61_secondary_depth import build,postprocess,generated,GERMAN_PERSONALISED

class SecondaryDepthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base=base_build(ROOT)
        cls.depth=build(ROOT)
        cls.outputs=base|cls.depth|postprocess(base|cls.depth,ROOT)

    def test_effective_campaign_size(self):
        for profile in PROFILES:
            path=f'common/national_focus/secondary_{profile["slug"]}.txt'
            nodes=[n for n in walk(parse(self.outputs[path])) if n.key=='focus' and isinstance(n.value,list) and n.scalar('id')]
            if profile['slug']=='german_princes':
                self.assertEqual(len(nodes),403)
                _,meta=generated(profile)
                generic=sum(1 for row in meta if not row['personalised'])
                self.assertEqual(generic,114)
                for tag in profile['tags']:
                    self.assertEqual(23+generic+sum(1 for row in meta if row['personalised_tag']==tag),175)
            else:
                self.assertEqual(len(nodes),175,profile['slug'])

    def test_38_personalised_focuses_per_country(self):
        for profile in PROFILES:
            _,meta=generated(profile)
            if profile['slug']=='german_princes':
                for tag in profile['tags']:
                    self.assertEqual(sum(1 for row in meta if row['personalised_tag']==tag),38)
            else:
                self.assertEqual(len(meta),152)
                self.assertEqual(sum(1 for row in meta if row['personalised']),38)

    def test_german_personalised_branches_are_hidden_for_other_tags(self):
        text=self.outputs['common/national_focus/secondary_german_princes.txt']
        for tag,branches in GERMAN_PERSONALISED.items():
            root=generated(next(p for p in PROFILES if p['slug']=='german_princes'))[1]
            first_id=next(row['id'] for row in root if row['personalised_tag']==tag)
            from pdx import dumps
            node=next(n for n in walk(parse(text)) if n.key=='focus' and n.scalar('id')==first_id)
            self.assertIn(f'allow_branch = {{\n\t\ttag = {tag}',dumps([node]))

    def test_new_focus_ids_unique(self):
        ids=[]
        for profile in PROFILES:
            ids += [row['id'] for row in generated(profile)[1]]
        self.assertEqual(len(ids),len(set(ids)))

    def test_localisation_covers_new_focuses(self):
        loc=self.depth['localisation/english/nap_secondary_depth_l_english.yml']
        for profile in PROFILES:
            for row in generated(profile)[1]:
                self.assertIn(' '+row['id']+':0 ',loc)
                self.assertIn(' '+row['id']+'_desc:0 ',loc)

    def test_no_territorial_shortcuts(self):
        for profile in PROFILES:
            path=f'common/national_focus/secondary_{profile["slug"]}.txt'
            text=self.outputs[path]
            for token in ('transfer_state','add_core_of','annex_country','puppet =','create_faction =','declare_war_on'):
                self.assertNotIn(token,text)

    def test_expanded_scripts_parse(self):
        for profile in PROFILES:
            parse(self.outputs[f'common/national_focus/secondary_{profile["slug"]}.txt'])

if __name__=='__main__':unittest.main()
