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

from pathlib import Path
from typing import List, Dict
from scripture_phaser.backend.enums import Bible
from scripture_phaser.backend.enums import Bible_Books
from scripture_phaser.backend.enums import Reverse_Bible_Books
from meaningless.bible_web_extractor import WebExtractor


TRANSLATION_DIR = Path(__file__).parent.parent.absolute()


# Remains Distinct from BibleGateway Agent in the Event that Another API Needs
# to be Used
class BaseAPIAgent:
    def __init__(self, translation: str) -> None:
        self.translation = translation

    def fetch(
        self,
        book_start: int,
        chapter_start: int,
        verse_start: int,
        book_end: int,
        chapter_end: int,
        verse_end: int,
    ) -> List[str]:
        raise NotImplementedError("Child agent must implement fetch()")


class OfflineTextAgent:
    def __init__(self, translation: str) -> None:
        self.translation = translation

    def fetch(self, id_start: int, id_end: int) -> List[str]:
        text = []

        translation_filepath = TRANSLATION_DIR + self.translation.lower() + ".txt"
        with open(translation_filepath, "r") as translation_file:
            for _ in range(id_start):
                next(translation_file)
            for _ in range(id_end - id_start):
                text.append(translation_file.readline())

        return text


class BibleGatewayAgent(BaseAPIAgent):
    def __init__(self, translation: str) -> None:
        self.translation = translation
        self.xtcr = WebExtractor(
            show_passage_numbers=False,
            translation=self.translation,
            output_as_list=True,
            strip_excess_whitespace_from_list=True,
            use_ascii_punctuation=True,
        )

    def fetch(
        self,
        book_start: int,
        chapter_start: int,
        verse_start: int,
        book_end: int,
        chapter_end: int,
        verse_end: int,
    ) -> List[str]:
        book_start = Bible_Books[book_start]
        chapter_start += 1
        verse_start += 1
        book_end = Bible_Books[book_end]
        chapter_end += 1
        verse_end += 1

        if book_start == book_end:
            return self.xtcr.get_passage_range(
                book=book_start,
                chapter_from=chapter_start,
                passage_from=verse_start,
                chapter_to=chapter_end,
                passage_to=verse_end,
            )
        else:
            verses = []
            while book_start != book_end:
                verses.extend(
                    self.xtcr.get_passage_range(
                        book=book_start,
                        chapter_from=chapter_start,
                        passage_from=verse_start,
                        chapter_to=len(Bible[Reverse_Bible_Books[book_start]]),
                        passage_to=Bible[Reverse_Bible_Books[book_start]][-1],
                    )
                )
                book_start = Bible_Books[Reverse_Bible_Books[book_start] + 1]
                chapter_start, verse_start = 0, 0

            verses.extend(
                self.xtcr.get_passage_range(
                    book=book_start,
                    chapter_from=chapter_start,
                    passage_from=verse_start,
                    chapter_to=chapter_end,
                    passage_to=verse_end,
                )
            )
            return verses


class KJVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self) -> None:
        super().__init__(translation="KJV")


class WEBBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self) -> None:
        super().__init__(translation="WEB")


class ESVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self) -> None:
        super().__init__(translation="ESV")


class NIVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self) -> None:
        super().__init__(translation="NIV")


class NKJVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self) -> None:
        super().__init__(translation="NKJV")


class NLTBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self) -> None:
        super().__init__(translation="NLT")


class NASBBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self) -> None:
        super().__init__(translation="NASB")


class NRSVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self) -> None:
        super().__init__(translation="NRSV")


Agents: Dict[str, BibleGatewayAgent] = {
    "ESV": ESVBibleGatewayAgent(),
    "NIV": NIVBibleGatewayAgent(),
    "NASB": NASBBibleGatewayAgent(),
    "NLT": NLTBibleGatewayAgent(),
    "KJV": KJVBibleGatewayAgent(),
    "NKJV": NKJVBibleGatewayAgent(),
    "WEB": WEBBibleGatewayAgent(),
    "NRSV": NRSVBibleGatewayAgent(),
}
