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
from typing import List, Dict, Any
from difflib import SequenceMatcher
from src.enums import CACHE_DIR
from src.enums import CONFIG_DIR
from src.enums import AppDefaults
from src.stats import Stats
from src.models import Attempt
from src.passage import Passage
from src.enums import Translations
from src.reference import Reference
from src.exceptions import InvalidReference
from src.exceptions import InvalidTranslation


class API:
    def __init__(self) -> None:
        self.stats = Stats()
        self.config_path = CONFIG_DIR / "scripture_phaser"
        self.cache_path = CACHE_DIR / "scripture_phaser"

        config = self.load_config()

        # Single, Boolean
        # Get: api.{property}; Set: api.toggle_{property}()
        self.random_single_verse = config.get("random_single_verse", AppDefaults.random_single_verse) == "True"
        self.require_passage_numbers = config.get("require_passage_numbers", AppDefaults.require_passage_numbers) == "True"
        self.fast_recitations = config.get("fast_recitaitons", AppDefaults.fast_recitations) == "True"

        # Single, Finite Acceptable Value
        # Get: api.{property}; Set: api.set_{property}(); View: api.view_{property}()
        self.translation = config.get("translation", AppDefaults.translation)

        # Multiple, Infinite Acceptable Values
        # Add: api.add_{property}(); Remove: api.remove_{property}();
        # Select: api.select_{property}(); DeSelect: api.deselect_{property}();
        # View: api.view_{property}()
        self.reference = Reference(config.get("reference", AppDefaults.reference))
        self.passages = []
        if not self.reference.empty:
            self.add_passage(self.reference)

        if not Attempt.table_exists():
            Attempt.create_table()

    def load_config(self) -> Dict[str, Any]:
        config_file = self.config_path / "config"
        if not config_file.exists():
            with open(config_file, "w") as file:
                for default_key, default_value in vars(AppDefaults).items():
                    file.write(f"{default_key}={default_value}\n")

        with open(config_file, "r") as file:
            entries = file.readlines()
        config = {}
        for entry in entries:
            key, value = entry.split("=")
            key, value = key.strip(), value.strip()
            config[key] = value

        missing_keys = []
        for default_key in vars(AppDefaults):
            if default_key not in config:
                missing_keys.append(default_key)
        if len(missing_keys) > 0:
            with open(config_file, "a") as file:
                for key in missing_keys:
                    file.write(f"{key}={getattr(AppDefaults, key)}\n")
                    config[key] = getattr(AppDefaults, key)

        return config

    def save_config(self) -> None:
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

    def toggle_random_single_verse(self) -> None:
        self.random_single_verse = not self.random_single_verse
        self.save_config()

    def toggle_fast_recitations(self) -> None:
        self.fast_recitations = not self.fast_recitations
        self.save_config()

    def toggle_require_passage_numbers(self) -> None:
        self.require_passage_numbers = not self.require_passage_numbers
        self.set_passage(self.reference)
        self.save_config()

    def view_translation(self) -> List[str]:
        return Translations

    def set_translation(self, translation) -> None:
        if translation not in Translations:
            raise InvalidTranslation(translation)
        else:
            self.translation = translation
            self.save_config()

            if not self.reference.empty:
                self.set_passage(self.reference)

    def get_random_verse(self) -> Reference:
        return Reference(id=random.randrange(self.passage.reference.start_id, self.passage.reference.end_id + 1))

    def add_passage(self, reference: Reference) -> None:
        for i, passage in enumerate(self.passages):
            # Start ID is Inside Passage
            if reference.start_id >= passage.reference.start_id and reference.start_id <= passage.reference.end_id:
                # New Reference Extends Past Existing Passage
                if reference.end_id > passage.reference.end_id:
                    start_id = passage.reference.start_id
                    end_id = reference.end_id
                    self.delete_passage(i)
                    self.add_passage(Reference(id=start_id, end_id=end_id))
            # End ID is Inside Passage
            elif reference.end_id >= passage.reference.start_id and reference.end_id <= passage.reference.end_id:
                # New Reference Extends Before Existing Passage
                if reference.start_id < passage.reference.start_id:
                    start_id = reference.start_id
                    end_id = passage.reference.end_id
                    self.delete_passage(i)
                    self.add_passage(Reference(id=start_id, end_id=end_id))

        self.passages.append(Passage(reference, self.translation))
        self.passages.sort(key=lambda passage: passage.start_id, reverse=True)

    def list_passages(self) -> List[Passage]:
        return self.passages

    def delete_passage(self, index: int) -> None:
        del self.passages[index]

    def set_passage(self, reference: Reference) -> None:
        self.reference = reference
        if self.reference.empty:
            self.passage = None
        else:
            try:
                self.passage = Passage(self.reference, self.translation)
                self.passage.populate()
            except InvalidReference as e:
                print(e.__str__())

        self.save_config()

    def view_passage(self) -> str:
        if self.passage is not None:
            return self.passage.show(with_ref=True)
        else:
            return ""

    def new_recitation(self) -> Reference:
        if self.random_single_verse:
            return self.get_random_verse()
        else:
            return self.passage.reference

    def finish_recitation(self, reference: Reference, text: str) -> float:
        if self.fast_recitations:
            ans = self.get_fast_recitation_ans(reference)

            if text == ans:
                score = 1
            else:
                n_correct = sum([1 for i in range(len(ans)) if text[i] == ans[i]])
                score = n_correct / len(ans)
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

        Attempt.create(
            random_single_verse=self.random_single_verse,
            reference=reference.ref_str,
            score=score,
            attempt=text,
            datetime=datetime.datetime.now()
        )

        return score

    def get_fast_recitation_ans(self, reference: Reference) -> List[str]:
        if self.random_single_verse:
            passage = Passage(reference, self.translation)
            passage.populate()
        else:
            passage = self.passage

        raw_text = passage.show()
        text = "".join([char for char in raw_text if char.isalnum() or char.isspace()])
        return [word[0] for word in text.split()]

    def get_recitation_ans(self, reference: Reference) -> str:
        if self.random_single_verse:
            passage = Passage(reference, self.translation)
            passage.populate()
            return passage.show()
        else:
            return self.passage.show()
