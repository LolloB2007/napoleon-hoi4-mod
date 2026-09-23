import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from pdx import parse,walk
from build_60_secondary import build as base_build,PROFILES
from build_61_secondary_depth import build,postprocess,generated

class SecondaryDepthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base=base_build(ROOT)
        cls.depth=build(ROOT)
        cls.outputs=base|cls.depth|postprocess(base|cls.depth,ROOT)

    def test_every_campaign_has_175_focuses(self):
        for profile in PROFILES:
            path=f'common/national_focus/secondary_{profile["slug"]}.txt'
            nodes=[n for n in walk(parse(self.outputs[path])) if n.key=='focus' and isinstance(n.value,list) and n.scalar('id')]
            self.assertEqual(len(nodes),175,profile['slug'])

    def test_152_new_and_38_personalised_each(self):
        for profile in PROFILES:
            _,meta=generated(profile)
            self.assertEqual(len(meta),152)
            self.assertEqual(sum(1 for row in meta if row['personalised']),38)

    def test_new_focus_ids_unique(self):
        ids=[]
        for profile in PROFILES:
            ids += [row['id'] for row in generated(profile)[1]]
        self.assertEqual(len(ids),13*152)
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
