# scripture_phaser helps you to memorize the Bible.
# Copyright (C) 2023-2024 Nolan McMahon
#
# This file is part of scripture_phaser.
#
# scripture_phaser is licensed under the terms of the BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from src.enums import Bible
from src.enums import Bible_Books
from src.enums import Reverse_Bible_Books
from src.exceptions import InvalidReference


class Reference:
    def __init__(self, reference):
        if reference.strip() == "":
            self.empty = True
            self.ref_str = ""
        else:
            self.empty = False

            self.book_start, self.chapter_start, self.verse_start, \
            self.book_end, self.chapter_end, self.verse_end = \
                self.interpret_reference(reference)

            self.ref_str = self.standardize_reference()

    @staticmethod
    def reference_replacements(ref):
        # Replace "Psalm" -> "Psalms" will also turn "Psalms" -> "Psalmss"
        ref = ref \
            .replace(".", "") \
            .replace("Psalm", "Psalms") \
            .replace("Psalmss", "Psalms") \
            .replace("First", "One") \
            .replace("Second", "Two") \
            .replace("Third", "Three") \
            .replace("1 Samuel", "One Samuel") \
            .replace("1 Kings", "One Kings") \
            .replace("1 Chronicles", "One Chronicles") \
            .replace("1 Corinthians", "One Corinthians") \
            .replace("1 Thessalonians", "One Thessalonians") \
            .replace("1 Timothy", "One Timothy") \
            .replace("1 Peter", "One Peter") \
            .replace("1 John", "One John") \
            .replace("2 Samuel", "Two Samuel") \
            .replace("2 Kings", "Two Kings") \
            .replace("2 Chronicles", "Two Chronicles") \
            .replace("2 Corinthians", "Two Corinthians") \
            .replace("2 Thessalonians", "Two Thessalonians") \
            .replace("2 Timothy", "Two Timothy") \
            .replace("2 Peter", "Two Peter") \
            .replace("2 John", "Two John") \
            .replace("3 John", "Three John") \
            .replace("Gen ", "Genesis ") \
            .replace("Ex ", "Exodus ") \
            .replace("Lev ", "Leviticus ") \
            .replace("Num ", "Numbers ") \
            .replace("Deut ", "Deuteronomy ") \
            .replace("Josh ", "Joshua ") \
            .replace("Judg ", "Judges ") \
            .replace("1Sam ", "One Samuel ") \
            .replace("1sam ", "One Samuel ") \
            .replace("1 Sam ", "One Samuel ") \
            .replace("2Sam ", "Two Samuel ") \
            .replace("2sam ", "Two Samuel ") \
            .replace("2 Sam ", "Two Samuel ") \
            .replace("1Chron ", "One Chronicles ") \
            .replace("1chron ", "One Chronicles ") \
            .replace("1 Chron ", "One Chronicles ") \
            .replace("Neh ", "Nehemiah ") \
            .replace("Est ", "Esther ") \
            .replace("Ps ", "Psalms ") \
            .replace("Prov ", "Proverbs ") \
            .replace("Eccles ", "Ecclesiastes ") \
            .replace("Song ", "Song of Songs ") \
            .replace("Isa ", "Isaiah ") \
            .replace("Jer ", "Jeremiah ") \
            .replace("Lam ", "Lamentations ") \
            .replace("Ezek ", "Ezekiel ") \
            .replace("Dan ", "Daniel ") \
            .replace("Hos ", "Hosea ") \
            .replace("Obad ", "Obadiah ") \
            .replace("Mic ", "Micah ") \
            .replace("Nah ", "Nahum ") \
            .replace("Hab ", "Habakkuk ") \
            .replace("Zeph ", "Zephaniah ") \
            .replace("Hag ", "Haggai ") \
            .replace("Zech ", "Zechariah ") \
            .replace("Mal ", "Malachi ") \
            .replace("Matt ", "Matthew ") \
            .replace("Rom ", "Romans ") \
            .replace("1Cor ", "One Corinthians ") \
            .replace("1cor ", "One Corinthians ") \
            .replace("1 Cor ", "One Corinthians ") \
            .replace("2Cor ", "Two Corinthians ") \
            .replace("2cor ", "Two Corinthians ") \
            .replace("2 Cor ", "Two Corinthians ") \
            .replace("Gal ", "Galatians ") \
            .replace("Eph ", "Ephesians ") \
            .replace("Phil ", "Philippians ") \
            .replace("Col ", "Colossians ") \
            .replace("1Thess ", "One Thessalonians ") \
            .replace("1thess ", "One Thessalonians ") \
            .replace("1 Thess ", "One Thessalonians ") \
            .replace("2Thess ", "Two Thessalonians ") \
            .replace("2thess ", "Two Thessalonians ") \
            .replace("2 Thess ", "Two Thessalonians ") \
            .replace("1Tim ", "One Timothy ") \
            .replace("1tim ", "One Timothy ") \
            .replace("1 Tim ", "One Timothy ") \
            .replace("2Tim ", "Two Timothy ") \
            .replace("2tim ", "Two Timothy ") \
            .replace("2 Tim ", "Two Timothy ") \
            .replace("Philem ", "Philemon ") \
            .replace("Heb ", "Hebrews ") \
            .replace("1Pet ", "One Peter ") \
            .replace("1pet ", "One Peter ") \
            .replace("1 Pet ", "One Peter ") \
            .replace("2Pet ", "Two Peter ") \
            .replace("2pet ", "Two Peter ") \
            .replace("2 Pet ", "Two Peter ") \
            .replace("Rev ", "Revelation ")

        return ref

    @classmethod
    def clean_reference(cls, ref):
        ref = " ".join(ref.split()) # Multiple Whitespaces -> One Whitespace
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
                    prev_char = ref[max(0, i)]
                    continue
                # Remove Space After ":" and Before Verse Number
                elif prev_char == ":" and next_char.isdigit():
                    prev_char = ref[max(0, i)]
                    continue

            prev_char = ref[max(0, i)]
            new_ref += ref[i]

        new_ref = cls.reference_replacements(new_ref)

        return new_ref

    @classmethod
    def interpret_reference(cls, ref):
        ref = cls.clean_reference(ref)

        # Handle a Single Whole Book Reference [Genesis]
        if ref in Reverse_Bible_Books:
            book_start = Reverse_Bible_Books.get(ref, -1)
            book_end = book_start
            chapter_start = 0
            chapter_end = len(Bible[book_end]) - 1
            verse_start = 0
            verse_end = Bible[book_end][chapter_end] - 1

        else:
            ref_components = ref.split(" - ")

            # No Split Reference (no "-")
            if len(ref_components) == 1:
                split_components = ref_components[0].split(" ")

                # Get Book Name (Even if it is Multiple Words)
                i = 0
                while i < len(split_components) and split_components[i].isalpha():
                    i += 1
                book_start = book_end = Reverse_Bible_Books.get(" ".join(split_components[:i]), -1)

                # Book Name is not in the Bible (Billy)
                if book_start == -1:
                    raise InvalidReference(ref)

                # Get Chapter:Verse Split
                loc_components = split_components[-1].split(":")

                if len(loc_components) == 1:
                    # Handle Single Chapter Books (Jude 10)
                    if len(Bible[book_start]) == 1:
                        chapter_start = chapter_end = 0
                        verse_start = verse_end = int(loc_components[0]) - 1
                    # Handle Entire Chapter References (John 1)
                    else:
                        chapter_start = chapter_end = int(loc_components[0]) - 1
                        verse_start = 0
                        verse_end = Bible[book_start][chapter_start] - 1

                # Handle Single Verse References [John 1:1]
                else:
                    chapter_start = chapter_end = int(loc_components[0]) - 1
                    verse_start = verse_end = int(loc_components[1]) - 1

            # Split Reference (one "-")
            elif len(ref_components) == 2:
                # Handle First Half of Split
                split_components = ref_components[0].split(" ")

                # Get Book Name (Even if it is Multiple Words)
                i = 0
                while i < len(split_components) and split_components[i].isalpha():
                    i += 1
                book_start = Reverse_Bible_Books.get(" ".join(split_components[:i]), -1)

                # Book Name is not in the Bible (Billy)
                if book_start == -1:
                    raise InvalidReference(ref)

                # Get Chapter:Verse Split (if part of reference isn't book name)
                if not split_components[-1].isalpha():
                    loc_components = split_components[-1].split(":")

                    if len(loc_components) == 1:
                        # Handle Single Chapter Books (Jude 10)
                        if len(Bible[book_start]) == 1:
                            chapter_start = 0
                            verse_start = int(loc_components[0]) - 1
                        # Handle Entire Chapter References (John 1)
                        else:
                            chapter_start = int(loc_components[0]) - 1
                            verse_start = 0

                    # Handle Single Verse References [John 1:1]
                    else:
                        chapter_start = int(loc_components[0]) - 1
                        verse_start = int(loc_components[1]) - 1
                # Handle Just a Book (Genesis)
                else:
                    chapter_start = verse_start = 0

                # Handle Second Half of Split
                split_components = ref_components[1].split(" ")

                # Check for Book Name
                if split_components[0].isalpha():
                    # Get Book Name (Even if it is Multiple Words)
                    i = 0
                    while i < len(split_components) and split_components[i].isalpha():
                        i += 1
                    book_end = Reverse_Bible_Books.get(" ".join(split_components[:i]), -1)
                # Second Book is Not Specified [John 1:1 - 1:2]
                else:
                    book_end = book_start

                # Book Name is not in the Bible (Billy)
                if book_end == -1:
                    raise InvalidReference(ref)

                # Get Chapter:Verse Split (if part of reference isn't book name)
                if not split_components[-1].isalpha():
                    loc_components = split_components[-1].split(":")

                    if len(loc_components) == 1:
                        # Handle Single Chapter Books (Jude 10)
                        if len(Bible[book_end]) == 1:
                            chapter_end = 0
                            verse_end = int(loc_components[0]) - 1
                        # Handle Entire Chapter References (John 1)
                        # Handle Chapter Ranges (John 1 - 2)
                        elif book_end != book_start or ":" not in ref_components[0]:
                            chapter_end = int(loc_components[0]) - 1
                            verse_end = Bible[book_end][chapter_end] - 1
                        # Handle Single Values As Verses not Chapters (John 1:4 - 6)
                        else:
                            chapter_end = chapter_start
                            verse_end = int(loc_components[0]) - 1

                    # Handle Single Verse References [John 1:1]
                    else:
                        chapter_end = int(loc_components[0]) - 1
                        verse_end = int(loc_components[1]) - 1
                # Handle Just a Book (Genesis)
                else:
                    chapter_end = len(Bible[book_end]) - 1
                    verse_end = Bible[book_end][chapter_end] - 1

            # More than One Split is No Good (two+ "-")
            else:
                raise InvalidReference(ref)

        return book_start, chapter_start, verse_start, book_end, chapter_end, verse_end

    def standardize_reference(self):
        # Single Book Reference? - Only Print Book Name Once
        if self.book_start == self.book_end:
            # Single Chapter Book? - No ":"s
            if len(Bible[self.book_start]) == 1:
                # Single Verse? - No "-"
                if self.verse_start == self.verse_end:
                    return (
                        f"{Bible_Books[self.book_start]} "
                        f"{self.verse_start + 1}"
                    )
                # Multiple Verses - Yes "-"
                else:
                    return (
                        f"{Bible_Books[self.book_start]} "
                        f"{self.verse_start + 1}-{self.verse_end + 1}"
                    )
            # Multi Chapter Book - Yes ":"s
            else:
                # Reference Contained in 1 Chapter? - Only 1 ":"
                if self.chapter_start == self.chapter_end:
                    # Reference is a Single Verse? - No "-"
                    if self.verse_start == self.verse_end:
                        return (
                            f"{Bible_Books[self.book_start]} "
                            f"{self.chapter_start + 1}:{self.verse_start + 1}"
                        )
                    # Reference is Multiple Verses - Yes "-"
                    else:
                        return (
                            f"{Bible_Books[self.book_start]} "
                            f"{self.chapter_start + 1}:"
                            f"{self.verse_start + 1}-{self.verse_end + 1}"
                        )
                # Reference Spread Over Multiple Chapters - 2 ":"s
                else:
                    return (
                        f"{Bible_Books[self.book_start]} "
                        f"{self.chapter_start + 1}:{self.verse_start + 1}-"
                        f"{self.chapter_end + 1}:{self.verse_end + 1}"
                    )
        # Multiple Book Reference - Print Both Book Names
        else:
            # Both Books are Single Chapter Books? - No ":"s
            if len(Bible[self.book_start]) == 1 and len(Bible[self.book_end]) == 1:
                return (
                    f"{Bible_Books[self.book_start]} {self.verse_start + 1} "
                    f"- {Bible_Books[self.book_end]} {self.verse_end + 1}"
                )
            # Only First Book is a Single Chapter Book? - No ":" at Start
            elif len(Bible[self.book_start]) == 1:
                return (
                    f"{Bible_Books[self.book_start]} {self.verse_start + 1} "
                    f"- {Bible_Books[self.book_end]} {self.chapter_end + 1}:"
                    f"{self.verse_end + 1}"
                )
            # Only Last Book is a Single Chapter Book? - No ":" at End
            elif len(Bible[self.book_end]) == 1:
                return (
                    f"{Bible_Books[self.book_start]} {self.chapter_start + 1}:"
                    f"{self.verse_start + 1} - {Bible_Books[self.book_end]} "
                    f"{self.verse_end + 1}"
                )
            # Neither Book is a Single Chapter Book - Two ":"s
            else:
                return (
                    f"{Bible_Books[self.book_start]} {self.chapter_start + 1}:"
                    f"{self.verse_start + 1} - {Bible_Books[self.book_end]} "
                    f"{self.chapter_end + 1}:{self.verse_end + 1}"
                )
