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
        raise NotImplementedError("Child agent must implement _clean()")

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
            agent=Agents.ESVAPI,
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
        verse_number_pattern = re.compile(r"\s*\[[0-9]+\]\s*")

        # Always starts with a verse marker leaving the 0th element empty
        return re.split(verse_number_pattern, text)[1:]
