# helps you to memorize the Word of Truth.
# Copyright (C) 2023 Nolan McMahon
#
# This file is part of.
#
# is licensed under the terms of the BSD 3-Clause License
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
from src.exceptions import InvalidReference

class Verse:
    def __init__(self, book, chapter, verse, text=None):
        self.book = book
        self.chapter = chapter
        self.verse = verse
        self.reference = f"{Bible_Books.get(self.book, None)} {self.chapter+1}:{self.verse+1}"
        self.valid = self.validate(self)

        self.initialized = text is not None
        if self.initialized:
            self.initialize(text)

    def initialize(self, text):
        self.initialized = True
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
            text = f"{text} - {self.reference}"

        return text

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
