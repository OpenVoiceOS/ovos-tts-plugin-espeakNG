# espeak-ng speech synthesis served through ovos-tts-server's ElevenLabs-compatible
# API. A self-contained, fully offline image: any client that speaks the
# ovos-tts-server / ElevenLabs API can hit it, and it can be A/B-tested against other
# ovos-tts-server voices (phoonnx, edge-tts, omnivoice, ...) by pointing at a different
# port.
#
# espeak-ng is an offline synthesizer, so this container needs no network access at
# runtime.
FROM python:3.11-slim

# espeak-ng: the synthesizer binary the plugin shells out to. It emits WAV directly,
# so no ffmpeg transcoding is needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
        espeak-ng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# the plugin + the OVOS TTS server. setuptools<81 keeps ovos-plugin-manager's
# pkg_resources usage working. ovos-tts-server>=1.13.5a1's alpha floor lets pip resolve
# the prerelease without --pre.
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "setuptools<81" "." "ovos-tts-server>=1.13.5a1"

# Default language, overridable with the LANG build arg (any espeak-ng lang works).
ARG LANG=en-us
RUN useradd -m -u 1000 ovos \
    && mkdir -p /home/ovos/.config/mycroft \
    && printf '{\n  "tts": {\n    "module": "ovos-tts-plugin-espeakng",\n    "ovos-tts-plugin-espeakng": {\n      "lang": "%s",\n      "voice": "m1"\n    }\n  }\n}\n' "${LANG}" \
        > /home/ovos/.config/mycroft/mycroft.conf \
    && chown -R 1000:1000 /home/ovos/.config
USER 1000

EXPOSE 9666
ENTRYPOINT ["ovos-tts-server", "--engine", "ovos-tts-plugin-espeakng", \
            "--host", "0.0.0.0", "--port", "9666", "--cache"]
