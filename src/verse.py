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
from itertools import accumulate
from src.enums import Bible_Books
from src.reference import Reference


class Verse:
    def __init__(self, book, chapter, verse, text=None):
        self.book = book
        self.chapter = chapter
        self.verse = verse
        self.reference = Reference(f"{Bible_Books[self.book]} {self.chapter + 1}:{self.verse + 1}")
        self.valid = self.validate(self)

        self.id = self.reference_to_id(self.reference)

        self.initialized = text is not None
        if self.initialized:
            self.initialize(text)

    def initialize(self, text, require_passage_numbers=False):
        self.initialized = True
        if require_passage_numbers:
            self.text = f"[{self.verse+1}] " + text
        else:
            self.text = text
        self.length = len(self.text)
        self.n_words = len(self.text.split())

    def show(self, with_verse=False, with_ref=False):
        if not self.initialized:
            return ""

        text = self.text
        if with_verse:
            text = f"[{self.verse+1}] {text}"
        if with_ref:
            text = f"{text} - {self.reference.ref_str}"

        return text

    @staticmethod
    def reference_to_id(ref):
        if ref.book_start == ref.book_end and \
        ref.chapter_start == ref.chapter_end and \
        ref.verse_start == ref.verse_end:
            pass
        else:
            pass
            

    @staticmethod
    def id_to_reference(id):
        verse_sums = list(accumulate([sum(book) for book in Bible]))
        book_id = [id <= bound for bound in verse_sums].index(True)

        if book_id > 0:
            id -= verse_sums[book_id - 1]

        book_sums = list(accumulate(Bible[book_id]))
        chapter_id = [id <= bound for bound in book_sums].index(True)

        if chapter_id > 0:
            id -= book_sums[chapter_id - 1]

        return Reference(f"{Bible_Books[book_id]} {chapter_id + 1}:{id + 1}")

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
