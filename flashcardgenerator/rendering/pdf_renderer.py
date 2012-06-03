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
                Spacer(A8[0], A8[1] / 2.5),
                Paragraph(word, self.flash_card_style),
                ]

            return elements

    def render_cards(self, word_pairs, output):

        story = []

        for original, translated in word_pairs:
            original_card = self.__build_card(original)
            translated_card = self.__build_card(translated)
            story = story + original_card
            story.append(PageBreak())
            story = story + translated_card
            story.append(PageBreak())

        doc = FlashCardTemplate(output)
        doc.multiBuild(story)
