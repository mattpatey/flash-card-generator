

import os
from tempfile import gettempdir
from unittest import TestCase
from uuid import uuid4

from flashcardgenerator.rendering.pdf_renderer import CardRenderer


class RendererTests(TestCase):

    def test_save_as_pdf(self):

        renderer = CardRenderer()
        f = str(uuid4())
        path = os.path.join(gettempdir(), f)
        word_pairs = (({'word': 'foo', 'gender': None}, 'bar'),)
        renderer.render_cards(word_pairs, path)
        self.assertTrue(os.path.isfile(path))
