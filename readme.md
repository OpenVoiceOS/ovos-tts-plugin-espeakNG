## Description

This plugin adds [espeak-ng](https://github.com/espeak-ng/espeak-ng) as a text-to-speech
engine for OpenVoiceOS. espeak-ng runs fully offline and supports many languages and
voices. The plugin registers with
[ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) so any OVOS
component can select it as a TTS backend.

## Install

```bash
pip install ovos_tts_plugin_espeakng
```

The plugin needs the `espeak-ng` executable. Install it with:

```bash
apt-get install espeak-ng
```

## Configuration

Add this block to your OVOS configuration to select the plugin and a voice:

```json
  "tts": {
    "module": "ovos_tts_plugin_espeakng",
    "ovos_tts_plugin_espeakng": {
      "voice": "m1"
    }
 }
```

## Docker

This plugin also ships a self-contained image that serves espeak-ng behind
[ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server)'s
ElevenLabs-compatible HTTP API on port `9666`. espeak-ng runs fully offline, so the
container needs no network access and no API keys at runtime.

Pull the published image:

```bash
docker run --rm -p 9666:9666 ghcr.io/openvoiceos/ovos-tts-plugin-espeakng:dev
```

Or build it locally. You can override the default language at build time:

```bash
docker build -t ovos-tts-plugin-espeakng --build-arg LANG=pt .
docker run --rm -p 9666:9666 ovos-tts-plugin-espeakng
```

Or use the bundled compose file:

```bash
docker compose up
```

Synthesize speech with a request to the running server:

```bash
curl 'http://localhost:9666/synthesize/hello%20world' --output hello.wav
```

## Related projects

- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager): loads and manages OVOS TTS plugins.
- [OpenVoiceOS/ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server): HTTP server that exposes this and other TTS plugins over an API.
- [espeak-ng/espeak-ng](https://github.com/espeak-ng/espeak-ng): the speech synthesizer this plugin wraps.
