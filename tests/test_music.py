import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class MusicTests(unittest.TestCase):
    def test_a11_vorbis_assets_present(self):
        for name in ('nap_council_of_europe.ogg','nap_marseillaise_rendering.ogg'):
            data=(ROOT/'music'/name).read_bytes()
            self.assertTrue(data.startswith(b'OggS'),name)
            self.assertGreater(len(data),4000,name)

    def test_asset_and_playlist_registration(self):
        asset=(ROOT/'music/napoleonic_music.asset').read_text()
        playlist=(ROOT/'music/napoleonic_songs.txt').read_text()
        for title in ('Napoleonic Era - Council of Europe','Napoleonic Era - La Marseillaise Rendering'):
            self.assertIn(f'name = "{title}"',asset)
            self.assertIn(f'song = "{title}"',playlist)
        self.assertIn('music_station = "base_music"',playlist)

    def test_provenance_separates_composition_and_recording(self):
        text=(ROOT/'music/Credits.txt').read_text()
        self.assertIn('original composition',text)
        self.assertIn('public-domain composition',text)
        self.assertIn('source recording: none',text)
        self.assertIn('No commercial or third-party recording',text)

if __name__=='__main__': unittest.main()
