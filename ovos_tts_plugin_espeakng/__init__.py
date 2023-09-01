import subprocess
from distutils.spawn import find_executable

from ovos_plugin_manager.templates.tts import TTS, TTSValidator
from ovos_utils.log import LOG


class EspeakNGTTS(TTS):
    """OVOS Text-To-Speech plugin using espeakNG"""

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            validator=EspeakNGValidator(self),
            ssml_tags=[
                "speak",
                "say-as",
                "voice",
                "audio",
                "prosody",
                "break",
                "emphasis",
                "sub",
                "tts:style",
                "p",
                "s",
                "mark",
            ]
        )
        LOG.debug(self.config)
        self.lang = self.config.get("lang") or "en-us"
        self.voice = self.config.get("voice") or "m1"
        self.amplitude = self.config.get("tts", {}).get("ovos_tts_plugin_espeakng", {}).get("amplitude")
        LOG.debug(f"Amplitude: {self.amplitude}")
        self.gap = self.config.get("gap")
        self.capital = self.config.get("capital")
        self.pitch = self.config.get("pitch")
        self.speed = self.config.get("speed")

        # allow user to override espeak binary path
        self.espeak_bin = self.config.get("binary") or \
                          find_executable("espeak-ng") or \
                          find_executable("espeak")

    def modify_tag(self, tag):
        """Override to modify each supported ssml tag"""
        if "%" in tag:
            if "-" in tag:
                val = tag.split("-")[1].split("%")[0]
                tag = tag.replace("-", "").replace("%", "")
                new_val = str(int(val) / 100)
                tag = tag.replace(val, new_val)
            elif "+" in tag:
                val = tag.split("+")[1].split("%")[0]
                tag = tag.replace("+", "").replace("%", "")
                new_val = str(int(val) / 100)
                tag = tag.replace(val, new_val)
        return tag

    def get_tts(self, sentence, wav_file, lang=None):
        """Make TTS request and create a wav file with the response"""
        lang = lang or self.lang
        subprocess.call(
            [self.espeak_bin, '-m', "-w", wav_file, '-v', lang + '+' +
             self.voice, sentence])
        return wav_file, None

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return set(_get_voices().keys())


class EspeakNGValidator(TTSValidator):
    def __init__(self, tts):
        super(EspeakNGValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO
        pass

    def validate_connection(self):
        if not self.tts.espeak_bin:
            raise ImportError('espeak-ng executable not found. '
                              'please install espeak-ng')

    def get_tts_class(self):
        return EspeakNGTTS


def _get_voices():
    """ helper method to populate plugin voice list """
    espeak = find_executable("espeak-ng") or find_executable("espeak")
    if not espeak:
        # espeak-ng not installed, do not report invalid config options
        return {}

    voice_data = {}
    v = subprocess.check_output([espeak, '--voices']).decode("utf-8")
    for vd in v.split("\n")[1:]:  # skip header
        # this cleans all the extra spaces
        vd = " ".join((_ for _ in vd.split() if _))
        if not vd:
            continue

        # parse relevant keys
        _, lang, _, name, *_ = vd.split(" ")
        name = name.replace("_", " ").title()
        lang2 = lang  # espeak key

        # TODO lang codes should be normalized better
        if len(lang) == 3:
            # what do? 3 letter codes not supported by ovos
            continue
        # merge dialects to the main lang
        if len(lang.split("-")) > 2 or \
                any((len(_) != 2 for _ in lang.split("-"))):

            # hack to keep english subdialects sorted
            if lang[:5] in ["en-us", "en-gb"]:
                lang = lang[:5]
            else:
                lang = lang.split("-")[0]

        if lang not in voice_data:
            voice_data[lang] = []

        # add male/female variants to list
        voice_data[lang].append({
            'voice': "m1",
            "lang": lang2,
            "meta": {
                'display_name': name + " Male",
                'gender': "male",
                "priority": 90,
                "offline": True}
        })
        voice_data[lang].append({
            'voice': "f1",
            "lang": lang2,
            "meta": {'display_name': name + " Female",
                     'gender': "female",
                     "priority": 90,
                     "offline": True}
        })

    return voice_data


EspeakNGTTSPluginConfig = _get_voices()

if __name__ == "__main__":
    e = EspeakNGTTS()
    e.validator.validate_connection()

    ssml = """Hello world"""
    e.get_tts(ssml, "espeak.wav")
