import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'content'))
from build_00_contracts import build, COUNTRIES
from pdx import parse

class BuildTests(unittest.TestCase):
    def test_namespace_unique(self):
        tags = [r.split('|')[0] for r in COUNTRIES.splitlines()]
        self.assertEqual(len(tags), 68)
        self.assertEqual(len(tags), len(set(tags)))
    def test_contracts_parse(self):
        for path, text in build(ROOT).items():
            if path.endswith(('.txt','.gfx')):
                parse(text)
    def test_flags_sizes(self):
        files = build(ROOT)
        self.assertEqual(len(files['gfx/flags/FRA.tga']), 18 + 82 * 52 * 3)
        self.assertEqual(len(files['gfx/flags/medium/FRA.tga']), 18 + 41 * 26 * 3)
        self.assertEqual(len(files['gfx/flags/small/FRA.tga']), 18 + 10 * 7 * 3)
    def test_localisation_bom(self):
        for path, text in build(ROOT).items():
            if path.endswith('.yml'):
                self.assertTrue(text.startswith('\ufeffl_english:'))

if __name__ == '__main__':
    unittest.main()
