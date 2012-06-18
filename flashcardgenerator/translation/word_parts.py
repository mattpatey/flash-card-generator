

class Noun():

    FEMININE = 'f'
    MASCULINE = 'm'
    NEUTRAL = 'n'

    def __init__(self, word, gender, plural_form, translation):

        self.word = word
        self.gender = gender
        self.plural_form = plural_form
        self.translation = translation

    def __eq__(self, other):

        if not isinstance(other, Noun):
            return False

        if (other.word == self.word and
            other.plural_form == self.plural_form and
            other.translation == self.translation):
            return True

        return False


class Adjective():

    def __init__(self, word, translation):

        self.word = word
        self.translation = translation

    def __eq__(self, other):

        if not isinstance(other, Adjective):
            return False

        if (other.word == self.word and
            other.translation == self.translation):
            return True

        return False


class Verb():

    def __init__(self, word, translation):

        self.word = word
        self.translation = translation

    def __eq__(self, other):

        if not isinstance(other, Verb):
            return False

        if (other.word == self.word and
            other.translation == self.translation):
            return True

        return False
