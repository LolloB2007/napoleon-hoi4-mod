import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from pdx import parse,dumps
from build_65_geography import build,EUROPE
from build_10_era import TAGS

class GeographyTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'content/geographic_scope.json').read_text())
        self.files=build(ROOT)
    def test_scripts_parse(self):
        for path,text in self.files.items():
            if path.endswith('.txt'): parse(text)
    def test_approved_scope_tags_use_era_mechanics(self):
        required={t for tags in self.data['meaningful_groups'].values() for t in tags}
        self.assertTrue(required.issubset(set(TAGS)))
    def test_colonies_use_puppet_relationships(self):
        text=self.files['common/scripted_effects/nap_geography.txt']
        for row in self.data['colonial_subjects']:
            self.assertIn('puppet = '+row['subject'],text)
    def test_outside_scope_is_explicitly_abstracted(self):
        trigger=self.files['common/scripted_triggers/nap_geography.txt']
        self.assertIn('nap_geography_outside_scope_country',trigger)
        self.assertIn('nap_outside_scope_inert',self.files['common/ideas/nap_geography.txt'])
    def test_scope_contains_required_regions(self):
        for key in ('north_africa','north_america','india'):
            self.assertTrue(self.data['meaningful_groups'][key])

if __name__=='__main__': unittest.main()
