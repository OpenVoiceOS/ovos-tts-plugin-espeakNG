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


## Docker

This plugin ships a self-contained image that serves espeak-ng behind
[ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server)'s
ElevenLabs-compatible HTTP API on port `9666`. espeak-ng runs fully offline, so the
container needs no network access or API keys at runtime.

Pull the published image:

```bash
docker run --rm -p 9666:9666 ghcr.io/openvoiceos/ovos-tts-plugin-espeakng:dev
```

…or build it locally, optionally overriding the default language:

```bash
docker build -t ovos-tts-plugin-espeakng --build-arg LANG=pt .
docker run --rm -p 9666:9666 ovos-tts-plugin-espeakng
```

…or use the bundled compose file:

```bash
docker compose up
```

Synthesize speech:

```bash
curl 'http://localhost:9666/synthesize/hello%20world' --output hello.wav
```