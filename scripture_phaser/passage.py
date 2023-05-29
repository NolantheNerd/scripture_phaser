from scripture_phaser.enums import Bible
from scripture_phaser.exceptions import InvalidReference
from scripture_phaser.exceptions import InvalidReferenceFormat

class Passage:
    def __init__(self, ref_string, translation):
        self.translation = translation
        self.start_ref, self.end_ref = self.split_reference(ref_string)
        if (
            not self.validate_reference(self.start_ref) or \
            not self.validate_reference(self.end_ref) or \
            not self.validate_reference_pair(self.start_ref, self.end_ref) \
        ):
            raise InvalidReference(ref_string)
        self.text = self.translation.agent.fetch()

    @classmethod
    def split_reference(cls, ref_string):
        ref_string = ref_string.lower().title()
        ref_string = ref_string \
            .replace(" ", "_") \
            .replace("First", "One") \
            .replace("1_Samuel", "One_Samuel") \
            .replace("1_Kings", "One_Kings") \
            .replace("1_Chronicles", "One_Chronicles") \
            .replace("1_Corinthians", "One_Corinthians") \
            .replace("1_Thessalonians", "One_Thessalonians") \
            .replace("1_Timothy", "One_Timothy") \
            .replace("1_Peter", "One_Peter") \
            .replace("1_John", "One_John") \
            .replace("Second", "Two") \
            .replace("2_Samuel", "Two_Samuel") \
            .replace("2_Kings", "Two_Kings") \
            .replace("2_Chronicles", "Two_Chronicles") \
            .replace("2_Corinthians", "Two_Corinthians") \
            .replace("2_Thessalonians", "Two_Thessalonians") \
            .replace("2_Timothy", "Two_Timothy") \
            .replace("2_Peter", "Two_Peter") \
            .replace("2_John", "Two_John") \
            .replace("Third", "Three") \
            .replace("3 John", "Three_John")

        ref_components = ref_string.split("_")

        if len(ref_components) == 1:
            raise InvalidReferenceFormat()

        book = ref_components.pop(0)
        # Handle 2 Word Book Names
        if book in ["One", "Two", "Three"]:
            book = book + f"_{ref_components.pop(0)}"
        ref_components = "".join(ref_components).split("-")

        start_ref = ref_components[0].split(":")
        start_chapter = start_ref[0]
        # Handle No Verse in Reference
        if len(start_ref) == 1:
            start_verse = "1"
        else:
            start_verse = start_ref[1]

        # Handle Multiverse References
        if len(ref_components) == 2:
            end_ref = ref_components[1].split(":")
            end_chapter = end_ref[0]
            # Handle No Verse in Reference
            if len(end_ref) == 1:
                end_verse = str(Bible[book].value[f"_{end_chapter}"].value)
            else:
                end_verse = end_ref[1]
        else:
            end_chapter = start_chapter
            # Handle Single Chapter References
            if len(start_ref) == 1:
                end_verse = str(Bible[book].value[f"_{end_chapter}"].value)
            # Handle Single Verse References
            else:
                end_verse = start_verse

        return (book, start_chapter, start_verse), (book, end_chapter, end_verse)

    @classmethod
    def validate_reference(cls, ref):
        book, chapter, verse = ref
        # Accomodate for chapter enum names starting with "_"
        chapter = f"_{chapter}"
        if book not in Bible.__members__:
            return False
        if chapter not in Bible[book].value.__members__:
            return False
        if int(verse) > Bible[book].value[chapter].value:
            return False
        return True

    @classmethod
    def validate_reference_pair(cls, ref1, ref2):
        book1, chapter1, verse1 = ref1
        book2, chapter2, verse2 = ref2

        if book1 != book2:
            return False
        if int(chapter2) < int(chapter1):
            return False
        if int(chapter2) == int(chapter1) and int(verse2) < int(verse1):
            return False
        return True
