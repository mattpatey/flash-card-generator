# -*- coding: utf-8 -*-
"""
Tests for the parsing mechanism.
"""


import os
from unittest import TestCase

from flashcardgenerator.translation.translator import (
    DictionaryParser,
    Translator,
    WordNotFoundException,
    )


class TranslatorTests(TestCase):

    def test_translate(self):

        translator = Translator()
        expected = dict(
            singular=u'Brot',
            gender=u'n',
            plural=u'Brote',
            translations=(u'bread'))
        self.assertEqual(expected, translator.translate('Brot'))

    def test_uncapitalized_noun(self):
        """
        Nouns shouldn't have to be capitalized when input.
        """
        translator = Translator()
        expected = dict(
            singular=u'Brot',
            gender=u'n',
            plural=u'Brote',
            translations=(u'bread'))
        self.assertEqual(expected, translator.translate('brot'))


class DictionaryParserTests(TestCase):
    """
    Tests for interpreting content from a dictionary.
    """

    def setUp(self):

        super(DictionaryParserTests, self).setUp()
        self.parser = DictionaryParser()
        self.adjective = u"Brötchen {n}; Semmel {f}; Wecken {m}; Schrippe {f} [cook.] | Brötchen {pl}; Semmeln {pl}; Wecken {pl}; Schrippen {pl} | (kleines, rundes) Brötchen {n} | kleine(re) Brötchen backen müssen [übtr.] :: roll; bread roll | rolls; bread rolls | biscuit [Am.] | to have to set one's sights lower"

    def test_lookup(self):

        expected = dict(singular=u"Brötchen",
                        gender=u"n",
                        plural=u"Brötchen",
                        translations=u"roll")
        result = self.parser.lookup(u"Brötchen")
        self.assertEqual(expected, result)

    def test_lookup_raises_when_word_not_found(self):

        self.assertRaises(WordNotFoundException, self.parser.lookup, word='xyz')

    def test_parse_line(self):

        expected = dict(singular=u"Brötchen",
                        gender='n',
                        plural=u"Brötchen",
                        translations="roll")
        result = self.parser.parse_line(self.adjective)
        self.assertEqual(expected, result)

    def test_multi_word_translation(self):

        expected = dict(singular=u"aufrufen",
                        gender=None,
                        plural=None,
                        translations=u"to invoice")
        line = u"aufrufen :: to invoice"
        result = self.parser.parse_line(line)
        self.assertEqual(expected, result)

    def test_get_language_parts(self):

        original, translation = self.parser.split_original_translation(self.adjective)

        expected = u"Brötchen {n}; Semmel {f}; Wecken {m}; Schrippe {f} [cook.] | Brötchen {pl}; Semmeln {pl}; Wecken {pl}; Schrippen {pl} | (kleines, rundes) Brötchen {n} | kleine(re) Brötchen backen müssen [übtr.]"
        self.assertEqual(expected, original)

        expected = u"roll; bread roll | rolls; bread rolls | biscuit [Am.] | to have to set one's sights lower"
        self.assertEqual(expected, translation)

    def test_get_variants(self):

        original, translated = self.parser.split_original_translation(self.adjective)

        expected = u"Brötchen {n}; Semmel {f}; Wecken {m}; Schrippe {f} [cook.]"
        result = self.parser.get_variants(original)
        self.assertEqual(expected, result)

        expected = u"roll; bread roll"
        result = self.parser.get_variants(translated)
        self.assertEqual(expected, result)

    def test_get_plurals(self):

        expected = u"Brötchen {pl}; Semmeln {pl}; Wecken {pl}; Schrippen {pl}"
        result = self.parser.get_plurals(self.adjective)
        self.assertEqual(expected, result)

    def test_parse_variants(self):

        self.maxDiff = 1000
        original, translated = self.parser.split_original_translation(self.adjective)
        variants = self.parser.get_variants(original)
        expected = [
            dict(word=u'Brötchen',
                 gender=u'n',
                 field=None,
                 ),
            dict(word=u'Semmel',
                 gender=u'f',
                 field=None,
                 ),
            dict(word=u'Wecken',
                 gender=u'm',
                 field=None,
                 ),
            dict(word=u'Schrippe',
                 gender=u'f',
                 field=u'cook.',
                 ),
            ]
        result = self.parser.parse_variants(variants)
        self.assertEqual(expected, result)

        expected = [
            dict(word=u'roll',
                 gender=None,
                 field=None),
            dict(word=u'bread roll',
                 gender=None,
                 field=None),
            ]
        variants = self.parser.get_variants(translated)
        result = self.parser.parse_variants(variants)
        self.assertEqual(expected, result)

    def test_parse_plural_forms(self):

        plural_forms = self.parser.get_plurals(self.adjective)
        expected = [dict(word=u'Brötchen'),
                    dict(word=u'Semmeln'),
                    dict(word=u'Wecken'),
                    dict(word=u'Schrippen'),
                    ]
        result = self.parser.parse_plurals(plural_forms)
        self.assertEqual(expected, result)
