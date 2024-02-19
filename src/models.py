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

import difflib
import datetime
from pathlib import Path
from peewee import Model
from peewee import TextField
from peewee import CharField
from peewee import FloatField
from peewee import BooleanField
from peewee import DateTimeField
from peewee import SqliteDatabase
from src.enums import App
from src.enums import TermColours as TC
from xdg.BaseDirectory import save_data_path

class Attempt(Model):
    datetime = DateTimeField(null=True)
    random_mode = BooleanField()
    reference = CharField()
    score = FloatField(null=True)
    attempt = TextField(null=True)
    diff = TextField(null=True)

    class Meta:
        database = SqliteDatabase(
            Path(save_data_path(App.Name.value)) / App.Database.value
                 )

    def complete(self, attempt, passage):
        self.attempt = attempt
        self.datetime = datetime.datetime.now()
        self._grade(passage)
        self.save()
        return self.score, self.diff

    def _grade(self, passage):
        ans = passage.show()
        if self.attempt == ans:
            self.score = 1
            self.diff = ""
        else:
            self.diff = ""
            n_correct_chars, n_incorrect_chars = 0, 0
            result = difflib.SequenceMatcher(a=self.attempt, b=ans).get_opcodes()
            for tag, i1, i2, j1, j2 in result:
                if tag == "replace":
                    n_incorrect_chars += max([(j2 - j1), (i2 - i1)])
                    segment = f"{TC.RED}{self.attempt[i1:i2]}{TC.GREEN}{ans[j1:j2]}{TC.WHITE}"
                    segment = segment.replace(" ", "_")
                    segment = segment.replace("\n", "\\n")
                    self.diff += segment
                elif tag == "delete":
                    n_incorrect_chars += i2 - i1
                    segment = f"{TC.RED}{self.attempt[i1:i2]}{TC.WHITE}"
                    segment = segment.replace(" ", "_")
                    segment = segment.replace("\n", "\\n")
                    self.diff += segment
                elif tag == "insert":
                    n_incorrect_chars += j2 - j1
                    segment = f"{TC.GREEN}{ans[j1:j2]}{TC.WHITE}"
                    segment = segment.replace(" ", "_")
                    segment = segment.replace("\n", "\\n")
                    self.diff += segment
                elif tag == "equal":
                    n_correct_chars += i2 - i1
                    self.diff += f"{TC.CYAN}{self.attempt[i1:i2]}{TC.WHITE}"

            self.score = n_correct_chars / (n_correct_chars + n_incorrect_chars)
