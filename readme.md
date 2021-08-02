## Description

OpenVoiceOS TTS plugin for [espeak-ng](https://github.com/espeak-ng/espeak-ng)

## Install

```bash
pip install ovos_tts_plugin_espeakng
```

`espeak-ng` needs to be available

```bash
apt-get install espeak-ng
```


## Configuration

```json
  "tts": {
    "module": "ovos_tts_plugin_espeakng",
    "ovos_tts_plugin_espeakng": {
      "voice": "m1"
    }
 }
```
