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

    def test_runtime_opinion_modifier_uses_value_key(self):
        opinions = (ROOT/'common/opinion_modifiers/nap_runtime_opinions.txt').read_text()
        self.assertIn('value = -50', opinions)
        self.assertNotRegex(opinions, r'(?m)^\s*opinion\s*=')

    def test_polish_leader_uses_valid_vanilla_subideology(self):
        text = (ROOT/'history/countries/POL - Poland.txt').read_text(encoding='utf-8-sig')
        self.assertNotIn('social_democracy', text)
        self.assertIn('ideology = conservatism', text)

    def test_deferred_capitals_are_set_after_state_transfer(self):
        prussia = (ROOT/'history/countries/PRU - Prussia.txt').read_text(encoding='utf-8-sig')
        venice = (ROOT/'history/countries/VEN - Venice.txt').read_text(encoding='utf-8-sig')
        setup = (ROOT/'common/scripted_effects/napoleonic_state_setup.txt').read_text()
        self.assertNotRegex(prussia, r'(?m)^\s*capital\s*=\s*64\b')
        self.assertNotRegex(venice, r'(?m)^\s*capital\s*=\s*160\b')
        self.assertIn('PRU = { set_capital = { state = 64 } }', setup)
        self.assertIn('VEN = { set_capital = { state = 160 } }', setup)

    def test_all_mod_declared_tags_have_history_files(self):
        tag_file = (ROOT/'common/country_tags/00_napoleonic_countries.txt').read_text()
        tags = {
            m.group(1) for m in
            (re.match(r'\s*([A-Z0-9]{3})\s*=', line) for line in tag_file.splitlines())
            if m
        }
        histories = {p.name[:3] for p in (ROOT/'history/countries').glob('*.txt')}
        self.assertFalse(tags - histories, sorted(tags - histories))

    def test_generated_tga_assets_are_32bpp(self):
        for path in (
            ROOT/'gfx/flags/FRA.tga',
            ROOT/'gfx/leaders/ENG/nap_william_pitt_the_younger.tga',
        ):
            data = path.read_bytes()
            self.assertGreaterEqual(len(data), 18, str(path))
            self.assertEqual(data[16], 32, str(path))

    def test_sound_effects_have_category(self):
        text = (ROOT/'sound/napoleonic.asset').read_text()
        self.assertIn('name = "nap_event_sfx"', text)
        for effect in ('nap_dispatch_effect','nap_crowd_effect','nap_cannon_effect'):
            self.assertIn(effect, text)

    def test_history_portrait_fields_match_leader_type(self):
        country = (ROOT/'history/countries/ENG - Great Britain.txt').read_text(encoding='utf-8-sig')
        self.assertRegex(country, r'(?s)create_country_leader\s*=\s*\{.*?picture\s*=\s*"GFX_NAP_PORTRAIT_')
        self.assertRegex(country, r'(?s)create_(?:field_marshal|corps_commander|navy_leader)\s*=\s*\{.*?gfx\s*=\s*GFX_NAP_PORTRAIT_')
        presentation = (ROOT/'interface/nap_presentation.gfx').read_text()
        self.assertIn('GFX_NAP_PORTRAIT_ENG_', presentation)
        self.assertIn('_small" texturefile = "gfx/leaders/ENG/small/', presentation)

    def test_airlike_custom_equipment_has_map_icons(self):
        text = (ROOT/'common/units/equipment/recon_corps_equipment.txt').read_text()
        expected = {
            'scout_equipment': ('light_plane', '1'),
            'courier_equipment': ('light_plane', '2'),
            'balloon_equipment': ('medium_plane', '6'),
            'intelligence_equipment': ('heavy_plane', '11'),
            'privateer_equipment': ('light_plane', '3'),
        }
        for equipment, (sprite, frame) in expected.items():
            match = re.search(
                rf'(?s)^\s*{equipment}\s*=\s*\{{(.*?)^\s*\}}',
                text,
                re.M
            )
            self.assertIsNotNone(match, equipment)
            self.assertIn(f'sprite = {sprite}', match.group(1), equipment)
            self.assertIn(f'air_map_icon_frame = {frame}', match.group(1), equipment)

    def test_opening_non_aggression_pacts_are_not_created_twice(self):
        text = (ROOT/'common/scripted_effects/napoleonic_diplomacy_setup.txt').read_text()
        targets = re.findall(
            r'diplomatic_relation\s*=\s*\{\s*country\s*=\s*([A-Z]{3})\s*relation\s*=\s*non_aggression_pact',
            text
        )
        self.assertEqual(targets.count('HAB'), 1)
        self.assertEqual(targets.count('PRU'), 1)
        self.assertEqual(targets.count('NET'), 2)
        self.assertEqual(targets.count('ENG'), 0)

    def test_custom_technology_folders_use_vanilla_ui_roots(self):
        tags = (ROOT/'common/technology_tags/00_napoleonic_tags.txt').read_text()
        cavalry = (ROOT/'common/technologies/cavalry.txt').read_text()
        recon = (ROOT/'common/technologies/recon_corps.txt').read_text()
        self.assertNotIn('technology_folders = {', tags)
        self.assertNotIn('cavalry_folder', cavalry)
        self.assertNotIn('recon_corps_folder', recon)
        self.assertIn('name = infantry_folder', cavalry)
        self.assertIn('name = support_folder', recon)

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
