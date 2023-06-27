import re
import requests
from unicodedata import normalize
from xdg.BaseDirectory import save_data_path
from xdg.BaseDirectory import save_config_path
from scripture_phaser.enums import App
from scripture_phaser.enums import Bible
from scripture_phaser.enums import Agents
from scripture_phaser.enums import Translations
from scripture_phaser.verse import Verse
from scripture_phaser.enums import Reverse_Bible_Books

class BaseAgent:
    def __init__(self, agent):
        self.agent = agent
        self.data_path = save_data_path(App.Name.value)
        self.config_path = save_config_path(App.Name.value)

    def _fetch(self, ref):
        raise NotImplementedError("Child agent must implement _fetch()")

    def _clean(self, text):
        return text

    def _split(self, text):
        return text

    def get(self, ref):
        return self._split(self._clean(self._fetch(ref)))

class BibleGatewayAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.BibleGateway
        )

class ESVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__()
        self.api = "https://www.biblegateway.com/passage/?version=ESV"

class ESVAPIAgent(BaseAgent):
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

class KJVAPIAgent(BaseAgent):
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

class WEBAPIAgent(BaseAgent):
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
