import re
import requests
from unicodedata import normalize
from xdg.BaseDirectory import save_data_path
from xdg.BaseDirectory import save_config_path
from scripture_phaser.enums import App
from scripture_phaser.enums import Agents
from scripture_phaser.enums import Translations

class BaseAgent:
    def __init__(self, agent):
        self.agent = agent

        if agent is Agents.BibleGateway:
            self.api += f"version={self.translation}&"

        self.data_path = save_data_path(App.Name.value)
        self.config_path = save_config_path(App.Name.value)

    def _fetch(self, ref):
        raise NotImplementedError("Child agent must implement _fetch()")

    def _clean(self, text):
        raise NotImplementedError("Child agent must implement _clean()")

    def get(self, ref):
        return self._clean(self._fetch(ref))

class BibleGatewayAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.BibleGateway
        )

    def _fetch(self, ref):
        raise NotImplementedError()

    def _clean(self, text):
        raise NotImplementedError()

class ESVBibleGatewayAgent(BibleGatewayAgent):
    def __init__(self):
        super().__init__()
        self.api = "https://www.biblegateway.com/passage/?version=ESV"

class ESVAPIAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.ESVAPI,
        )

    def _fetch(self, ref):
        headers = {"Authorization": "Token %s" % self.api_key}
        # @@@ TODO Allow ESV API params to be configured by user
        params = {
            "q": ref,
            "include-passage-references": False,
            "include-footnotes": False,
            "include-headings": False,
            "include-short-copyright": False,
            "include-selahs": False,
            "include-verse-numbers": False,
            "indent-paragraphs": 0,
            "indent-poetry": False,
            "indent-declares": 0,
            "indent-psalm-doxology": 0
        }
        resp = requests.get(self.api, params=params, headers=headers).json()
        return resp["passages"][0]

    def _clean(self, text):
        text = re.sub("“", "\"", text)
        text = re.sub("”", "\"", text)
        text = re.sub("—", "-", text)
        return normalize("NFKD", text)
