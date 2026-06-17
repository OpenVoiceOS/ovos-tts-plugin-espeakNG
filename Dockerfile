FROM python:3.11-slim

RUN apt-get update && \
  apt-get install -y git build-essential espeak-ng && \
  rm -rf /var/lib/apt/lists/*

RUN pip3 install ovos-tts-server

COPY . /tmp/ovos-tts-plugin-espeakng
RUN pip3 install /tmp/ovos-tts-plugin-espeakng

ENTRYPOINT ovos-tts-server --engine ovos-tts-plugin-espeakng
