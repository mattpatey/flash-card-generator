

class Noun():

    FEMININE = u"f"
    MASCULINE = u"m"
    NEUTRAL = u"n"

    def __init__(self, word, type_identifier):

        self.word = word
        self.type_identifier = type_identifier

    def __eq__(self, other):

        if not isinstance(other, Noun):
            return False

        if (other.word == self.word and
            other.plural_form == self.plural_form and
            other.translation == self.translation):
            return True

        return False

    def __unicode__(self):

        return self.word


class Adjective():

    ADJECTIVE = 'adj'

    def __init__(self, word, **_kwargs):

        self.word = word
        self.type_identifier = ADJECTIVE

    def __eq__(self, other):

        if not isinstance(other, Adjective):
            return False

        if (other.word == self.word and
            other.translation == self.translation):
            return True

        return False

    def __unicode__(self):

        return self.word


class Verb():

    INTRANSITIVE = 'vi'
    TRANSITIVE = 'vt'

    def __init__(self, word, type_identifier):

        self.word = word
        self.type_identifier = type_identifier

    def __eq__(self, other):

        if not isinstance(other, Verb):
            return False

        if (other.word == self.word and
            other.translation == self.translation):
            return True

        return False

    def __unicode__(self):

        return self.word


class Translation():

    def __init__(self, word):

        self.word = word

    def __eq__(self, other):

        if not isinstance(other, Translation):
            return False

        if other.word == self.word:
            return True

        return False

    def __unicode__(self):

        return self.word
