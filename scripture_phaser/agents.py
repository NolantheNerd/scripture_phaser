import pdb
import requests
from dotenv import dotenv_values
from unicodedata import normalize
from xdg.BaseDirectory import save_data_path
from xdg.BaseDirectory import save_config_path
from xdg.BaseDirectory import load_first_config
from scripture_phaser.enums import App
from scripture_phaser.enums import Agents
from scripture_phaser.enums import Translations
from scripture_phaser.exceptions import MissingAPIKey

class BaseAgent:
    def __init__(self, agent, translation):
        self.Name = agent.name
        self.api = agent.value

        if agent is Agents.BibleGateway:
            self.api += f"version={self.translation}&"

        self.data_path = save_data_path(App.Name.value)
        self.config_path = save_config_path(App.Name.value)

    def _fetch(self, ref):
        raise NotImplementedError("Child agent must implement _fetch()")

    def _clean(self, text):
        raise NotImplementedError("Child agent must implement _clean()")

    def get(self, ref):
        self.text = self._clean(self._fetch(ref))

class BibleGatewayAgent(BaseAgent):
    def __init__(self, translation):
        super().__init__(
            agent=Agents.BibleGateway,
            translation=translation
        )

    def _fetch(self, ref):
        raise NotImplementedError()

    def _clean(self, text):
        raise NotImplementedError()

class ESVAPIAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.ESVAPI,
            translation=Translations.ESV
        )

        self.api_key = dotenv_values(
            load_first_config(App.Name.value) + "/config"
        ).get("ESV_API_KEY", None)

        if self.api_key is None:
            raise MissingAPIKey()

    def _fetch(self, ref):
        headers = {"Authorization": "Token %s" % self.api_key}
        # @@@ TODO Allow ESV API params to be configured by user
        params = {
            "q": ref,
            "include-passage-references": False,
            "include-footnotes": False,
            "include-headings": False,
            "include-short-copyright": False,
            "include-selahs": False
        }
        resp = requests.get(self.api, params=params, headers=headers).json()
        print(resp)
        return resp["passages"][0]

    def _clean(self, text):
        pdb.set_trace()
        return normalize("NFKD", text).encode("ascii", "ignore")
