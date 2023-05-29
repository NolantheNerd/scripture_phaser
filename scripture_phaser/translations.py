import webbrowser
from scripture_phaser.enums import Translations
from scripture_phaser.agents import ESVAPIAgent
from scripture_phaser.agents import BibleGatewayAgent

class BaseTranslation:
    def __init__(self, name, source, agent):
        self.name = name.name
        self.source = source
        self.agent = agent

    def about(self):
        print(self.name.value)

    def visit_source(self):
        webbrowser.open(self.source)

class ESV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name = Translations.ESV,
            source="https://esv.org",
            api="https://www.biblegateway.com/passage/?version=ESV"
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
