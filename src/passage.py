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
from src.verse import Verse
from src.agents import Agents
from src.enums import Reverse_Bible_Books
from src.exceptions import InvalidReference


class Passage:
    def __init__(self, reference, translation):
        self.agent = Agents[translation]
        self.reference = reference
        self.verses = self.reference_to_verses()
        self.populated = False

    def populate(self, texts=None):
        self.populated = True
        if texts is None:
            texts = self.agent.get(self.reference)
        for verse, text in zip(self.verses, texts):
            verse.initialize(text)

    def show(self, with_verse=False, with_ref=False):
        if not self.populated: return ""
        else:
            if with_verse:
                texts = [verse.show(with_verse=True) for verse in self.verses]
            else:
                texts = [verse.show() for verse in self.verses]

            text = " ".join(texts)

            # Spaces after new lines are no good
            text = text.replace("\n ", "\n")

            if with_ref:
                text = f"{text} - {self.reference.reference}"
            return text

    def reference_to_verses(self):
        first_verse = Verse(
            self.reference.book_start,
            self.reference.chapter_start,
            self.reference.verse_start
        )
        last_verse = Verse(
            self.reference.book_end,
            self.reference.chapter_end,
            self.reference.verse_end
        )
        self.validate(first_verse, last_verse)

        if Verse.verse_equal(first_verse, last_verse):
            return [first_verse]
        else:
            return self.infill_verse([first_verse, last_verse])

    @staticmethod
    def infill_verse(verses):
        new_verse = Verse.next_verse(verses[-2])
        while not Verse.verse_equal(verses[-1], new_verse):
            verses.insert(-1, new_verse)
            new_verse = Verse.next_verse(verses[-2])
        return verses

    def validate(self, start_verse, end_verse):
        if (
            not start_verse.valid or \
            not end_verse.valid or \
            not self.validate_verse_pair(start_verse, end_verse) \
        ):
            raise InvalidReference(self.reference)

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
