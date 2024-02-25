# scripture_phaser helps you to memorize the Bible.
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
from src.exceptions import InvalidReference
from src.exceptions import InvalidTranslation


class API:
    def __init__(self):
        self.stats = Stats()
        self.config_path = Path(save_config_path(App.Name.value))
        self.cache_path = Path(save_cache_path(App.Name.value))
        self.is_windows = platform.system() == "Windows"

        config = self.load_config()
        self.translation = config.get(App.translation.name, AppDefaults().translation)
        self.random_mode = config.get(App.random_mode.name, AppDefaults().random_mode)
        self.passage = config.get(App.reference.name, AppDefaults().reference)

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

    def save_config(self):
        config = {
            "translation": self.translation,
            "random_mode": self.random_mode,
            "reference": self.passage.reference
        }

        config_path = Path(save_config_path(App.Name.value))
        config_file = config_path / "config"

        os.remove(config_file)

        with open(config_file, "w") as file:
            for key in config.keys():
                file.write(f"{key}=\"{config[key]}\"\n")

    def toggle_random_mode(self):
        self.random_mode = not self.random_mode
        self.save_config()

    def list_translations(self):
        return Translations.keys()

    def set_translation(self, translation):
        if translation not in Translations:
            raise InvalidTranslation(translation)
        else:
            self.translation = translation
            self.save_config()

            if self.passage != "None":
                self.passage = self.passage.reference

    def get_random_verse(self):
        verse = random.choice(self.passage.verses)
        verse_passage = Passage(verse.reference, self.translation)
        verse_passage.populate([verse.text])
        return verse_passage

    def set_passage(self, reference):
        if reference.strip() == "" or reference == "None":
            self.passage = None
        else:
            try:
                self.passage = Passage(reference, self.translation)
                self.passage.populate()
            except InvalidReference as e:
                print(e.__str__())

        self.save_config()

    def view_passage(self):
        if self.passage is not None:
            return self.passage.show(with_ref=True)
        else:
            return ""

    def recitation(self):
        if self.random_mode:
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

            # Editors Sometimes add \n at the end of a file, if one doesn't
            # already exist @@@ TODO (Nolan): Think about the case where the
            # correct recitation ends with a \n and the user has set these
            # options...
            if len(text) > 0 and text[-1] == "\n":
                text = text[:-1]

            if self.filename.exists():
                os.remove(self.filename)

        attempt = Attempt.create(
            random_mode=self.random_mode,
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
