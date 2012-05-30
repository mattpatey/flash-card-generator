

import os
from tempfile import gettempdir
from unittest import TestCase
from uuid import uuid4

from ..pdf_renderer import CardRenderer


TEST_WORDS = u"""\
foo
bar
baz"""


class RendererTests(TestCase):

    def test_save_as_pdf(self):

        renderer = CardRenderer()
        f = str(uuid4())
        path = os.path.join(gettempdir(), f)
        renderer.render(TEST_WORDS.split('\n'), path)
        self.assertTrue(os.path.isfile(path))
