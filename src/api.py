# scripture_phaser helps you to memorize the Word of Truth.
# Copyright (C) 2023-2024 Nolan McMahon
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
import platform
import random
import subprocess
from sys import exit
from shutil import which
from pathlib import Path
from dotenv import dotenv_values
from xdg.BaseDirectory import save_cache_path
from xdg.BaseDirectory import save_config_path
from src.enums import App
from src.enums import AppDefaults
from src.stats import Stats
from src.models import Attempt
from src.passage import Passage
from src.enums import Translations
from src.exceptions import EditorNotFound
from src.exceptions import InvalidTranslation
from src.translations import ESV
from src.translations import NIV
from src.translations import KJV
from src.translations import WEB
from src.translations import NKJV
from src.translations import NLT
from src.translations import NASB
from src.translations import NRSV
from src.exceptions import InvalidReference


class API:
    def __init__(self):
        self.stats = Stats()
        self.config_path = Path(save_config_path(App.Name.value))
        self.cache_path = Path(save_cache_path(App.Name.value))
        self.config = self.load_config()
        self.is_windows = platform.system() == "Windows"

        if App.translation.name in self.config:
            self.translation = self.config[App.translation.name]
        else:
            self.translation = App.Defaults.translation.value
        if App.random_mode.name in self.config:
            self.mode = self.config[App.random_mode.name]
        if App.reference.name in self.config:
            self.passage = self.config[App.reference.name]

        if not Attempt.table_exists():
            Attempt.create_table()

    @staticmethod
    def load_config():
        config_path = Path(save_config_path(App.Name.value))
        config_file = config_path / "config"
        if not config_file.exists():
            with open(config_file, "w") as file:
                for default_key, default_value in vars(AppDefaults()).items():
                    file.write(f"{default_key}=\"{default_value}\"\n")

        config = dotenv_values(config_file)

        missing_keys = []
        for default_key in vars(AppDefaults()):
            if default_key not in config:
                missing_keys.append(default_key)
        if len(missing_keys) > 0:
            with open(config_file, "a") as file:
                for key in missing_keys:
                    file.write(f"{key}=\"{getattr(AppDefaults(), key)}\"\n")
                    config[key] = getattr(AppDefaults(), key)

        return config

    @staticmethod
    def save_config(config):
        config_path = Path(save_config_path(App.Name.value))
        config_file = config_path / "config"

        os.remove(config_file)

        with open(config_file, "w") as file:
            for key in config.keys():
                file.write(f"{key}=\"{config[key]}\"\n")

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
        self.save_config(self.config)

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
            self.save_config(self.config)

            if hasattr(self, "passage") and self.passage is not None:
                self.passage = self.passage.reference

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
        if reference.strip() == "" or reference == "None":
            self._passage = None
            self.config[App.reference.name] = "None"
        else:
            try:
                self._passage = Passage(reference, self.translation)
                self._passage.populate()
                self.config[App.reference.name] = self._passage.reference
            except InvalidReference as e:
                print(e.__str__())

        self.save_config(self.config)

    def view_passage(self):
        if self.passage is not None:
            return self.passage.show(with_ref=True)
        else:
            return ""

    def recitation(self):
        if self.mode:
            self.target = self.get_random_verse()
        else:
            self.target = self.passage

        try:
            editor = os.environ["EDITOR"]
        except KeyError:
            try:
                if which("gedit") is not None:
                    editor = "gedit"
                elif which("nano") is not None:
                    editor = "nano"
                elif which("nvim") is not None:
                    editor = "nvim"
                elif which("vim") is not None:
                    editor = "vim"
                elif which("notepad") is not None:
                    editor = "notepad"
                else:
                    raise EditorNotFound()
            except EditorNotFound:
                print("Text editor not found; set the 'EDITOR'" +
                  "environmental variable and try again")
                exit()

        if self.is_windows:
            windows_filename = f"{self.target.reference}".replace(":", ";")
            self.filename = self.cache_path / windows_filename
        else:
            self.filename = self.cache_path / f"{self.target.reference}"

        self.filename.touch(exist_ok=True)
        subprocess.run([editor, self.filename])

        if not self.filename.exists():
            text = ""
        else:
            with open(self.filename, "r") as file:
                text = file.readlines()
                text = "".join(text)

            # Vim Automatically Adds a Newline at the End of the File when
            # you save it. (Unless you set :nofixeol and set :nofixendofline -
            # in which case, this fix won't work - TODO Think about the case
            # where the correct recitation ends with a \n and the user has set
            # these options...)
            if (editor in ("vim", "nvim", "nano")) and len(text) > 0 and text[-1] == "\n":
                text = text[:-1]

            if self.filename.exists():
                os.remove(self.filename)

        attempt = Attempt.create(
            random_mode=self.mode,
            reference=self.target.reference,
        )
        score, diff = attempt.complete(text, self.passage)
        attempt.save()
        return score, diff

    @staticmethod
    def reset_db():
        if Attempt.table_exists():
            Attempt.drop_table()
        Attempt.create_table()
