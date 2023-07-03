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

import random
from dotenv import dotenv_values
from scripture_phaser.passage import Passage
from scripture_phaser.attempt import Attempt
from scripture_phaser.database import Database
from scripture_phaser.enums import Translations
from xdb.BaseDirectory import load_first_config
from scripture_phaser.exceptions import InvalidTranslation

class API:
    def __init__(self):
        self.config = dotenv_values(
            load_first_config(App.Name.value) + "/config"
        )
        self._translation = self.config["TRANSLATION"]
        self._random_mode = False
        self.db = Database()
        self._passage = None
        self.attempt = None

    @property
    def random_mode(self):
        return self._random_mode

    @mode.setter
    def mode(self, random_mode):
        self._random_mode = random_mode

    def list_translations(self):
        return [translation.name for translation in Translations]

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, translation):
        if translation not in self.list_translations:
            raise InvalidTranslation(translation)
        else:
            self._translation = translation

    @property
    def passage(self):
        if self.random_mode:
            verse = random.choices(self._passage.verses)
            random_passage = Passage(verse.reference, self.translation)
            random_passage.populate([verse.text])
            return random_passage
        else:
            return self._passage

    @passages.setter
    def passage(self, passage):
        self.passages = Passage(reference, self.translation)

    def new_attempt(self):
        ident = len(self.db) # LOL Fix this
        passage = self.passage
        self.attempt = attempt(passage, self.random_mode, ident)
        return self.attempt.reference

    def show_attempt(self):
        return self.attempt.show()

    def complete_attempt(self, text):
        self.attempt.complete(text)
        self.db.add_attempt(self.attempt)
        self.attempt = None

    def get_stats(self):
        pass

    def reset_db(self):
        self.db.reset()
