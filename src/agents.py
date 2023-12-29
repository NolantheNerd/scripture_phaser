# scripture_phaser helps you to memorize the Word of Truth.
# Copyright (C) 2023 Nolan McMahon
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

import re
import requests
from unicodedata import normalize
from src.enums import Agents
from src.enums import Bible
from src.enums import Bible_Books
from src.enums import Reverse_Bible_Books
from src.passage import Passage
from meaningless.bible_web_extractor import WebExtractor


# Remains Distinct from BibleGateway Agent in the Event that Another API is
# Needs to be Used
class BaseAPIAgent:
    def __init__(self, agent):
        self.agent = agent

    def _fetch(self, ref):
        raise NotImplementedError("Child agent must implement _fetch()")

    def _clean(self, text):
        return text

    def _split(self, text):
        return text

    def get(self, ref):
        return self._split(self._clean(self._fetch(ref)))


class BibleGatewayAgent(BaseAPIAgent):
    # @@@ TODO: Start Here ^^^ Maybe Don't Subclass? It's just
    # unpredictability in terms of which API will be used to
    # return data in the test_show() test in test_passage().
    # Maybe hard code the agent to use in the test?
    def __init__(self, agent):
        self.agent = agent
        self.xtcr = WebExtractor(
            translation=self.agent.value,
            show_passage_numbers=False,
            output_as_list=True,
            strip_excess_whitespace_from_list=False,
            use_ascii_punctuation=True
        )

    def _fetch(self, ref):
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(ref)
        b1 = Bible_Books[b1]
        c1 += 1
        v1 += 1
        b2 = Bible_Books[b2]
        c2 += 1
        v2 += 1

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
            agent=Agents.KJVBGW
        )


class WEBBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.WEBBGW
        )


class ESVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.ESVBGW
        )


class NIVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.NIVBGW
        )


class NKJVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.NKJVBGW
        )


class NLTBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.NLTBGW
        )


class NASBBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.NASBBGW
        )


class NRSVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.NRSVBGW
        )
