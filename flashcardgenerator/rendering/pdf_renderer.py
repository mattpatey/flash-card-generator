"""
Render flashcards as PDFs.
"""


from reportlab.lib.enums import TA_CENTER

from reportlab.lib.styles import ParagraphStyle

from reportlab.lib.units import mm, cm

from reportlab.platypus import (
    PageBreak,
    SimpleDocTemplate,
    Spacer,
    )

from reportlab.platypus.doctemplate import (
    BaseDocTemplate,
    PageTemplate,
    )

from reportlab.platypus.frames import Frame

from reportlab.platypus.paragraph import Paragraph


A8 = (74.325*mm, 52.556*mm)


class FlashCardTemplate(BaseDocTemplate):

    def __init__(self, filename, **kw):

        BaseDocTemplate.__init__(self, filename, pagesize=A8, **kw)
        template = PageTemplate('normal', [Frame(0*mm, 0*mm, A8[0], A8[1], id='F1')])
        self.addPageTemplates(template)


class CardRenderer():

    flash_card_style = ParagraphStyle(name='centeredStyle', alignment=TA_CENTER)

    def __build_card(self, word):

            elements = [

                ]

            return elements

    def render_cards(self, word_pairs, output):

        story = []

        def _c(original, translated, gender=None):
            if gender:
                first_line_original = u'%s (%s)' % (original, gender)
            else:
                first_line_original = original

            elements = [Spacer(A8[0], A8[1] / 2.5),
                        Paragraph(first_line_original, self.flash_card_style),
                        PageBreak(),
                        Spacer(A8[0], A8[1] / 2.5),
                        Paragraph(translated, self.flash_card_style),
                        PageBreak(),
                        ]
            return elements

        for original, translated in word_pairs:
            word = original['word']
            gender = original['gender']
            cards = _c(word, translated, gender=gender)
            story = story + cards

        doc = FlashCardTemplate(output)
        doc.multiBuild(story)
