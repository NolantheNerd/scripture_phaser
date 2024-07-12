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
import datetime
import random as rd
from difflib import SequenceMatcher
from src.enums import CONFIG_DIR
from src.stats import Stats
from src.models import Attempt
from src.enums import Translations
from src.reference import Reference
from typing import List, Dict, Union
from src.exceptions import NoReferences
from src.exceptions import InvalidTranslation


class SPDefault:
    translation: str = "NIV"
    complete_recitation: str = "False"
    one_verse_recitation: str = "False"
    include_verse_numbers: str = "False"
    fast_recitations: str = "False"
    reference: str = ""


class API:
    def __init__(self) -> None:
        self.stats = Stats()
        config = self.load_config()

        self.complete_recitation = config.get("complete_recitation", SPDefault.complete_recitation) == "True"
        self.one_verse_recitation = config.get("one_verse_recitation", SPDefault.one_verse_recitation) == "True"
        self.include_verse_numbers = config.get("include_verse_numbers", SPDefault.include_verse_numbers) == "True"
        self.fast_recitations = config.get("fast_recitaitons", SPDefault.fast_recitations) == "True"

        self.translation = config.get("translation", SPDefault.translation)

        self.references = []
        for ref in config["reference"]:
            self.add_reference(ref)

        if not Attempt.table_exists():
            Attempt.create_table()

    def load_config(self) -> Dict[str, Union[str, List[str]]]:
        config_file = CONFIG_DIR / "config"
        if not config_file.exists():
            with open(config_file, "w") as file:
                for default_key, default_value in vars(SPDefault).items():
                    file.write(f"{default_key}={default_value}\n")

        with open(config_file, "r") as file:
            entries = file.readlines()
        config = {}
        for entry in entries:
            key, value = entry.split("=")
            key, value = key.strip(), value.strip()

            if key == "reference":
                config[key] = config.get(key, []) + [value]
            else:
                config[key] = value

        missing_keys = []
        for default_key in vars(SPDefault):
            if default_key not in config:
                missing_keys.append(default_key)
        if len(missing_keys) > 0:
            with open(config_file, "a") as file:
                for key in missing_keys:
                    file.write(f"={getattr(SPDefault, key)}\n")
                    config[key] = getattr(SPDefault, key)

        return config

    def save_config(self) -> None:
        config = {
            "translation": self.translation,
            "one_verse_recitation": self.one_verse_recitation,
            "complete_recitation": self.complete_recitation,
            "reference": [ref.ref_str for ref in self.references],
            "include_verse_numbers": self.include_verse_numbers,
            "fast_recitations": self.fast_recitations
        }

        config_file = CONFIG_DIR / "config"
        os.remove(config_file)

        with open(config_file, "w") as file:
            for key in config.keys():
                if key == "reference":
                    for ref in config["reference"]:
                        file.write(f"reference={ref}\n")
                else:
                    file.write(f"{key}={config[key]}\n")

    def toggle_one_verse_recitation(self) -> None:
        self.one_verse_recitation = not self.one_verse_recitation
        self.save_config()

    def toggle_complete_recitation(self) -> None:
        self.complete_recitation = not self.complete_recitation
        self.save_config()

    def toggle_fast_recitations(self) -> None:
        self.fast_recitations = not self.fast_recitations
        self.save_config()

    def toggle_include_verse_numbers(self) -> None:
        self.include_verse_numbers = not self.include_verse_numbers
        self.save_config()

    def view_translation(self) -> List[str]:
        return Translations

    def set_translation(self, translation) -> None:
        if translation not in Translations:
            raise InvalidTranslation(translation)
        else:
            self.translation = translation
            self.save_config()

    def add_reference(self, ref: Union[str, Reference]) -> None:
        recursed = False

        if not isinstance(ref, Reference):
            new_reference = Reference(self.translation, ref)
        else:
            new_reference = ref

        if new_reference.empty:
            return

        for i, old_reference in enumerate(self.references):
            # Start ID is Inside Passage
            if new_reference.start_id >= old_reference.start_id and new_reference.start_id <= old_reference.end_id:
                # New Reference Extends Past Existing Passage
                if new_reference.end_id > old_reference.end_id:
                    recursed = True
                    start_id = old_reference.start_id
                    end_id = new_reference.end_id
                    self.delete_reference(i)
                    self.add_reference(Reference(self.translation, id=start_id, end_id=end_id))
            # End ID is Inside Passage
            elif new_reference.end_id >= old_reference.start_id and new_reference.end_id <= old_reference.end_id:
                # New Reference Extends Before Existing Passage
                if new_reference.start_id < old_reference.start_id:
                    recursed = True
                    start_id = new_reference.start_id
                    end_id = old_reference.end_id
                    self.delete_reference(i)
                    self.add_reference(Reference(self.translation, id=start_id, end_id=end_id))

        if not recursed:
            self.references.append(new_reference)
            self.references.sort(key=lambda reference: reference.start_id)
            self.save_config()

    def list_references(self) -> List[str]:
        if len(self.references) == 0:
           raise NoReferences()

        return [reference.ref_str for reference in self.references]

    def view_reference(self, index: int) -> str:
        if len(self.references) == 0:
           raise NoReferences()

        return self.references[index].view(include_verse_numbers=False, include_ref=True)

    def delete_reference(self, index: int) -> None:
        del self.references[index]

    def get_reference(self) -> Reference:
        if len(self.references) == 0:
            raise NoReferences()

        chosen_reference = rd.choice(self.references)
        if not self.complete_recitation:
            if self.one_verse_recitation:
                chosen_id = rd.randrange(chosen_reference.start_id, chosen_reference.end_id + 1)
                return Reference(self.translation, id=chosen_id)
            else:
                chosen_start_id = rd.randrange(chosen_reference.start_id, chosen_reference.end_id + 1)
                chosen_end_id = rd.randrange(chosen_start_id, chosen_reference.end_id + 1)
                return Reference(self.translation, id=chosen_start_id, end_id=chosen_end_id)
        else:
            return chosen_reference

    def recite(self, reference: Reference, text: str) -> Attempt:
        if self.fast_recitations:
            ans = reference.view_first_letter(self.include_verse_numbers)

            if text == ans:
                score = 1
            else:
                n_correct = sum([1 for i in range(len(ans)) if text[i] == ans[i]])
                score = n_correct / len(ans)
        else:
            ans = reference.view(self.include_verse_numbers, include_ref=False)

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

        return Attempt.create(
            reference=reference.ref_str,
            score=score,
            attempt=text,
            datetime=datetime.datetime.now()
        )
