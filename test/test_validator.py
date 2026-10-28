"""The validator's rejection path, and its exception type.

`validate_connection` raised `ImportError` when the espeak-ng executable was
absent. Nothing failed to import: a system package is missing. The type is
asserted here so a later rewrite of this message cannot quietly put the wrong
class back.

The plugin loader (`ovos_plugin_manager.tts`) catches `Exception` around
`validate()` and re-raises without reading the type, and nothing in the
organisation matches on this message or on the old class, both checked by grep
before the change. So the effect is on a caller's ability to tell the two
failures apart, not on the loader.

T-5157 chose `RuntimeError` for the same condition in ovos-tts-plugin-pico.
"""
import unittest

from ovos_tts_plugin_espeakng import EspeakNGValidator


class _FakeTTS:
    """The validator reads tts.espeak_bin and nothing else."""

    def __init__(self, espeak_bin):
        self.espeak_bin = espeak_bin


class TestValidateConnection(unittest.TestCase):
    def test_a_missing_binary_raises_runtimeerror(self):
        validator = EspeakNGValidator(_FakeTTS(None))
        with self.assertRaises(RuntimeError) as caught:
            validator.validate_connection()
        self.assertIn("espeak-ng executable not found", str(caught.exception))

    def test_it_is_not_an_importerror(self):
        """The same statement from the other side.

        An `except ImportError` elsewhere is the accident that motivated the
        change, so the class is named here rather than only implied by the
        RuntimeError assertion above.
        """
        validator = EspeakNGValidator(_FakeTTS(None))
        with self.assertRaises(RuntimeError) as caught:
            validator.validate_connection()
        self.assertNotIsInstance(caught.exception, ImportError)

    def test_a_present_binary_is_accepted(self):
        """The control. Without it a validator that rejected everything would
        pass the test above."""
        validator = EspeakNGValidator(_FakeTTS("/usr/bin/espeak-ng"))
        self.assertIsNone(validator.validate_connection())


if __name__ == "__main__":
    unittest.main()
