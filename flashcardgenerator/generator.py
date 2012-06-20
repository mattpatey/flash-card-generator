

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
    NoTypeIndicatorException,
    ParseException,
    Translator,
    UnknownVariantTypeException,
    VariantParseException,
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
                word, translation = dict_parser.parse_line(line)
                if not translation:
                    logger.error(u"Couldn't find translation for '%s'" % line)
                    continue
                entry_key = unicode(word)
                if not entries.get(entry_key):
                    entries[entry_key] = word, translation
                else:
                    logger.info("Skipping duplicate entry for '%s'." % entry_key)
            except ParseException, e:
                logger.warn(u"Parse error: '%s'" % e)
            except NoTypeIndicatorException, e:
                logger.warn(u"Couldn't figure out word type for line: '%s'" % e)
            except VariantParseException, e:
                logger.warn(u"Couldn't parse some variants: '%s'" % e)
            except UnknownVariantTypeException, e:
                logger.warn(u"Not sure what a '%s' is." % e)
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
        words_and_translations = []
        with codecs.open(args.word_file, 'r', encoding='utf-8') as lines:
            for word in lines:
                try:
                    original, translation = translate(word.strip(), translator)
                except WordNotFoundException:
                    continue
                words_and_translations.append((original, translation))

        renderer = CardRenderer()
        renderer.render_cards(words_and_translations, '/tmp/test.pdf')
        sys.exit(0)
