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
import sqlite3
from scripture_phaser.enums import App
from xdg.BaseDirectory import save_data_path

class Database:
    def __init__(self):
        self.path = save_data_path(App.Name.value) + "/attempt_db"
        if not os.path.isfile(self.path):
            self._create_db()
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()

    def _create_db(self):
        sql = f"""
        create table Attempts (
            ID int,
            Timestamp text,
            Mode text,
            Reference text,
            Score real,
            Attempt text,
            Diff text
        );
        """
        self.cur.execute(sql)
        self.cur.commit()

    def add_attempt(self, attempt):
        sql = f"insert into Attempts values {attempt._serialize()};"
        self.cur.execute(sql)
        self.cur.commit()

    def get_attempts(self, selector):
        sql = f"select {selector} from Attempts;"
        return self.cur.execute(sql)

    def reset(self):
        os.remove(self.path)
