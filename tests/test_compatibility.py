import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from pdx import parse
from build_08_compatibility import build

class CompatibilityTests(unittest.TestCase):
    def test_a08_requires_la_resistance(self):
        files=build(ROOT)
        self.assertIn('has_dlc = "La Resistance"',files['common/scripted_triggers/nap_compatibility.txt'])
        self.assertIn('La Résistance',files['docs/compatibility.md'])
    def test_compatibility_scripts_parse(self):
        for path,text in build(ROOT).items():
            if path.endswith('.txt'): parse(text)
    def test_descriptor_targets_119_and_documents_requirement(self):
        text=(ROOT/'descriptor.mod').read_text()
        self.assertIn('supported_version="1.19.*"',text)
        self.assertIn('Required DLC: La Resistance',text)

if __name__=='__main__': unittest.main()
