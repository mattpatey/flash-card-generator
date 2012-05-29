"""
Render flashcards as PDFs.
"""


from reportlab.pdfgen import canvas


class CardRenderer():

    def render(self, words, output):

        c = canvas.Canvas(output)
        for word in words:
            self.render_card(word, canvas)
        c.showPage()
        c.save()

    def render_card(self, word_dict, canvas):

        raise NotImplementedError
