#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from configparser import ConfigParser

import argparse
import os

from dictionary import get_dictionary


__version__ = (0, 0, 1)

def validate_config(config):
    assert 'language' in config, '[language] section MUST require.'
    assert 'support' in config['language']
    langs = [x.strip() for x in config['language']['support'].split(',')]
    if not langs:
        raise AssertionError('language.support MUST not empty.')
    for lang in langs:
        assert lang in config.sections(), \
               '[{}] section MUST require.'.format(lang)
        assert 'name' in config[lang]
        assert 'url' in config[lang]
        assert 'path' in config[lang]


def read_option(filename):
    config = ConfigParser()
    config.read(os.path.abspath(filename))
    validate_config(config)
    return config


def setup_translator(translators):
    translator_env = {}
    for t in translators:
        inst = get_dictionary(**t)
        translator_env[inst.name] = inst
    return translator_env


def main(lang, word, configfile):
    options = read_option(configfile)
    assert lang in options['language']['support'], \
            'language MUST be one of {}'.format(options['language']['support'])
    translator = get_dictionary(**options[lang])
    print(translator.translate(word))


parser = argparse.ArgumentParser(description='Command line dictionary.')
parser.add_argument('language', metavar='LANG',
                    help='Choose dictionary to translate word. '
                         'following options are available.', type=str)
parser.add_argument('word', metavar='WORD',
                    help='Type the word to be translated.', type=str)
parser.add_argument('--config', '-c', help='config file', dest='configfile',
                    default='conf.ini')
args = parser.parse_args()
main(args.language, args.word, args.configfile)
