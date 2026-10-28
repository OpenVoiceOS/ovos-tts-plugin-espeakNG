import os
import wave
import tempfile
import unittest

from ovos_tts_plugin_espeakng import EspeakNGTTS, _get_voices


class TestModifyTag(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tts = EspeakNGTTS()

    def test_percentage_increase_tag(self):
        # +50% should become a +0.5 style fraction with markup chars stripped
        out = self.tts.modify_tag('rate+50%')
        self.assertNotIn("%", out)
        self.assertIn("0.5", out)

    def test_percentage_decrease_tag(self):
        out = self.tts.modify_tag('rate-25%')
        self.assertNotIn("%", out)
        self.assertIn("0.25", out)

    def test_tag_without_percent_unchanged(self):
        self.assertEqual(self.tts.modify_tag("speak"), "speak")


class TestEspeakNGTTS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tts = EspeakNGTTS()

    def test_binary_resolved(self):
        self.assertTrue(self.tts.espeak_bin)
        self.assertTrue(os.path.basename(self.tts.espeak_bin).startswith("espeak"))

    def test_voices_discovered(self):
        voices = _get_voices()
        self.assertTrue(voices, "espeak-ng reported no voices")
        # english must be available
        self.assertTrue(any(k.startswith("en") for k in voices))

    def test_available_languages(self):
        langs = self.tts.available_languages
        self.assertTrue(langs)
        self.assertTrue(any(l.startswith("en") for l in langs))

    def test_get_tts_creates_valid_wav(self):
        path = os.path.join(tempfile.mkdtemp(), "espeak_out.wav")
        wav_file, _ = self.tts.get_tts("Hello world", path)
        self.assertTrue(os.path.isfile(wav_file))
        self.assertGreater(os.path.getsize(wav_file), 0)
        with wave.open(wav_file, "rb") as f:
            self.assertGreater(f.getnframes(), 0)
            self.assertGreater(f.getframerate(), 0)


if __name__ == "__main__":
    unittest.main()
