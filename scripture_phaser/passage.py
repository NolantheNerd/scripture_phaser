from scripture_phaser.enums import Bible
from scripture_phaser.verse import Verse
from scripture_phaser.agents import ESVAPIAgent
from scripture_phaser.enums import Reverse_Bible_Books
from scripture_phaser.exceptions import InvalidReference

class Passage:
    def __init__(self, reference, translation):
        self.translation = translation
        self.reference = self.clean_reference(reference)
        self.verses = self.reference_to_verses(self.reference)

    @staticmethod
    def clean_reference(ref):
        ref = ref.strip().lower().title()

        new_ref = ""
        prev_char = ""
        for i, char in enumerate(ref):
            next_char = ref[min(len(ref)-1, i+1)]
            # Insert Space After Book Name and Before Chapter/Verse Number
            if char.isdigit() and prev_char.isalpha():
                new_ref += " "

            # Insert Space After Verse Number and Before Second Book Name
            elif char.isalpha() and prev_char.isdigit():
                new_ref += " "

            # Insert Space Between Number and "-"
            elif char == "-" and prev_char != " " and prev_char != "":
                new_ref += " "

            # Insert Space Between "-" and Number/Book
            elif prev_char == "-" and char != " ":
                new_ref += " "

            elif char == " ":
                # Remove Space Before ":" and After Chapter Number
                if prev_char.isdigit() and next_char == ":":
                    continue
                # Remove Space After ":" and Before Verse Number
                elif prev_char == ":" and next_char.isdigit():
                    continue

            prev_char = ref[max(0, i-1)]
            new_ref += ref[i]

        new_ref = new_ref \
            .replace("Psalm", "Psalms") \
            .replace("First", "One") \
            .replace("1 Samuel", "One Samuel") \
            .replace("1 Kings", "One Kings") \
            .replace("1 Chronicles", "One Chronicles") \
            .replace("1 Corinthians", "One Corinthians") \
            .replace("1 Thessalonians", "One Thessalonians") \
            .replace("1 Timothy", "One Timothy") \
            .replace("1 Peter", "One Peter") \
            .replace("1 John", "One John") \
            .replace("Second", "Two") \
            .replace("2 Samuel", "Two Samuel") \
            .replace("2 Kings", "Two Kings") \
            .replace("2 Chronicles", "Two Chronicles") \
            .replace("2 Corinthians", "Two Corinthians") \
            .replace("2 Thessalonians", "Two Thessalonians") \
            .replace("2 Timothy", "Two Timothy") \
            .replace("2 Peter", "Two Peter") \
            .replace("2 John", "Two John") \
            .replace("Third", "Three") \
            .replace("3 John", "Three John")

        return new_ref

    @classmethod
    def reference_to_verses(cls, ref):
        # Handle a Single Whole Book Reference [Genesis]
        if ref in Reverse_Bible_Books:
            book1 = Reverse_Bible_Books.get(ref, -1)
            book2 = book1
            chapter1 = 0
            chapter2 = len(Bible[book2]) - 1
            verse1 = 0
            verse2 = Bible[book2][chapter2] - 1

        else:
            ref_components = ref.split(" - ")

            # No Split Reference (no "-")
            if len(ref_components) == 1:
                split_components = ref_components[0].split(" ")

                # Get Book Name (Even if it is Multiple Words)
                i = 0
                while i < len(split_components) and split_components[i].isalpha():
                    i += 1
                book1 = book2 = Reverse_Bible_Books.get(" ".join(split_components[:i]), -1)

                # Get Chapter:Verse Split
                loc_components = split_components[-1].split(":")

                if len(loc_components) == 1:
                    # Handle Single Chapter Books (Jude 10)
                    if len(Bible[book1]) == 1:
                        chapter1 = chapter2 = 0
                        verse1 = verse2 = int(loc_components[0]) - 1
                    # Handle Entire Chapter References (John 1)
                    else:
                        chapter1 = chapter2 = int(loc_components[0]) - 1
                        verse1 = 0
                        verse2 = Bible[book1][chapter1] - 1

                # Handle Single Verse References [John 1:1]
                else:
                    chapter1 = chapter2 = int(loc_components[0]) - 1
                    verse1 = verse2 = int(loc_components[1]) - 1

            # Split Reference (one "-")
            elif len(ref_components) == 2:
                # Handle First Half of Split
                split_components = ref_components[0].split(" ")

                # Get Book Name (Even if it is Multiple Words)
                i = 0
                while i < len(split_components) and split_components[i].isalpha():
                    i += 1
                book1 = Reverse_Bible_Books.get(" ".join(split_components[:i]), -1)

                # Get Chapter:Verse Split (if part of reference isn't book name)
                if not split_components[-1].isalpha():
                    loc_components = split_components[-1].split(":")

                    if len(loc_components) == 1:
                        # Handle Single Chapter Books (Jude 10)
                        if len(Bible[book1]) == 1:
                            chapter1 = 0
                            verse1 = int(loc_components[0]) - 1
                        # Handle Entire Chapter References (John 1)
                        else:
                            chapter1 = int(loc_components[0]) - 1
                            verse1 = 0

                    # Handle Single Verse References [John 1:1]
                    else:
                        chapter1 = int(loc_components[0]) - 1
                        verse1 = int(loc_components[1]) - 1
                # Handle Just a Book (Genesis)
                else:
                    chapter1 = verse1 = 0

                # Handle Second Half of Split
                split_components = ref_components[1].split(" ")

                # Check for Book Name
                if split_components[0].isalpha():
                    # Get Book Name (Even if it is Multiple Words)
                    i = 0
                    while i < len(split_components) and split_components[i].isalpha():
                        i += 1
                    book2 = Reverse_Bible_Books.get(" ".join(split_components[:i]), -1)
                # Second Book is Not Specified [John 1:1 - 1:2]
                else:
                    book2 = book1

                # Get Chapter:Verse Split (if part of reference isn't book name)
                if not split_components[-1].isalpha():
                    loc_components = split_components[-1].split(":")

                    if len(loc_components) == 1:
                        # Handle Single Chapter Books (Jude 10)
                        if len(Bible[book1]) == 1:
                            chapter2 = 0
                            verse2 = int(loc_components[0]) - 1
                        # Handle Entire Chapter References (John 1)
                        else:
                            chapter2 = int(loc_components[0]) - 1
                            verse2 = Bible[book2][chapter2] - 1

                    # Handle Single Verse References [John 1:1]
                    else:
                        chapter2 = int(loc_components[0]) - 1
                        verse2 = int(loc_components[1]) - 1
                # Handle Just a Book (Genesis)
                else:
                    chapter2 = len(Bible[book2]) - 1
                    verse2 = Bible[book2][chapter2] - 1

            # More than One Split is No Good (two+ "-")
            else:
                raise InvalidReference(ref)

        first_verse = Verse(book1, chapter1, verse1)
        last_verse = Verse(book2, chapter2, verse2)
        cls.validate(first_verse, last_verse)

        if Verse.verse_equal(first_verse, last_verse):
            return [first_verse]
        else:
            return cls.infill_verse([first_verse, last_verse])

    @classmethod
    def infill_verse(cls, verses):
        new_verse = Verse.next_verse(verses[-2])
        while not Verse.verse_equal(verses[-1], new_verse):
            verses.insert(-1, new_verse)
            new_verse = Verse.next_verse(verses[-2])
        return verses

    @classmethod
    def validate(cls, start_verse, end_verse):
        if (
            not start_verse.valid or \
            not end_verse.valid or \
            not cls.validate_verse_pair(start_verse, end_verse) \
        ):
            raise InvalidReference(ref)

    @staticmethod
    def validate_verse_pair(verse1, verse2):
        if verse1.book > verse2.book:
            return False
        elif verse1.book == verse2.book:
            if verse1.chapter > verse2.chapter:
                return False
            elif verse1.chapter == verse2.chapter:
                if verse1.verse > verse2.verse:
                    return False
        return True
