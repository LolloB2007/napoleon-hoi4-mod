import tempfile
import unittest
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'content')]
from build_98_localisation_policy import validate_localisation_policy

class LocalisationPolicyTests(unittest.TestCase):
    def test_repository_is_english_only(self):
        validate_localisation_policy(ROOT)

    def test_generated_non_english_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'localisation/english').mkdir(parents=True)
            (root/'localisation/english/base_l_english.yml').write_text('\ufeffl_english:\n x:0 "X"\n',encoding='utf-8')
            with self.assertRaises(ValueError):
                validate_localisation_policy(root,{'localisation/french/x_l_french.yml':'\ufeffl_french:\n x:0 "X"\n'})

    def test_generated_english_with_bom_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'localisation/english').mkdir(parents=True)
            validate_localisation_policy(root,{'localisation/english/x_l_english.yml':'\ufeffl_english:\n x:0 "X"\n'})

    def test_bad_english_header_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'localisation/english').mkdir(parents=True)
            (root/'localisation/english/bad.yml').write_text('l_french:\n x:0 "X"\n')
            with self.assertRaises(ValueError):
                validate_localisation_policy(root)

if __name__=='__main__': unittest.main()
