## Description

OpenVoiceOS TTS plugin for [espeak-ng](https://github.com/espeak-ng/espeak-ng)

## Install

```bash
pip install jarbas_plugin_espeakNG_tts
```

`espeak-ng` needs to be available

```bash
apt-get install espeak-ng
```


## Configuration

```json
  "tts": {
    "module": "espeakNG_tts_plugin",
    "espeakNG_tts_plugin": {
      "voice": "m1"
    }
 }
```
