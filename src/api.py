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
import random
import datetime
from difflib import SequenceMatcher
from src.enums import CACHE_DIR
from src.enums import CONFIG_DIR
from src.enums import App
from src.enums import AppDefaults
from src.stats import Stats
from src.models import Attempt
from src.passage import Passage
from src.enums import Translations
from src.reference import Reference
from src.exceptions import EditorNotFound
from src.exceptions import InvalidReference
from src.exceptions import InvalidTranslation


class API:
    def __init__(self):
        self.stats = Stats()
        self.config_path = CONFIG_DIR / App.Name.value
        self.cache_path = CACHE_DIR / App.Name.value

        config = self.load_config()
        self.translation = config.get(App.translation.name, AppDefaults().translation)
        self.random_single_verse = config.get(App.random_single_verse.name, AppDefaults().random_single_verse) == "True"
        self.reference = Reference(config.get(App.reference.name, AppDefaults().reference))
        self.require_passage_numbers = config.get(App.require_passage_numbers.name, AppDefaults().require_passage_numbers) == "True"
        self.fast_recitations = config.get(App.fast_recitations.name, AppDefaults().fast_recitations) == "True"
        if not self.reference.empty:
            self.set_passage(self.reference.ref_str)
        else:
            self.passage = None

        if not Attempt.table_exists():
            Attempt.create_table()

    def load_config(self):
        config_file = self.config_path / "config"
        if not config_file.exists():
            with open(config_file, "w") as file:
                for default_key, default_value in vars(AppDefaults()).items():
                    file.write(f"{default_key}={default_value}\n")

        with open(config_file, "r") as file:
            entries = file.readlines()
        config = {}
        for entry in entries:
            key, value = entry.split("=")
            key, value = key.strip(), value.strip()
            config[key] = value

        missing_keys = []
        for default_key in vars(AppDefaults()):
            if default_key not in config:
                missing_keys.append(default_key)
        if len(missing_keys) > 0:
            with open(config_file, "a") as file:
                for key in missing_keys:
                    file.write(f"{key}={getattr(AppDefaults(), key)}\n")
                    config[key] = getattr(AppDefaults(), key)

        return config

    def save_config(self):
        config = {
            "translation": self.translation,
            "random_single_verse": self.random_single_verse,
            "reference": self.reference.ref_str,
            "require_passage_numbers": self.require_passage_numbers,
            "fast_recitations": self.fast_recitations
        }

        config_file = self.config_path / "config"

        os.remove(config_file)

        with open(config_file, "w") as file:
            for key in config.keys():
                file.write(f"{key}={config[key]}\n")

    def new_reference(self, reference):
        return Reference(reference)

    def set_random_single_verse(self):
        self.random_single_verse = not self.random_single_verse
        self.save_config()

    def set_fast_recitations(self):
        self.fast_recitations = not self.fast_recitations
        self.save_config()

    def set_require_passage_numbers(self):
        self.require_passage_numbers = not self.require_passage_numbers
        self.set_passage(self.reference.ref_str)
        self.save_config()

    def view_translation(self):
        return Translations

    def set_translation(self, translation):
        if translation not in Translations:
            raise InvalidTranslation(translation)
        else:
            self.translation = translation
            self.save_config()

            if not self.reference.empty:
                self.set_passage(self.reference.ref_str)

    def get_random_verse(self):
        return random.choice(self.passage.verses).reference

    def set_passage(self, reference):
        self.reference = Reference(reference)
        if self.reference.empty:
            self.passage = None
        else:
            try:
                self.passage = Passage(self.reference, self.translation)
                self.passage.populate(require_passage_numbers=self.require_passage_numbers)
            except InvalidReference as e:
                print(e.__str__())

        self.save_config()

    def view_passage(self):
        if self.passage is not None:
            return self.passage.show(with_ref=True)
        else:
            return ""

    def new_recitation(self):
        if self.random_single_verse:
            return self.get_random_verse()
        else:
            return self.passage.reference

    def finish_recitation(self, reference, text):
        if self.fast_recitations:
            ans = self.get_fast_recitation_ans(reference)

            if text == ans:
                score = 1
            else:
                n_correct = sum([1 for i in range(len(ans)) if text[i] == ans[i]])
                score = n_correct / len(ans)

                passage_words = self.passage.show().split()
        else:
            ans = self.get_recitation_ans(reference)

            if text == ans:
                score = 1
            else:
                n_correct_chars, n_incorrect_chars = 0, 0
                result = SequenceMatcher(a=text, b=ans).get_opcodes()
                for tag, i1, i2, j1, j2 in result:
                    if tag == "replace":
                        n_incorrect_chars += max([(j2 - j1), (i2 - i1)])
                    elif tag == "delete":
                        n_incorrect_chars += i2 - i1
                    elif tag == "insert":
                        n_incorrect_chars += j2 - j1
                    elif tag == "equal":
                        n_correct_chars += i2 - i1

                score = n_correct_chars / (n_correct_chars + n_incorrect_chars)

        attempt = Attempt.create(
            random_single_verse=self.random_single_verse,
            reference=reference.ref_str,
            score=score,
            attempt=text,
            datetime=datetime.datetime.now()
        )

        return score

    def get_fast_recitation_ans(self, reference):
        if self.random_single_verse:
            passage = Passage(reference, self.translation)
            passage.populate([v.text for v in self.passage.verses if v.reference.ref_str == reference.ref_str])
        else:
            passage = self.passage

        raw_text = passage.show()
        if self.require_passage_numbers:
            raw_text = raw_text.replace("[", "")
        return [word[0] for word in raw_text.split()]

    def get_recitation_ans(self, reference):
        if self.random_single_verse:
            passage = Passage(reference, self.translation)
            passage.populate([v.text for v in self.passage.verses if v.reference.ref_str == reference.ref_str])
            ans = passage.show()
        else:
            ans = self.passage.show()
