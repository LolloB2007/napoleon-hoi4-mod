import re
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'content')]
from build_content import compile_sources
from build_00_contracts import COUNTRIES

class PresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.outputs=compile_sources(ROOT)

    def text(self,path):
        return self.outputs[path].decode('utf-8-sig')

    def test_focus_icons_are_custom_and_unique_by_id(self):
        focus_paths=[p for p in self.outputs if p.startswith('common/national_focus/') and p.endswith('.txt')]
        from pdx import parse, walk
        ids=[]; icons=[]
        for path in focus_paths:
            for node in walk(parse(self.text(path))):
                if node.key!='focus' or not isinstance(node.value,list):
                    continue
                fid=node.scalar('id')
                if not fid:
                    continue
                ids.append(fid)
                icon=node.scalar('icon')
                self.assertIsNotNone(icon,path+': '+fid)
                self.assertTrue(icon.startswith('GFX_NAP_FOCUS_'),path+': '+fid+' -> '+icon)
                icons.append(icon)
        # The parser deliberately skips some compact/generated focus forms, so
        # validate complete file-level coverage independently of a hardcoded
        # repository-wide count.
        raw_focus_count=0
        raw_custom_icon_count=0
        for path in focus_paths:
            raw=self.text(path)
            raw_focus_count += len(re.findall(r'(?m)^\\s*focus\\s*=\\s*\\{',raw))
            raw_custom_icon_count += len(re.findall(r'\\bicon\\s*=\\s*GFX_NAP_FOCUS_[A-Z0-9_]+',raw))
        self.assertGreaterEqual(raw_focus_count,800)
        self.assertEqual(raw_custom_icon_count,raw_focus_count)
        self.assertEqual(len(icons),len(ids))
        self.assertEqual(len(set(icons)),len(icons))

    def test_event_blocks_have_period_art(self):
        for path in [p for p in self.outputs if p.startswith('events/') and p.endswith('.txt')]:
            text=self.text(path)
            count=len(re.findall(r'(?m)^\s*(?:country_event|news_event)\s*=\s*\{',text))
            pics=len(re.findall(r'\bpicture\s*=\s*GFX_NAP_EVENT_\d\d',text))
            self.assertEqual(pics,count,path)

    def test_inline_leaders_have_portraits(self):
        paths=[p for p in self.outputs if (p.startswith('history/countries/') or p.startswith('events/') or p.startswith('common/national_focus/')) and p.endswith('.txt')]
        for path in paths:
            text=self.text(path)
            for m in re.finditer(r'create_(?:country_leader|field_marshal|corps_commander|navy_leader)\s*=\s*\{',text):
                block=text[m.start():text.find('}',m.start())+1]
                self.assertIn('picture = GFX_NAP_PORTRAIT_',block,path)

    def test_regime_flags_cover_namespace(self):
        tags=[r.split('|')[0] for r in COUNTRIES.splitlines()]
        for tag in tags:
            for suffix in ('','_neutrality','_democratic','_communism','_fascism'):
                for folder in ('','medium/','small/'):
                    self.assertIn(f'gfx/flags/{folder}{tag}{suffix}.tga',self.outputs)

    def test_loading_screens_and_bookmark_are_binary_assets(self):
        for i in range(1,4):
            data=self.outputs[f'gfx/loadingscreens/load_napoleonic_{i}.dds']
            self.assertTrue(data.startswith(b'DDS '))
            self.assertGreater(len(data),100000)
        self.assertTrue(self.outputs['gfx/interface/select_date_napoleonic.tga'].startswith(b'\x00\x00\x02'))

    def test_event_audio_is_generated_and_registered(self):
        for name in ('dispatch','crowd','cannon'):
            data=self.outputs[f'sound/nap_{name}.wav']
            self.assertTrue(data.startswith(b'RIFF'))
        asset=self.text('sound/napoleonic.asset')
        self.assertIn('nap_dispatch_effect',asset)
        self.assertIn('nap_cannon_effect',asset)

    def test_flavour_events_exist(self):
        text=self.text('events/10_flavour.txt')
        self.assertEqual(len(re.findall(r'(?m)^country_event\s*=\s*\{',text)),12)
        self.assertIn('scoped_sound_effect = "nap_dispatch_effect"',text)

    def test_historical_namelists_exist(self):
        div=self.text('common/units/names_divisions/napoleonic_names_divisions.txt')
        ships=self.text('common/units/names_ships/napoleonic_ship_names.txt')
        for tag in ('FRA','ENG','HAB','PRU','RUS','SPR','POR','TUR','SWE','DEN','POL','NET','VEN','USA'):
            self.assertIn(f'{tag}_NAP_INF',div)
        for tag in ('FRA','ENG','RUS','SPR','POR','SWE','DEN','NET','VEN','TUR','USA'):
            self.assertIn(f'{tag}_NAP_SAIL',ships)

    def test_oob_templates_use_namelists(self):
        for path in [p for p in self.outputs if p.startswith('history/units/') and p.endswith('.txt')]:
            tag=Path(path).name[:3]
            if tag not in ('BAV','DEN','HAN','NAP','NET','PAP','POL','POR','SAR','SAX','SPR','SWE','TUR','TUS','VEN','WUR'):
                continue
            text=self.text(path)
            templates=len(re.findall(r'(?m)^division_template\s*=\s*\{',text))
            groups=len(re.findall(r'division_names_group\s*=',text))
            self.assertEqual(groups,templates,path)

    def test_english_localisation_has_no_obvious_generation_markers(self):
        bad=('placeholder','the the ','advances the Spain campaign while preserving','advances the Polish State campaign while preserving','balance values remain provisional','Numeric balance remains provisional')
        for path in [p for p in self.outputs if p.startswith('localisation/english/') and p.endswith('.yml')]:
            text=self.text(path)
            for token in bad:
                self.assertNotIn(token,text,path)

    def test_asset_provenance_is_explicit(self):
        text=self.text('docs/asset-provenance.md')
        self.assertIn('original procedural',text)
        self.assertIn('No external painting',text)

if __name__=='__main__':
    unittest.main()
