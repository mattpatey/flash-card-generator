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
from flashcardgenerator.translation.word_parts import (
    Adjective,
    Noun,
    Translation,
    Verb,
    )


class TranslatorTests(TestCase):

    lookup_table = {u"Brot": (Noun(u"Brot", gender=Noun.NEUTRAL), Translation(u"roll")),
                    u"gnadenlos": (Adjective(u"gnadenlos"), Translation(u"merciless")),
                    }


    def setUp(self):

        super(TranslatorTests, self).setUp()
        self.translator = Translator(self.lookup_table)

    def test_lookup(self):

        expected = (Noun(u"Brot", gender=Noun.NEUTRAL,),
                    Translation(u"roll"))
        self.assertEqual(expected, self.translator.lookup(u"Brot"))

    def test_uncapitalized_noun(self):
        """
        Nouns shouldn't have to be capitalized when input.
        """
        expected = (Noun(u"Brot", gender=Noun.NEUTRAL),
                    Translation(u"roll"))
        self.assertEqual(expected, self.translator.lookup(u"brot"))

    def test_capitalized_non_noun(self):
        expected = (Adjective(u"gnadenlos"),
                    Translation(u"merciless"))
        self.assertEqual(expected, self.translator.lookup(u"Gnadenlos"))

    def test_partial_lookup(self):

        self.translator.lookup(u"bloße")
        self.translator.lookup(u"Zugeh")


class DictionaryParserTests(TestCase):
    """
    Tests for interpreting content from a dictionary.
    """

    def setUp(self):

        super(DictionaryParserTests, self).setUp()
        self.parser = DictionaryParser()
        self.noun = u"Brötchen {n}; Semmel {f}; Wecken {m}; Schrippe {f} [cook.] | Brötchen {pl}; Semmeln {pl}; Wecken {pl}; Schrippen {pl} | (kleines, rundes) Brötchen {n} | kleine(re) Brötchen backen müssen [übtr.] :: roll; bread roll | rolls; bread rolls | biscuit [Am.] | to have to set one's sights lower"

    def test_lookup(self):

        expected = (Noun(u"Brötchen", gender=Noun.NEUTRAL),
                    Translation(u"roll"))
        result = self.parser.lookup(u"Brötchen")
        self.assertEqual(expected, result)

    def test_lookup_raises_when_word_not_found(self):

        self.assertRaises(WordNotFoundException, self.parser.lookup, word='xyz')

    def test_parse_line(self):
        expected = (Noun(u"Brötchen", gender=Noun.NEUTRAL,),
                    Translation(u"roll"))
        result = self.parser.parse_line(self.noun)
        self.assertEqual(expected, result)

    def test_get_variant_type(self):

        result = self.parser.get_variant_type(u"Brötchen {n}")
        self.assertEqual(Noun, result)

        result = self.parser.get_variant_type(u"fliegen {vi}")
        self.assertEqual(Verb, result)

        result = self.parser.get_variant_type(u"nüchtern {adj}")
        self.assertEqual(Adjective, result)

    def test_multi_word_translation(self):

        expected = (Noun(word=u"Abnehmerbügel",
                        gender=Noun.MASCULINE,),
                    Translation(word=u"towing arm"))
        line = u"Abnehmerbügel {m} :: towing arm"
        result = self.parser.parse_line(line)
        self.assertEqual(expected, result)

    def test_get_language_parts(self):

        original, translation = self.parser.split_original_translation(self.noun)

        expected = u"Brötchen {n}; Semmel {f}; Wecken {m}; Schrippe {f} [cook.] | Brötchen {pl}; Semmeln {pl}; Wecken {pl}; Schrippen {pl} | (kleines, rundes) Brötchen {n} | kleine(re) Brötchen backen müssen [übtr.]"
        self.assertEqual(expected, original)

        expected = u"roll; bread roll | rolls; bread rolls | biscuit [Am.] | to have to set one's sights lower"
        self.assertEqual(expected, translation)

    def test_get_variants(self):

        original, translated = self.parser.split_original_translation(self.noun)

        expected = u"Brötchen {n}; Semmel {f}; Wecken {m}; Schrippe {f} [cook.]"
        result = self.parser.get_variants(original)
        self.assertEqual(expected, result)

        expected = u"roll; bread roll"
        result = self.parser.get_variants(translated)
        self.assertEqual(expected, result)

    def test_parse_variants(self):

        original, translated = self.parser.split_original_translation(self.noun)
        variants = self.parser.get_variants(original)

        expected = [Noun(u"Brötchen", gender=Noun.NEUTRAL),
                    Noun(u"Semmel", gender=Noun.FEMININE),
                    Noun(u'Wecken', gender=Noun.MASCULINE),
                    Noun(u'Schrippe', gender=Noun.FEMININE),
                    ]
        result = self.parser.parse_variants(variants)
        self.assertEqual(expected, result)
