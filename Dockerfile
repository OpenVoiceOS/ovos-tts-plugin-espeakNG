FROM python:3.7

RUN apt-get update && apt-get install -y espeak-ng

RUN pip3 install ovos-utils==0.0.35
RUN pip3 install ovos-plugin-manager==0.0.23
RUN pip3 install ovos-tts-server==0.0.3a8 
COPY . /tmp/ovos-tts-plugin-espeakng
RUN pip3 install /tmp/ovos-tts-plugin-espeakng

COPY mycroft.con[f] /etc/mycroft/mycroft.conf
COPY mycroft.con[f] /root/.config/mycroft/mycroft.conf

ENTRYPOINT ovos-tts-server --engine ovos-tts-plugin-espeakng
