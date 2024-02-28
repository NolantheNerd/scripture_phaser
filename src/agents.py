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

import requests
from unicodedata import normalize
from src.enums import Bible
from src.enums import Bible_Books
from src.enums import Reverse_Bible_Books
from meaningless.bible_web_extractor import WebExtractor


# Remains Distinct from BibleGateway Agent in the Event that Another API is
# Needs to be Used
class BaseAPIAgent:
    def __init__(self, translation):
        self.translation = translation

    def _fetch(self, ref):
        raise NotImplementedError("Child agent must implement _fetch()")

    def _clean(self, text):
        return text

    def _split(self, text):
        return text

    def get(self, ref):
        return self._split(self._clean(self._fetch(ref)))


class BibleGatewayAgent(BaseAPIAgent):
    def __init__(self, translation):
        self.translation = translation
        self.xtcr = WebExtractor(
            translation=self.translation,
            show_passage_numbers=False,
            output_as_list=True,
            strip_excess_whitespace_from_list=False,
            use_ascii_punctuation=True
        )

    def _fetch(self, ref):
        b1 = Bible_Books[ref.book_start]
        c1 = ref.chapter_start + 1
        v1 = ref.verse_start + 1
        b2 = Bible_Books[ref.book_end]
        c2 = ref.chapter_end + 1
        v2 = ref.verse_end + 1

        if b1 == b2:
            return self.xtcr.get_passage_range(
                book=b1,
                chapter_from=c1,
                passage_from=v1,
                chapter_to=c2,
                passage_to=v2
            )
        else:
            verses = []
            while b1 != b2:
                verses.extend(self.xtcr.get_passage_range(
                        book=b1,
                        chapter_from=c1,
                        passage_from=v1,
                        chapter_to=len(Bible[b1]),
                        passage_to=Bible[b1][-1]
                    )
                )
                b1 = Bible_Books[Reverse_Bible_Books[b1] + 1]
                c1, v1 = 0, 0

            verses.extend(self.xtcr.get_passage_range(
                    book=b1,
                    chapter_from=c1,
                    passage_from=v1,
                    chapter_to=c2,
                    passage_to=v2
                )
            )
            return verses

class KJVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            translation="KJV"
        )


class WEBBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            translation="WEB"
        )


class ESVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            translation="ESV"
        )


class NIVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            translation="NIV"
        )


class NKJVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            translation="NKJV"
        )


class NLTBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            translation="NLT"
        )


class NASBBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            translation="NASB"
        )


class NRSVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            translation="NRSV"
        )


Agents = {
    "ESV": ESVBibleGatewayAgent(),
    "NIV": NIVBibleGatewayAgent(),
    "NASB": NASBBibleGatewayAgent(),
    "NLT": NLTBibleGatewayAgent(),
    "KJV": KJVBibleGatewayAgent(),
    "NKJV": NKJVBibleGatewayAgent(),
    "WEB": WEBBibleGatewayAgent(),
    "NRSV": NRSVBibleGatewayAgent()
}
