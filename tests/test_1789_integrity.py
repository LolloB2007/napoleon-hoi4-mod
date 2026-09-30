import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "content")]

from pdx import load, walk, focus_graph, validate_graph


MAJORS = ("FRA", "ENG", "HAB", "PRU", "RUS")
EARLY_FILES = (
    "common/national_focus/FRA.txt",
    "common/decisions/nap_france_campaigns.txt",
    "common/scripted_effects/nap_france_campaigns.txt",
    "common/on_actions/nap_france_campaigns.txt",
    "events/01_french_revolution.txt",
    "events/02_napoleonic_wars.txt",
    "events/03_collapse.txt",
    "events/04_1789_diplomacy.txt",
)


class EarlyCampaignIntegrityTests(unittest.TestCase):
    def test_major_starting_oobs_exist_parse_and_are_loaded(self):
        for tag in MAJORS:
            oob = ROOT / "history" / "units" / f"{tag}_1789.txt"
            self.assertTrue(oob.is_file(), tag)
            load(oob)
            country = next((p for p in (ROOT / "history" / "countries").glob(f"{tag} -*.txt")), None)
            self.assertIsNotNone(country, tag)
            text = country.read_text(encoding="utf-8-sig")
            self.assertRegex(text, rf"\boob\s*=\s*[\"']?{tag}_1789[\"']?")

    def test_all_land_oob_references_resolve(self):
        references = set()
        roots = (ROOT / "history" / "countries", ROOT / "events", ROOT / "common")
        pattern = re.compile(r"\b(?:oob|set_oob|load_oob)\s*=\s*[\"']?([A-Za-z0-9_.-]+)")
        for base in roots:
            for path in base.rglob("*.txt"):
                text = path.read_text(encoding="utf-8-sig")
                references.update(pattern.findall(text))
        missing = sorted(name for name in references if not (ROOT / "history" / "units" / f"{name}.txt").is_file())
        self.assertEqual(missing, [])

    def test_early_event_calls_resolve(self):
        defined = set()
        for path in (ROOT / "events").glob("*.txt"):
            for node in load(path):
                if node.key in ("country_event", "news_event", "state_event") and isinstance(node.value, list):
                    identifier = node.scalar("id")
                    if identifier:
                        defined.add(identifier)

        references = set()
        for rel in EARLY_FILES:
            for node in walk(load(ROOT / rel)):
                if node.key in ("country_event", "news_event", "state_event") and isinstance(node.value, list):
                    identifier = node.scalar("id")
                    if identifier:
                        references.add(identifier)

        self.assertEqual(sorted(references - defined), [])

    def test_focus_graph_is_reachable_by_reference(self):
        validate_graph(focus_graph(ROOT))


if __name__ == "__main__":
    unittest.main()
