import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from pdx import parse, Entry, validate_graph

class ParserTests(unittest.TestCase):
    def test_comments_do_not_close_blocks(self):
        with self.assertRaises(ValueError):
            parse('SPR = { # stashed }')
    def test_quoted_braces_and_comments(self):
        self.assertEqual(parse('name = "{ # not syntax }"')[0].value, '{ # not syntax }')
    def test_lists_and_duplicate_keys(self):
        entries = parse('x = { a b key = 1 key = 2 }')[0].value
        self.assertEqual([e.key for e in entries], ['a', 'b', 'key', 'key'])
    def test_unterminated_string(self):
        with self.assertRaises(ValueError):
            parse('name = "unterminated')
    def test_operator(self):
        self.assertEqual(parse('value > 2')[0].op, '>')
    def test_missing_reference(self):
        with self.assertRaises(ValueError):
            validate_graph({'a': Entry('focus', [Entry('prerequisite', [Entry('focus', 'missing')])])})
    def test_cycle(self):
        with self.assertRaises(ValueError):
            validate_graph({k: Entry('focus', [Entry('prerequisite', [Entry('focus', v)])]) for k,v in [('a','b'),('b','a')]})
    def test_bom(self):
        self.assertEqual(parse('\ufeffx = yes')[0].value, 'yes')

if __name__ == '__main__':
    unittest.main()
