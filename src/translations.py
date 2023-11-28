# helps you to memorize the Word of Truth.
# Copyright (C) 2023 Nolan McMahon
#
# This file is part of.
#
# is licensed under the terms of the BSD 3-Clause License
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

import webbrowser
from dotenv import dotenv_values
from src.enums import App
from src.enums import Translations
from src.agents import KJVAPIAgent
from src.agents import WEBAPIAgent
from src.agents import BBEAPIAgent
from src.agents import ESVAPIAgent
from src.agents import ESVBibleGatewayAgent
from src.agents import NIVBibleGatewayAgent
from src.agents import NKJVBibleGatewayAgent
from src.agents import NLTBibleGatewayAgent
from src.agents import NASBBibleGatewayAgent
from src.agents import NRSVBibleGatewayAgent
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
    def __init__(self, api_key=None):
        self.api_key = api_key

        if self.api_key is not None:
            super().__init__(
                name=Translations.ESV.value,
                source="https://www.esv.org",
                agent=ESVAPIAgent(self.api_key)
            )
        else:
            super().__init__(
                name=Translations.ESV.value,
                source="https://www.esv.org",
                agent=ESVBibleGatewayAgent()
            )

class KJV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.KJV.value,
            source="https://www.kingjamesbibleonline.org/",
            agent=KJVAPIAgent()
        )

class WEB(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.WEB.value,
            source="https://worldenglish.bible/",
            agent=WEBAPIAgent()
        )

class BBE(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.BBE.value,
            source="https://www.o-bible.com/bbe.html",
            agent=BBEAPIAgent()
        )

class NIV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.NIV.value,
            source="https://thenivbible.com",
            agent=NIVBibleGatewayAgent()
        )

class NKJV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.NKJV.value,
            source="https://www.thomasnelsonbibles.com/nkjv-bible/",
            agent=NKJVBibleGatewayAgent()
        )

class NLT(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.NLT.value,
            source="https://nlt.to/",
            agent=NLTBibleGatewayAgent()
        )

class NASB(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.NASB.value,
            source="https://www.lockman.org/new-american-standard-bible-nasb/",
            agent=NASBBibleGatewayAgent()
        )

class NRSV(BaseTranslation):
    def __init__(self):
        super().__init__(
            name=Translations.RSV.value,
            source="https://www.friendshippress.org/pages/about-the-nrsvue",
            agent=NRSVBibleGatewayAgent()
        )