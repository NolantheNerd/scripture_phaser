# scripture_phaser helps you to memorize the Word of Truth.
# Copyright (C) 2023 Nolan McMahon
#
# This file is part of scripture_phaser.
#
# scripture_phaser is licensed under the terms of the BSD 3-Clause License
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

import os
import random
import subprocess
from pathlib import Path
from dotenv import dotenv_values
from xdg.BaseDirectory import xdg_config_home
from xdg.BaseDirectory import save_config_path
from xdg.BaseDirectory import load_first_config
from scripture_phaser.enums import App
from scripture_phaser.stats import Stats
from scripture_phaser.models import Attempt
from scripture_phaser.passage import Passage
from scripture_phaser.enums import Translations
from scripture_phaser.exceptions import InvalidTranslation
from scripture_phaser.translations import ESV
from scripture_phaser.translations import NIV
from scripture_phaser.translations import KJV
from scripture_phaser.translations import WEB
from scripture_phaser.translations import BBE
from scripture_phaser.translations import NKJV
from scripture_phaser.translations import NLT
from scripture_phaser.translations import NASB
from scripture_phaser.translations import NRSV

class API:
    def __init__(
        self,
        translation=App.Defaults.value[App.Translation.name].value,
        mode=App.Defaults.value[App.Random_Mode.name].value,
        passage=None
    ):
        self._translation = globals()[translation]()
        self._mode = mode
        self._passage = passage
        self.stats = Stats()

    def load_config(self):
        config_path = Path(save_config_path(App.Name.value))
        config_path /= "config"
        if not config_path.exists():
            with open(config_path, "w") as config_file:
                for default in App.Defaults.value:
                    config_file.write(f"{default.name}=\"{default.value}\"\n")

        self.config = dotenv_values(config_path)

        missing_keys = []
        for default in App.Defaults.value:
            key = default.name
            if key not in self.config:
                missing_keys.append(key)
        if len(missing_keys) > 0:
            with open(config_path, "a") as config_file:
                for key in missing_keys:
                    config_file.write(f"{key}=\"{App.Defaults.value[key].value}\"\n")
                    self.config[key] = App.Defaults.value[key].value

        if App.Translation.name in self.config:
            self.translation = self.config[App.Translation.name]
        if App.Random_Mode.name in self.config:
            self.mode = self.config[App.Random_Mode.name]
        if App.Reference.name in self.config:
            self.passage = self.config[App.Reference.name]

    def save_config(self):
        config_path = Path(save_config_path(App.Name.value))
        config_path /= "config"

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, random_mode):
        self._mode = random_mode

    def list_translations(self):
        return [translation.name for translation in Translations]

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, translation):
        if translation not in self.list_translations():
            raise InvalidTranslation(translation)
        else:
            self._translation = globals()[translation]()

    def get_random_verse(self):
        verse = random.choice(self.passage.verses)
        verse_passage = Passage(verse.reference, self.translation)
        verse_passage.populate([verse.text])
        return verse_passage

    @property
    def passage(self):
        return self._passage

    @passage.setter
    def passage(self, reference):
        self._passage = Passage(reference, self.translation)
        self._passage.populate()

    def new_recitation(self):
        if self.mode:
            self.target = self.get_random_verse()
        else:
            self.target = self.passage
        return self.target

    def launch_recitation(self):
        # @@@ TODO: Check that EDITOR is set else try other common programs?
        editor = os.environ["EDITOR"]
        subprocess.run([editor, f"{self.target.reference}"])

    def preview_recitation(self, with_verse=False, with_ref=True):
        return self.target.show(with_verse=with_verse, with_ref=with_ref)

    def complete_recitation(self, text):
        attempt = Attempt(
            random_mode=self.random_mode,
            reference=self.target.reference,
        )
        score, diff = attempt.complete(text)
        attempt.save()
        return score, diff
