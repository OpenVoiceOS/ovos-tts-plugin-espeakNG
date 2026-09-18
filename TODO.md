# TODO

## Open issues

- [ ] #14 Dependency Dashboard
- [ ] #2 expose espeak options

## Gaps

- [ ] No unit tests; `test/license_tests.py` only checks dependency licenses.
- [ ] Not migrated to gh-automations CI: missing standard `build-tests`, `coverage`, `license-check`, `release_workflow`, `publish_stable`, and `opm-check` workflows.
- [ ] `license_tests.yml` calls a NeonGecko reusable workflow — remove (no Neon refs); use `OpenVoiceOS/gh-automations` instead.
- [ ] `dev2master.yml` pushes dev->master ad hoc; replace with the standard release workflow.
- [ ] Stale packaging in `setup.py`: `install_requires` hardcoded to `ovos-plugin-manager>=0.0.1a12` (conflicts with `requirements.txt` `>=2.1.0,<2.2.0`); license metadata vs classifier mismatch (GPL vs Apache); obsolete Python 2.7/3.0-3.6 classifiers; hand-pinned version. Consider migrating to `pyproject.toml`.
- [ ] Legacy entry-point group `mycroft.plugin.tts` rather than modern `opm.tts` / `opm.tts.config`.
- [ ] No `pyproject.toml`.
- [ ] Committed scratch artifacts: `ovos_tts_plugin_espeakng.egg-info/` and sample `espeak.wav`.

## Code TODOs

- [ ] `ovos_tts_plugin_espeakng/__init__.py:65` — `validate_lang()` is a `# TODO` stub.
- [ ] `ovos_tts_plugin_espeakng/__init__.py:97` — `# TODO lang codes should be normalized better` (3-letter codes dropped).
