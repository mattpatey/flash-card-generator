

import argparse

import logging

from rendering import CardRenderer

from translation import (
    Translator,
    WordNotFoundException,
    )


translator = Translator()


def translate(word):
    try:
        return translator.translate(word)
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
    parser.add_argument('--word-file', type=str)
    parser.add_argument('--lookup', type=str)
    args = parser.parse_args()

    if args.lookup:
        print translate(args.lookup.strip())
    elif args.word_file:
        word_pairs = []
        with open(args.word_file, 'r') as lines:
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
