import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from pdx import parse,walk,dumps
from build_41_major_depth import build,postprocess,THEMES,BASE_TOTALS,focus_id

class MajorDepthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files=build(ROOT)
        cls.tree=cls.files['common/national_focus/nap_major_deep_programmes.txt']
    def test_324_new_focuses_each(self):
        nodes=[n for n in parse(self.tree) if n.key=='shared_focus']
        self.assertEqual(len(nodes),1296)
        for tag in THEMES:
            self.assertEqual(sum(1 for n in nodes if n.scalar('id').startswith(tag+'_deep_')),324)
            self.assertTrue(350 <= BASE_TOTALS[tag]+324 <= 400)
    def test_36_country_specific_programmes_each(self):
        for tag,themes in THEMES.items():
            self.assertEqual(len(themes),36)
            self.assertEqual(len(set(themes)),36)
    def test_ids_and_localisation_unique(self):
        nodes=[n for n in parse(self.tree) if n.key=='shared_focus']
        ids=[n.scalar('id') for n in nodes]
        self.assertEqual(len(ids),len(set(ids)))
        loc=self.files['localisation/english/nap_major_deep_l_english.yml']
        for identifier in ids:
            self.assertIn(' '+identifier+':0 ',loc)
            self.assertIn(' '+identifier+'_desc:0 ',loc)
    def test_no_territorial_shortcuts(self):
        for token in ('transfer_state','add_core_of','annex_country','puppet =','declare_war_on'):
            self.assertNotIn(token,self.tree)
    def test_postprocess_imports_programme_roots(self):
        updates=postprocess({},ROOT)
        for tag,themes in THEMES.items():
            text=updates[f'common/national_focus/{tag}.txt']
            for theme in themes:
                self.assertIn('shared_focus = '+focus_id(tag,theme,0),text)
    def test_scripts_parse(self):
        parse(self.tree)

if __name__=='__main__':unittest.main()
