import webbrowser
from dotenv import dotenv_values
from scripture_phaser.enums import App
from scripture_phaser.enums import Translations
from scripture_phaser.agents import ESVAPIAgent
from scripture_phaser.agents import ESVBibleGatewayAgent
from xdg.BaseDirectory import load_first_config

class BaseTranslation:
    def __init__(self, name, source, agent):
        self.name = name
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

        if self.api_key is None:
            super().__init__(
                name=Translations.ESV,
                source="https://www.esv.org",
                agent=ESVAPIAgent
            )
        else:
            super().__init__(
                name=Translations.ESV,
                source="https://www.esv.org",
                agent=ESVBibleGatewayAgent
            )

class NIV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name = Translations.NIV,
            source="https://thenivbible.com",
            api="https://www.biblegateway.com/passage/?version=NIV"
        )

class KJV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name = Translations.KJV,
            source="https://www.kingjamesbibleonline.org/",
            api="https://www.biblegateway.com/passage/?version=KJV"
        )

class NKJV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name = Translations.NKJV,
            source="https://www.thomasnelsonbibles.com/nkjv-bible/",
            api="https://www.biblegateway.com/passage/?version=NKJV"
        )

class NLT(BaseTranslation):
    def __init__(self):
        super().__init__(
            name = Translations.NLT,
            source="https://nlt.to/",
            api="https://www.biblegateway.com/passage/?version=NLT"
        )

class NASB(BaseTranslation):
    def __init__(self):
        super().__init__(
            name = Translations.NASB,
            source="https://www.lockman.org/new-american-standard-bible-nasb/",
            api="https://www.biblegateway.com/passage/?version=NASB"
        )

class RSV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name = Translations.RSV,
            source="https://rsv.friendshippress.org/",
            api="https://www.biblegateway.com/passage/?version=RSV"
        )

class NCV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name = Translations.NCV,
            source="https://www.thomasnelsonbibles.com/ncv/",
            api="https://www.biblegateway.com/passage/?version=NCV"
        )

class MSG(BaseTranslation):
    def __init__(self):
        super().__init__(
            name = Translations.MSG,
            source="https://messagebible.com/",
            api="https://www.biblegateway.com/passage/?version=MSG"
        )
