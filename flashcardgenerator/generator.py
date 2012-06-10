

import argparse
import codecs
import logging
import os
import pickle

from pkg_resources import (
    resource_string,
    yield_lines,
    )

import sys

import data

from rendering import CardRenderer

from translation import (
    DictionaryParser,
    ParseException,
    Translator,
    WordNotFoundException,
    )


def parse_dictionary(dictionary_file):
    """
    Create a data structure from the dictionary.
    """
    entries = dict()
    dict_parser = DictionaryParser()
    with codecs.open(dictionary_file, 'r', encoding='utf-8') as lines:
        for line in lines:
            if line.startswith('#'):
                continue
            try:
                word, d = dict_parser.parse_line(line)
                if not d['translations']:
                    logger.error(u"Couldn't find translation for '%s'" % line)
                    continue
                entries[word] = d
            except ParseException, e:
                logger.warn(u'Parse error: %s' % e)
    return entries

def create_dictionary_pickle():
    logger.info("Creating dictionary pickle.")
    d = parse_dictionary('flashcardgenerator/data/de-en.txt')
    with open('dictionary.pkl', 'w') as f:
        pickle.dump(d, f)

def translate(word, translator):
    try:
        return translator.lookup(word)
    except WordNotFoundException:
        logging.warn("Couldn't find translation for '%s'." % word)
        raise


if __name__ == '__main__':
    logger = logging.getLogger()
    handler = logging.FileHandler('flash-card-generator.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)

    parser = argparse.ArgumentParser('Generate flash cards and lookup German to English translations.')
    parser.add_argument('--word-file', type=str)
    parser.add_argument('--lookup', type=str)
    args = parser.parse_args()

    if not os.path.exists('dictionary.pkl'):
        create_dictionary_pickle()

    with open('dictionary.pkl', 'r') as lookup_table_file:
        lookup_table = pickle.load(lookup_table_file)
    translator = Translator(lookup_table)

    if args.lookup:
        print translate(args.lookup.strip(), translator)
        sys.exit(0)

    if args.word_file:
        word_pairs = []
        with codecs.open(args.word_file, 'r', encoding='utf-8') as lines:
            for word in lines:
                try:
                    word_info = translate(word.strip(), translator)
                except WordNotFoundException:
                    continue
                original_word_data = dict(word=word_info['singular'],
                                          gender=word_info['gender'])
                word_pairs.append((original_word_data,
                                   word_info['translations']))

        renderer = CardRenderer()
        renderer.render_cards(word_pairs,
                              '/tmp/test.pdf')
        sys.exit(0)
