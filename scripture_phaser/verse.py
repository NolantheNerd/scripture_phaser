from scripture_phaser.enums import Bible
from scripture_phaser.enums import Bible_Books
from scripture_phaser.exceptions import InvalidReference

class Verse:
    def __init__(self, book, chapter, verse, text=None):
        self.book = book
        self.chapter = chapter
        self.verse = verse
        self.reference = f"{Bible_Books[self.book]} {self.chapter+1}:{self.verse+1}"
        self.valid = self.validate(self)

        self.initialized = text is not None
        if self.initialized:
            self.initialize(text)

    def initialize(self, text):
        self.text = text
        self.length = len(self.text)
        self.n_words = len(self.text.split())

    @staticmethod
    def verse_equal(verse1, verse2):
        if (verse1.book == verse2.book and
            verse1.chapter == verse2.chapter and
            verse1.verse == verse2.verse):
            return True
        return False

    @staticmethod
    def validate(verse):
        if verse.book >= 66 or verse.book < 0:
            return False
        if verse.chapter >= len(Bible[verse.book]) or verse.chapter < 0:
            return False
        if verse.verse > Bible[verse.book][verse.chapter] or verse.verse < 0:
            return False
        return True

    @staticmethod
    def previous_verse(verse):
        # Previous Verse, Same Chapter
        if verse.verse > 0:
            new_verse = verse.verse - 1
            return Verse(
                book=verse.book,
                chapter=verse.chapter,
                verse=new_verse
            )
        else:
            # Last Verse, Previous Chapter
            if verse.chapter > 0:
                new_chapter = verse.chapter - 1
                new_verse = Bible[verse.book][new_chapter] - 1
                return Verse(
                    book=verse.book,
                    chapter=new_chapter,
                    verse=new_verse
                )
            # Last Verse, Previous Book
            else:
                new_book = verse.book - 1
                new_chapter = len(Bible[new_book]) - 1
                new_verse = Bible[new_book][new_chapter] - 1
                return Verse(
                    book=new_book,
                    chapter=new_chapter,
                    verse=new_verse
                )

    @staticmethod
    def next_verse(verse):
        # Next Verse, Same Chapter
        if verse.verse < Bible[verse.book][verse.chapter] - 1:
            new_verse = verse.verse + 1
            return Verse(
                book=verse.book,
                chapter=verse.chapter,
                verse=new_verse
            )
        else:
            # First Verse, Next Chapter
            if verse.chapter < len(Bible[verse.book]) - 1:
                new_chapter = verse.chapter + 1
                new_verse = 0
                return Verse(
                    book=verse.book,
                    chapter=new_chapter,
                    verse=new_verse
                )
            # First Verse, Next Book
            else:
                new_book = verse.book + 1
                new_chapter = 0
                new_verse = 0
                return Verse(
                    book=new_book,
                    chapter=new_chapter,
                    verse=new_verse
                )
