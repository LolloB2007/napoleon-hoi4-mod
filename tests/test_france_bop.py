import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "content"))

from pdx import parse, dumps, walk
from build_22_france_bop import build, BOP_ID, NAPOLEON, ASSEMBLIES, MARSHALS, CATEGORY
from build_21_france_decisions import build as build_decisions


class FranceBalanceOfPowerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files = build(ROOT)
        cls.bop = parse(cls.files["common/bop/nap_france_personal_rule.txt"])[0]

    def test_generated_scripts_parse(self):
        for path, text in self.files.items():
            if path.endswith(".txt"):
                parse(text)

    def test_three_sides_and_default_counterweight(self):
        self.assertEqual(self.bop.key, BOP_ID)
        self.assertEqual(self.bop.scalar("left_side"), NAPOLEON)
        self.assertEqual(self.bop.scalar("right_side"), ASSEMBLIES)
        sides = {side.scalar("id") for side in self.bop.children("side")}
        self.assertEqual(sides, {NAPOLEON, ASSEMBLIES, MARSHALS})
        self.assertEqual(self.bop.scalar("decision_category"), CATEGORY)

    def test_ranges_cover_entire_bar_for_each_active_pair(self):
        root_ranges = [(float(r.scalar("min")), float(r.scalar("max"))) for r in self.bop.children("range")]
        self.assertEqual(root_ranges, [(-0.2, 0.2)])
        by_side = {}
        for side in self.bop.children("side"):
            by_side[side.scalar("id")] = [(float(r.scalar("min")), float(r.scalar("max"))) for r in side.children("range")]
        self.assertEqual(by_side[NAPOLEON], [(-1.0, -0.6), (-0.6, -0.2)])
        self.assertEqual(by_side[ASSEMBLIES], [(0.2, 0.6), (0.6, 1.0)])
        self.assertEqual(by_side[MARSHALS], [(0.2, 0.6), (0.6, 1.0)])

    def test_marshalate_replaces_assemblies_after_appointment(self):
        effects = self.files["common/scripted_effects/nap_france_bop.txt"]
        self.assertIn("has_country_flag = nap_fra_marshals_appointed", effects)
        self.assertIn("right_side = nap_fra_bop_marshals", effects)
        self.assertIn("right_side = nap_fra_bop_assemblies", effects)
        self.assertIn("has_country_flag = hundred_days", effects)
        self.assertIn("remove_power_balance", effects)

    def test_historical_shocks_and_drift_are_wired(self):
        effects = self.files["common/scripted_effects/nap_france_bop.txt"]
        for token in (
            "nap_legacy_napoleonic_wars_6_settled",
            "nap_legacy_napoleonic_wars_9_settled",
            "nap_legacy_napoleonic_wars_13_settled",
            "trafalgar_fought",
            "grande_armee_destroyed",
            "waterloo_fought",
            "nap_fra_napoleon_prestige > 84",
            "nap_war_exhaustion > 74",
        ):
            self.assertIn(token, effects)

    def test_russia_interacts_with_command_balance(self):
        triggers = self.files["common/scripted_triggers/nap_france_bop.txt"]
        effects = self.files["common/scripted_effects/nap_france_bop.txt"]
        self.assertIn("nap_fra_bop_can_force_major_campaign", triggers)
        self.assertIn("nap_fra_bop_override_marshals", triggers)
        self.assertIn("nap_fra_russian_supply = -4", effects)
        self.assertIn("nap_fra_russian_supply = 2", effects)

        france = build_decisions(ROOT)
        decisions = france["common/decisions/nap_france_campaigns.txt"]
        self.assertIn("nap_fra_bop_can_force_major_campaign = yes", decisions)
        press = next(e for e in walk(parse(decisions)) if e.key == "nap_fra_russia_press_on")
        self.assertIn("nap_fra_bop_can_force_major_campaign", dumps(press.children("available")))

    def test_abdication_crisis_has_two_responses(self):
        decisions = self.files["common/decisions/nap_france_bop.txt"]
        self.assertIn("nap_fra_bop_marshals_demand_abdication", decisions)
        self.assertIn("nap_fra_bop_fight_on", decisions)
        effects = self.files["common/scripted_effects/nap_france_bop.txt"]
        self.assertIn("id = napoleonic_collapse.5", effects)
        self.assertIn("add_manpower = 75000", effects)

    def test_bop_decisions_are_bound_to_bop_category(self):
        category = parse(self.files["common/decisions/categories/nap_france_bop.txt"])[0]
        self.assertEqual(category.key, CATEGORY)
        self.assertIn(BOP_ID, dumps(category.children("visible")))
        decisions = parse(self.files["common/decisions/nap_france_bop.txt"])[0]
        self.assertEqual(len(decisions.value), 10)

    def test_localisation_and_docs_explain_asymmetric_tradeoff(self):
        loc = self.files["localisation/english/nap_france_bop_l_english.yml"]
        self.assertTrue(loc.startswith("\ufeffl_english:"))
        for key in (BOP_ID, NAPOLEON, ASSEMBLIES, MARSHALS, CATEGORY):
            self.assertIn(" "+key+":0 ", loc)
        docs = self.files["docs/france-balance-of-power.md"]
        self.assertIn("Napoleon vs. the Assemblies", docs)
        self.assertIn("Marshalate transition", docs)
        self.assertIn("higher offensive ceiling", docs)


if __name__ == "__main__":
    unittest.main()
