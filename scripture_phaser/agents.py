import re
import requests
from unicodedata import normalize
from scripture_phaser.enums import Agents
from scripture_phaser.enums import Translations
from scripture_phaser.verse import Verse
from scripture_phaser.enums import Bible
from scripture_phaser.enums import Bible_Books
from scripture_phaser.enums import Reverse_Bible_Books
from scripture_phaser.passage import Passage
from meaningless.bible_web_extractor import WebExtractor

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

class ESVAPIAgent(BaseAPIAgent):
    def __init__(self, api_key):
        self.api = Agents.ESVAPI.value
        self.api_key = api_key

        super().__init__(
            agent=Agents.ESVAPI
        )

    def _fetch(self, ref):
        headers = {"Authorization": "Token %s" % self.api_key}
        params = {
            "q": ref,
            "include-passage-references": False,
            "include-footnotes": False,
            "include-headings": False,
            "include-short-copyright": False,
            "include-selahs": False,
            "include-verse-numbers": True,
            "indent-paragraphs": 0,
            "indent-poetry": False,
            "indent-declares": 0,
            "indent-psalm-doxology": 0
        }
        resp = requests.get(self.api, params=params, headers=headers).json()
        return resp["passages"][0]

    def _clean(self, text):
        # ESV API always returns 2 "\n" at the end
        text = text[:-2]

        text = re.sub("“", "\"", text)
        text = re.sub("”", "\"", text)
        text = re.sub("—", "-", text)

        return normalize("NFKD", text)

    def _split(self, text):
        verse_number_pattern = re.compile(r" *\[[0-9]+\] *")

        # Always starts with a verse marker leaving the 0th element empty
        return re.split(verse_number_pattern, text)[1:]

class KJVAPIAgent(BaseAPIAgent):
    def __init__(self):
        self.api = Agents.KJVAPI.value

        super().__init__(
            agent=Agents.KJVAPI
        )

    def _fetch(self, ref):
        params = {
            "translation": "kjv",
            "verse_numbers": True
        }
        resp = requests.get(f"{self.api}{ref}", params=params).json()
        return resp["text"]

    def _clean(self, text):
        # Bible-API Always Keeps 1 "\n" at the end of the returned text
        text = text[:-1]

        return text

    def _split(self, text):
        verse_number_pattern = re.compile(r" *\([0-9]+\) *")

        # Always starts with a verse marker leaving the 0th element empty
        return re.split(verse_number_pattern, text)[1:]

class WEBAPIAgent(BaseAPIAgent):
    def __init__(self):
        self.api = Agents.WEBAPI.value

        super().__init__(
            agent=Agents.WEBAPI
        )

    def _fetch(self, ref):
        params = {
            "translation": "web",
            "verse_numbers": True
        }
        resp = requests.get(f"{self.api}{ref}", params=params).json()
        return resp["text"]

    def _clean(self, text):
        # Bible-API Always Keeps 1 "\n" at the end of the returned text
        text = text[:-1]

        return text

    def _split(self, text):
        verse_number_pattern = re.compile(r" *\([0-9]+\) *")

        # Always starts with a verse marker leaving the 0th element empty
        return re.split(verse_number_pattern, text)[1:]

class BBEAPIAgent(BaseAPIAgent):
    def __init__(self):
        self.api = Agents.BBEAPI.value

        super().__init__(
            agent=Agents.BBEAPI
        )

    def _fetch(self, ref):
        params = {
            "translation": "bbe",
            "verse_numbers": True
        }
        resp = requests.get(f"{self.api}{ref}", params=params).json()
        return resp["text"]

    def _clean(self, text):
        return text

    def _split(self, text):
        verse_number_pattern = re.compile(r" *\([0-9]+\) *")

        # Always starts with a verse marker leaving the 0th element empty
        return re.split(verse_number_pattern, text)[1:]

class BibleGatewayAgent:
    def __init__(self, agent):
        self.agent = agent
        self.xtcr = WebExtractor(
            translation=self.agent.value,
            show_passage_numbers=False,
            output_as_list=True,
            strip_excess_whitespace_from_list=True,
            use_ascii_punctuation=True
        )

    def get(self, ref):
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(ref)

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
