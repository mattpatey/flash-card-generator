"""
Generate flash cards from a list of words and data.
"""


import codecs
import os
import re

from pkg_resources import (
    resource_string,
    yield_lines,
    )

from .. import data


class WordNotFoundException(Exception):

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
            # TODO: This is probably the least efficient way of
            # looking up a word, but it works (for now).
            for line in yield_lines(resource_string(data.__name__, 'de-en.txt')):
                line_u = line.decode('utf-8')
                if re.match(lookup_ptn, line_u):
                    return line_u
            raise WordNotFoundException

        try:
            line = find_word(word)
            return self.parse_line(line)
        except WordNotFoundException:
            raise

    def parse_line(self, line):
        """
        Build a data structure from a dictionary entry.

        The structure may include:

            - the singular form
            - the gender
            - plural forms
            - translations
        """

        orig, trans = self.split_original_translation(line)

        o_variants = self.parse_variants(self.get_variants(orig))
        o_plurals = self.parse_plurals(self.get_plurals(orig))
        t_variants = self.parse_variants(self.get_variants(trans))

        # TODO: Don't store properties for words for which the
        # property makes sense, e.g. verbs don't have gender.
        res = dict(singular=None,
                   gender=None,
                   plural=None,
                   translations=None)

        if o_variants:
            res['singular'] = o_variants[0]['word']
            res['gender'] = o_variants[0]['gender']
        if o_plurals:
            res['plural'] = o_plurals[0]['word']
        if t_variants:
            res['translations'] = t_variants[0]['word']

        return res

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

    def parse_variants(self, variants):
        """
        Return a data structure representative of word variants and
        their attributes.
        """

        # TODO: Parse verbs and acronyms (e.g. /CDU/)
        # TODO: Support multi-word entries, e.g. "zu leicht nehmen"
        all_variants = [v.strip() for v in variants.split(';')]
        word_parts = r'(?P<word>[\w\s]+) ?(\{(?P<gender>[m|f|n])\})? ?(\[(?P<field>\w+\.?)\])? ?'
        word_parts_re = re.compile(word_parts, re.UNICODE)
        regex_matches = [word_parts_re.match(v) for v in all_variants]
        variant_list = [v.groupdict() for v in regex_matches if v]

        for v in variant_list:
            v['word'] = v['word'].strip()

        return variant_list

    def get_plurals(self, line):
        """
        Return a data structure containing plural forms of an entry.
        """

        plural_ptn = r'\w+ \{pl\};?'
        plural_re = re.compile(plural_ptn, re.UNICODE)
        matches = plural_re.findall(line)

        return ' '.join(matches)

    def parse_plurals(self, plurals):
        """
        Return plural forms of an entry, if any.
        """

        all_parts = plurals.split(';')
        all_parts = [p.strip() for p in all_parts]
        part = r'(?P<word>\w+) \{pl\}'
        part_re = re.compile(part, re.UNICODE)
        plurals = [part_re.match(p) for p in all_parts]
        plurals = [p.groupdict() for p in plurals if p]

        return plurals


class Translator():
    """
    Find translations and meta-data of words.
    """

    def __init__(self):

        self.dictionary_parser = DictionaryParser()

    def translate(self, word):

        return self.dictionary_parser.lookup(word)
