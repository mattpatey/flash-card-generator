

import argparse
import codecs
import logging
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


with open('dictionary.pkl', 'r') as lookup_table_file:
    lookup_table = pickle.load(lookup_table_file)

translator = Translator(lookup_table)
dict_parser = DictionaryParser()


def parse_dictionary():
    """
    Create a data structure from the dictionary.
    """
    entries = dict()
    for line in yield_lines(resource_string(data.__name__, 'de-en.txt')):
        try:
            word, d = dict_parser.parse_line(line)
            entries[word] = d
        except ParseException, e:
            logger.warn('Parse error: %s' % e)
    return entries

def translate(word):
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

    parser = argparse.ArgumentParser('Generate flash cards.')
    parser.add_argument('--parse', type=str)
    parser.add_argument('--word-file', type=str)
    parser.add_argument('--lookup', type=str)
    args = parser.parse_args()

    if args.parse:
        d = parse_dictionary()
        with open('dictionary.pkl', 'w') as f:
            pickle.dump(d, f)
        sys.exit(0)

    if args.lookup:
        print translate(args.lookup.strip())
        sys.exit(0)

    if args.word_file:
        word_pairs = []
        with codecs.open(args.word_file, 'r', encoding='utf-8') as lines:
            for word in lines:
                try:
                    word_info = translate(word.strip())
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
