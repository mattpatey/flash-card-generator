

class Noun():

    FEMININE = u"f"
    MASCULINE = u"m"
    NEUTRAL = u"n"

    def __init__(self, word, plural_form=None, translation=None, **kwargs):

        self.word = word
        self.plural_form = plural_form
        self.translation = translation
        self.gender = kwargs['gender']

    def __eq__(self, other):

        if not isinstance(other, Noun):
            return False

        if (other.word == self.word and
            other.plural_form == self.plural_form and
            other.translation == self.translation):
            return True

        return False


class Adjective():

    ADJECTIVE = 'adj'

    def __init__(self, word, translation=None, **kwargs):

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

    INTRANSITIVE = 'vi'
    TRANSITIVE = 'vt'

    def __init__(self, word, translation=None, **kwargs):

        self.word = word
        self.translation = translation

    def __eq__(self, other):

        if not isinstance(other, Verb):
            return False

        if (other.word == self.word and
            other.translation == self.translation):
            return True

        return False


class Translation():

    def __init__(self, word):

        self.word = word

    def __eq__(self, other):

        if not isinstance(other, Translation):
            return False

        if other.word == self.word:
            return True

        return False
