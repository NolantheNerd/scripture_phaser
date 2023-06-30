import webbrowser
from dotenv import dotenv_values
from scripture_phaser.enums import App
from scripture_phaser.enums import Translations
from scripture_phaser.agents import KJVAPIAgent
from scripture_phaser.agents import WEBAPIAgent
from scripture_phaser.agents import BBEAPIAgent
from scripture_phaser.agents import ESVAPIAgent
from scripture_phaser.agents import ESVBibleGatewayAgent
from scripture_phaser.agents import NIVBibleGatewayAgent
from scripture_phaser.agents import NKJVBibleGatewayAgent
from scripture_phaser.agents import NLTBibleGatewayAgent
from scripture_phaser.agents import NASBBibleGatewayAgent
from scripture_phaser.agents import NRSVBibleGatewayAgent
from xdg.BaseDirectory import load_first_config

class BaseTranslation:
    def __init__(self, name, source, agent):
        self.name=name
        self.source = source
        self.agent = agent

    def about(self):
        return self.name.value

    def visit_source(self):
        webbrowser.open(self.source)

class ESV(BaseTranslation):
    def __init__(self):
        self.api_key = dotenv_values(
            load_first_config(App.Name.value) + "/config"
        ).get("ESV_API_KEY", None)

        if self.api_key is not None:
            super().__init__(
                name=Translations.ESV,
                source="https://www.esv.org",
                agent=ESVAPIAgent(self.api_key)
            )
        else:
            super().__init__(
                name=Translations.ESV,
                source="https://www.esv.org",
                agent=ESVBibleGatewayAgent
            )

class KJV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.KJV,
            source="https://www.kingjamesbibleonline.org/",
            agent=KJVAPIAgent()
        )

class WEB(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.WEB,
            source="https://worldenglish.bible/",
            agent=WEBAPIAgent()
        )

class BBE(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.BBE,
            source="https://www.o-bible.com/bbe.html",
            agent=BBEAPIAgent()
        )

class NIV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.NIV,
            source="https://thenivbible.com",
            agent=NIVBibleGatewayAgent()
        )

class NKJV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.NKJV,
            source="https://www.thomasnelsonbibles.com/nkjv-bible/",
            agent=NKJVBibleGatewayAgent()
        )

class NLT(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.NLT,
            source="https://nlt.to/",
            agent=NLTBibleGatewayAgent()
        )

class NASB(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.NASB,
            source="https://www.lockman.org/new-american-standard-bible-nasb/",
            agent=NASBBibleGatewayAgent()
        )

class NRSV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.RSV,
            source="https://www.friendshippress.org/pages/about-the-nrsvue",
            agent=NRSVBibleGatewayAgent()
        )
