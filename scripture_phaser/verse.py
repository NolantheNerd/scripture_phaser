from enums import Bible
from exceptions import InvalidReference

class Verse:
    def __init__(self, ref_string):
        book, chapter, verse = self.split_reference(ref_string)
        if not self.validate_reference(book, chapter, verse):
            raise InvalidReference(ref_string)
        self.ref = f"{book} {chapter}:{verse}"

    def split_reference(cls, ref_string):
        ref_string = ref_string.lower().title()

    def validate_reference(cls, book, chapter, verse):
        # Accomodate for chapter enum names starting with "_"
        chapter = f"_{chapter}"
        if book not in Bible.__members__:
            return False
        if chapter not in Bible[book].__members__:
            return False
        if verse > Bible[book][chapter].value:
            return False
        return True
