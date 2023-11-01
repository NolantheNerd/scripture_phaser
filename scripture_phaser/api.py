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
from sys import exit
from shutil import which
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
from scripture_phaser.exceptions import EditorNotFound
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
    def __init__(self):
        self.stats = Stats()
        self.load_config()

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

        if App.translation.name in self.config:
            self.translation = self.config[App.translation.name]
        else:
            self.translation = App.Defaults.translation.value
        if App.random_mode.name in self.config:
            self.mode = self.config[App.random_mode.name]
        if App.reference.name in self.config:
            self.passage = self.config[App.reference.name]

    def save_config(self):
        config_path = Path(save_config_path(App.Name.value))
        config_path /= "config"

        os.remove(config_path)

        with open(config_path, "w") as config_file:
            for key in self.config.keys():
                config_file.write(f"{key}=\"{self.config[key]}\"\n")

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, random_mode):
        if random_mode == "False" or not random_mode:
            self._mode = False
        else:
            self._mode = True
        self.config[App.random_mode.name] = self._mode

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
            self.config[App.translation.name] = translation

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
        if reference == "" or reference == "None":
            self._passage = None
        else:
            self._passage = Passage(reference, self.translation)
            self._passage.populate()
            self.config[App.reference.name] = self._passage.reference

    def new_recitation(self):
        if self.mode:
            self.target = self.get_random_verse()
        else:
            self.target = self.passage
        return self.target

    def launch_recitation(self):
        try:
            editor = os.environ["EDITOR"]
        except KeyError:
            try:
                # Try Gedit
                if which("gedit") is not None:
                    editor = "gedit"
                # Try Nano
                elif which("nano") is not None:
                    editor = "nano"
                # Try Neovim
                elif which("nvim") is not None:
                    editor = "nvim"
                # Try Vim
                elif which("vim") is not None:
                    editor = "vim"
                else:
                    raise EditorNotFound()
            except EditorNotFound:
                print("Text editor not found; set the 'EDITOR' environmental variable and try again")
                exit()

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
