import requests
from enums import Agents
from enums import Translations

class BaseAgent:
    def __init__(self, agent, translation):
        self.translation = translation.name
        self.name = agent.name
        self.api = agent.value

        if agent is Agents.BibleGateway:
            self.api += f"version={self.translation}&"

    def fetch(self, ref):
        raise NotImplementedError("Child agent must implement fetch()")

    def clean(self, text):
        raise NotImplementedError("Child agent must implement clean()")

class BibleGatewayAgent(BaseAgent):
    def __init__(self, translation):
        super().__init__(
            agent=Agents.BibleGateway,
            translation=translation
        )

    def fetch(self, ref):
        raise NotImplementedError()

    def clean(self, text):
        raise NotImplementedError()

class ESVAPIAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent=Agents.ESVAPI,
            translation=Translations.ESV
        )

    def fetch(self, ref):
        headers = {"Authorization": "Token %s" % API_KEY}
        params = {
            "q": ref,
            "include-passage-references": False,
            "include-footnotes": False,
            "include-headings": False,
            "include-short-copyright": False
        }
        resp = requests.get(self.api, params=params, headers=headers).json()
        return resp["passages"][0]

    def clean(self, text):
        raise NotImplementedError()
