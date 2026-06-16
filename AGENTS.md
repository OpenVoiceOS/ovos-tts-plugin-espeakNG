# ovos-tts-plugin-espeakNG

OVOS TTS plugin wrapping the `espeak-ng` (or `espeak`) command-line synthesizer. Offline, multilingual, SSML-aware.

## Setup

```bash
pip install .
apt-get install espeak-ng   # the espeak-ng binary must be on PATH
```

Runtime dep: `ovos-plugin-manager`. The plugin shells out to the `espeak-ng` binary (falls back to `espeak`); the path can be overridden via config key `binary`.

## Test

No unit tests exist. `test/license_tests.py` only checks dependency licenses, not behavior. There is no configured test runner.

## Lint/Typecheck

None configured.

## Layout

- `ovos_tts_plugin_espeakng/__init__.py` — the whole plugin:
  - `EspeakNGTTS(TTS)` — `get_tts()` calls `espeak-ng -m -w <wav> -v <lang>+<voice> <sentence>`; SSML tags declared; `modify_tag()` rewrites prosody percentages; `available_languages` derives from `_get_voices()`.
  - `EspeakNGValidator(TTSValidator)` — `validate_connection()` errors if no espeak binary; `validate_lang()` is a stub.
  - `_get_voices()` — parses `espeak --voices`, builds the per-language `m1`/`f1` voice config map used both for `available_languages` and the sample-config entry point.
- Entry-point group: `mycroft.plugin.tts` (plugin) and `mycroft.plugin.tts.config` (sample configs) in `setup.py`. These are the legacy group names; modern OVOS plugins use `opm.tts` / `opm.tts.config`.
- `Dockerfile` + `publish_docker.yml` build an `ovos-tts-server` container exposing the engine over HTTP.

## Conventions (Org hard rules)

- Branches: `dev` (work) and `master` (stable). NEVER use `main`.
- Never edit `version.py` / version fields by hand; gh-automations bumps semver from conventional-commit prefixes (`feat:`, `fix:`, `feat!:`).
- New repos are private by default; do not make source public without asking.
- Commit identity: `JarbasAi <jarbasai@mailfence.com>`.
- Reference `OpenVoiceOS/gh-automations` reusable workflows at `@dev`.
- No Neon / `neon-*` references.
- No meta-commentary (no history, dates, "design mistake" language); describe current state only.
- CI is provided by `OpenVoiceOS/gh-automations`.

## Gotchas

- Packaging is stale: `setup.py` hardcodes `install_requires=['ovos-plugin-manager>=0.0.1a12']` and ignores `requirements.txt` (`ovos-plugin-manager>=2.1.0,<2.2.0`). License field says `GPL-3.0-or-later` while a classifier says Apache. Version is hand-pinned (`0.0.3a1`) and Python 2.7/3.0-3.6 classifiers are listed.
- `_get_voices()` runs `espeak --voices` at import time; on a machine without the binary it returns `{}`, so the sample-config entry point and `available_languages` are empty.
- `validate_lang()` is a no-op stub; languages are not actually validated against the engine.
- 3-letter language codes from espeak are silently dropped; dialect codes are merged to the base lang (with an en-us/en-gb special case).
- CI does not use gh-automations; `license_tests.yml` calls a NeonGecko reusable workflow (forbidden by org rules). `dev2master.yml` pushes dev->master ad hoc rather than via the standard release workflow.
- Committed scratch/sample artifacts: `ovos_tts_plugin_espeakng.egg-info/` and `espeak.wav`.
