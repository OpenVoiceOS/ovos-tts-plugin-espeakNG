import subprocess

from ovos_plugin_manager.templates.tts import TTS, TTSValidator


class EspeakNGTTS(TTS):
    def __init__(self, *args, **kwargs):
        if "lang" not in kwargs:
            kwargs["lang"] = "en-us"
        if "config" not in kwargs:
            kwargs["config"] = {}
        super().__init__(*args, **kwargs,
                         validator=EspeakNGValidator(self),
                         ssml_tags=["speak", "say-as", "voice",
                                    "audio", "prosody", "break",
                                    "emphasis", "sub",
                                    "tts:style", "p", "s",
                                    "mark"])
        self.voice = self.voice or "m1"

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

    def get_tts(self, sentence, wav_file):
        subprocess.call(
            ['espeak-ng', '-m', "-w", wav_file, '-v', self.lang + '+' +
             self.voice, sentence])
        return wav_file, None


class EspeakNGValidator(TTSValidator):
    def __init__(self, tts):
        super(EspeakNGValidator, self).__init__(tts)

    def validate_lang(self):
        # TODO
        pass

    def validate_connection(self):
        try:
            subprocess.call(['espeak-ng', '--version'])
        except:
            raise Exception(
                'ESpeak is not installed. Run: sudo apt-get install espeak-ng')

    def get_tts_class(self):
        return EspeakNGTTS


if __name__ == "__main__":
    e = EspeakNGTTS()

    ssml = """Hello world"""
    e.get_tts(ssml, "espeak.wav")
