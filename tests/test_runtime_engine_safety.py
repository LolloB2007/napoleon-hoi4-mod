import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def event_blocks(text):
    for match in re.finditer(r'(?m)^\s*(?:country_event|news_event)\s*=\s*\{', text):
        brace = text.find('{', match.start())
        depth = 0
        for pos in range(brace, len(text)):
            if text[pos] == '{':
                depth += 1
            elif text[pos] == '}':
                depth -= 1
                if depth == 0:
                    yield text[match.start():pos + 1]
                    break


class RuntimeEngineSafetyTests(unittest.TestCase):
    def test_vanilla_ideology_database_is_not_overridden(self):
        self.assertFalse((ROOT/'common/ideologies/00_ideologies.txt').exists())

    def test_event_calls_do_not_contain_picture_tokens(self):
        for name in ('01_french_revolution.txt', '02_napoleonic_wars.txt', '03_collapse.txt'):
            text = (ROOT/'events'/name).read_text(encoding='utf-8-sig')
            for block in event_blocks(text):
                is_definition = re.search(r'(?m)^\s*(?:title|desc)\s*=', block)
                if not is_definition:
                    self.assertNotRegex(block, r'(?m)^\s*picture\s*=', name)

    def test_geography_startup_has_country_scope(self):
        text = (ROOT/'common/on_actions/nap_geography.txt').read_text()
        self.assertIn('FRA = { nap_geography_initialize = yes }', text)

    def test_doctrines_use_current_cost_key_and_scoped_terrain(self):
        text = (ROOT/'common/technologies/land_doctrine.txt').read_text()
        self.assertNotIn('xp_research_cost', text)
        self.assertIsNone(re.search(
            r'(?m)^\t\t(?:hills|forest|urban|fort|mountain|jungle)\s*=\s*\{',
            text
        ))

    def test_invalid_equipment_bonus_enums_are_removed(self):
        for name in ('ENG.txt', 'FRA.txt', 'PRU.txt', 'RUS.txt'):
            text = (ROOT/'common/ideas'/name).read_text()
            self.assertNotIn('equipment_bonus = {', text, name)

    def test_runtime_opinion_modifier_is_defined(self):
        focus = (ROOT/'common/national_focus/RUS.txt').read_text()
        opinions = (ROOT/'common/opinion_modifiers/nap_runtime_opinions.txt').read_text()
        self.assertIn('modifier = nap_rus_anglophobe_opinion', focus)
        self.assertIn('nap_rus_anglophobe_opinion = {', opinions)

    def test_credits_are_not_in_engine_parsed_music_txt(self):
        self.assertFalse((ROOT/'music/Credits.txt').exists())
        self.assertTrue((ROOT/'docs/music-credits.md').exists())

    def test_duplicate_vanilla_reign_of_terror_idea_is_not_defined(self):
        text = (ROOT/'common/ideas/FRA_dynamic.txt').read_text()
        self.assertNotIn('reign_of_terror = {', text)

    def test_dynamic_leaders_do_not_use_gfx_sprite_as_portrait_filename(self):
        for root in ('events', 'common/national_focus'):
            for path in (ROOT/root).glob('*.txt'):
                text = path.read_text(encoding='utf-8-sig')
                self.assertNotIn('picture = GFX_NAP_PORTRAIT_', text, str(path))

    def test_custom_subunits_do_not_override_vanilla_ids(self):
        infantry = (ROOT/'common/units/napoleonic_infantry.txt').read_text()
        support = (ROOT/'common/units/napoleonic_support.txt').read_text()
        self.assertNotRegex(infantry, r'(?m)^\s*militia\s*=\s*\{')
        self.assertIn('nap_militia = {', infantry)
        self.assertNotRegex(support, r'(?m)^\s*field_hospital\s*=\s*\{')
        self.assertIn('nap_field_hospital = {', support)


if __name__ == '__main__':
    unittest.main()
