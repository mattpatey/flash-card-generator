"""
Generate flash cards from a list of words and data.
"""


import os
import re

from pkg_resources import (
    resource_string,
    yield_lines,
    )

from .. import data

from word_parts import (
    Adjective,
    Noun,
    Translation,
    Verb,
    )


class ParseException(Exception):

    pass


class WordNotFoundException(Exception):

    pass


class UnknownVariantTypeException(Exception):

    pass


class NoTypeIndicatorException(Exception):

    pass


class DictionaryParser():
    """
    Parse plain-text lines in a dictionary.

    The supported format of a dictionary line is based on the open
    source data used by German/English dictionary provided by the
    Beolingus project, http://dict.tu-chemnitz.de/. No other formats
    will be supported.
    """

    def lookup(self, word):

        lookup_re = r'^%s.*$' % word
        lookup_ptn = re.compile(lookup_re, re.IGNORECASE)
        def find_word(w):
            for line in yield_lines(resource_string(data.__name__, 'de-en.txt')):
                line_u = line.decode('utf-8')
                if re.match(lookup_ptn, line_u):
                    return line_u
            raise WordNotFoundException

        line = find_word(word)
        return self.parse_line(line)

    def parse_line(self, line):
        """
        Build a data structure from a dictionary entry.
        """
        orig, trans = self.split_original_translation(line)
        original_variants = self.parse_variants(self.get_variants(orig))
        translated_variants = self.parse_variants(self.get_variants(trans), is_translation=True)

        return original_variants[0], translated_variants[0]

    def get_variant_type(self, variant):

        type_indicators = (
            (Adjective, ['adj',]),
            (Verb, ['vi', 'vt']),
            (Noun, [Noun.FEMININE, Noun.MASCULINE, Noun.NEUTRAL]),
            )

        for type_cls, indicators in type_indicators:
            for i in indicators:
                if i in variant:
                    return type_cls

        raise UnknownVariantTypeException(variant)

    def split_original_translation(self, line):
        """
        Return the original and translated parts of an entry.
        """

        split = line.split('::')
        return split[0].strip(), split[1].strip()

    def get_variants(self, line):
        """
        Return the part of an entry containing the word and variants,
        if any.
        """

        return line.split("|")[0].rstrip()

    def parse_variants(self, variants, is_translation=False):
        """
        Return a data structure representative of word variants and
        their attributes.
        """
        all_variants = [v.strip() for v in variants.split(';')]

        word_ptn = r'[\w\s]+'
        word_type_indicator_ptn = r'[%s|%s|%s|%s|%s|%s]' % (Noun.FEMININE,
                                                            Noun.MASCULINE,
                                                            Noun.NEUTRAL,
                                                            Verb.INTRANSITIVE,
                                                            Verb.TRANSITIVE,
                                                            Adjective.ADJECTIVE,)
        field_ptn = r'\w+\.?'
        word_parts = r'(?P<word>%(word_ptn)s) ?(\{(?P<word_type_indicator>%(word_type_indicator_ptn)s)\})? ?(\[(?P<field>%(field_ptn)s)\])? ?' % dict(
            word_ptn=word_ptn,
            word_type_indicator_ptn=word_type_indicator_ptn,
            field_ptn=field_ptn,
            )

        word_parts_re = re.compile(word_parts, re.UNICODE)
        regex_matches = [word_parts_re.match(v) for v in all_variants]

        variant_list = []
        for match in regex_matches:
            parts = match.groupdict()

            if not is_translation:
                if not parts['word_type_indicator']:
                    raise NoTypeIndicatorException(parts['word'])

                word_part_cls = self.get_variant_type(parts['word_type_indicator'])

                if word_part_cls == Noun:
                    word_attrs = dict(gender=parts['word_type_indicator'])
                elif word_part_cls == Verb:
                    word_attrs = dict(verb_type=parts['word_type_indicator'])
                else:
                    word_attrs = dict()

                word_obj = word_part_cls(parts['word'].strip(), **word_attrs)
            else:
                word_obj = Translation(parts['word'].strip())

            variant_list.append(word_obj)

        return variant_list


class Translator():
    """
    Find translations and meta-data of words.
    """

    def __init__(self, lookup_table):

        self.lookup_table = lookup_table

    def lookup(self, word):
        """
        Perform a totally dumb word lookup.

        If at first the provided word is not found then try again with
        a capialized or lowecased version of the word.

        TODO: Handle spelling mistakes.

        Raises WordNotFoundException if the word is not found despite
        our best efforts.
        """

        try:
            return self.lookup_table[word]
        except KeyError:
            try:
                if word[0].isupper():
                    modified_word = word.lower()
                else:
                    modified_word = word.capitalize()
                return self.lookup_table[modified_word]
            except KeyError:
                raise WordNotFoundException("%s / %s" % (word, modified_word))
