# scripture_phaser helps you to memorize the Bible.
# Copyright (C) 2023-2025 Nolan McMahon
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

import peewee as pw


class ScripturePhaser(pw.Model):
    class Meta:
        database = pw.SqliteDatabase("scripture_phaser.sqlite")


class User(ScripturePhaser):
    name = pw.TextField()
    username = pw.TextField(unique=True)
    password_hash = pw.BlobField()
    salt = pw.BlobField()
    email = pw.TextField(unique=True)


class UserToken(ScripturePhaser):
    user = pw.ForeignKeyField(User, on_delete="CASCADE")
    token = pw.TextField()
    expiry = pw.DateTimeField()


class Reference(ScripturePhaser):
    user = pw.ForeignKeyField(User, on_delete="CASCADE")
    ref = pw.TextField()
    translation = pw.TextField()


class Recitation(ScripturePhaser):
    datetime = pw.DateTimeField()
    recitation_type = pw.TextField()
    score = pw.FloatField()
    recitation = pw.TextField()
    user = pw.ForeignKeyField(User, null=True, on_delete="CASCADE")
    reference = pw.ForeignKeyField(Reference)


if __name__ == "__main__":
    User.drop_table()
    UserToken.drop_table()
    Reference.drop_table()
    Recitation.drop_table()
    User.create_table()
    UserToken.create_table()
    Reference.create_table()
    Recitation.create_table()
