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

from unittest import TestCase
from fastapi import HTTPException
from peewee import SqliteDatabase
from scripture_phaser.backend.user import (
    create_user,
    login,
    logout,
    change_password,
    UserCredentials,
    NewUserDetails,
)
from scripture_phaser.backend.models import User as UserTable, UserToken
from scripture_phaser.backend.exceptions import (
    InvalidUserToken,
)

in_memory_db = SqliteDatabase(":memory:")


class UserTests(TestCase):
    @classmethod
    def setUp(cls) -> None:
        in_memory_db.bind(
            [UserTable, UserToken], bind_refs=False, bind_backrefs=False
        )
        in_memory_db.connect()
        in_memory_db.create_tables([UserTable, UserToken])

    @classmethod
    def tearDown(cls) -> None:
        in_memory_db.drop_tables([UserTable, UserToken])
        in_memory_db.close()

    def test_login(self) -> None:
        name = "Bob Johnson"
        username = "bJohnson"
        password = "password"
        email = "bob@example.com"
        new_user_details = NewUserDetails(
            name=name, username=username, password=password, email=email
        )

        create_user(new_user_details)
        login(UserCredentials(username=username, password=password))

        with self.assertRaises(HTTPException):
            login(UserCredentials(username=username, password="password1"))

    def test_logout(self) -> None:
        name = "Sam Smith"
        username = "sSmith"
        password = "password"
        email = "sam@example.com"
        new_user_details = NewUserDetails(
            name=name, username=username, password=password, email=email
        )

        user = create_user(new_user_details)
        logout(user)

        with self.assertRaises(InvalidUserToken):
            logout(user)

    def test_change_password(self) -> None:
        name = "Indiana Jones"
        username = "iJones"
        password = "abadpassword"
        email = "indy@example.com"
        new_user_details = NewUserDetails(
            name=name, username=username, password=password, email=email
        )

        user = create_user(new_user_details)
        new_password = "abetterpassword"
        change_password(user, password, new_password)

        with self.assertRaises(HTTPException):
            login(UserCredentials(username=username, password=password))
