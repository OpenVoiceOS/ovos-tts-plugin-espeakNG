#!/usr/bin/env python3
from setuptools import setup

PLUGIN_ENTRY_POINT = 'ovos-tts-plugin-espeakng = ovos_tts_plugin_espeakng:EspeakNGTTS'
SAMPLE_CONFIGS = 'ovos-tts-plugin-espeakng.config = ' \
                 'ovos_tts_plugin_espeakng:EspeakNGTTSPluginConfig'
setup(
    name='ovos-tts-plugin-espeakng',
    version='0.0.3a1',
    description='espeakNG tts plugin for mycroft',
    url='https://github.com/OpenVoiceOS/ovos-tts-plugin-espeakNG',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='GPL-3.0-or-later',
    packages=['ovos_tts_plugin_espeakng'],
    install_requires=['ovos-plugin-manager>=0.0.1a12'],
    zip_safe=True,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mycroft OpenVoiceOS OVOS chatterbox plugin tts',
    entry_points={'mycroft.plugin.tts': PLUGIN_ENTRY_POINT,
                  'mycroft.plugin.tts.config': SAMPLE_CONFIGS}
)
