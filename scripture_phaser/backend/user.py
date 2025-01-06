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

import uuid
import datetime
from os import urandom
from hashlib import pbkdf2_hmac
from scripture_phaser.backend.translations import Translations
from scripture_phaser.backend.models import User, UserToken
from scripture_phaser.backend.exceptions import (
    UsernameAlreadyTaken,
    EmailAlreadyTaken,
    InvalidUserCredentials,
    InvalidUserToken,
    InvalidTranslation,
)

N_ITERATIONS = 100000
HASH_ALGORITHM = "PBKDF2"


def validate_token(user_token: str) -> None:
    token = UserToken.get_or_none(UserToken.token == user_token)
    if token is None:
        raise InvalidUserToken()

    if token.expiry < datetime.datetime.now():
        token.delete_instance()
        raise InvalidUserToken()


def create(username: str, password: str, email: str) -> UserToken:
    username_already_taken = User.get_or_none(User.username == username) is not None
    if username_already_taken:
        raise UsernameAlreadyTaken()

    email_already_taken = User.get_or_none(User.email == email) is not None
    if email_already_taken:
        raise EmailAlreadyTaken()

    salt = urandom(16)
    password_hash = pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, N_ITERATIONS
    )
    new_user = User.create(
        username=username,
        password_hash=password_hash,
        salt=salt,
        email=email,
    )
    return UserToken.create(
        user=new_user,
        token=uuid.uuid4().hex,
        expiry=datetime.datetime.now() + datetime.timedelta(days=7),
    )


def login(username: str, password: str) -> UserToken:
    user = User.get_or_none(User.username == username)
    if user is None:
        raise InvalidUserCredentials()

    hashed_password = pbkdf2_hmac(
        "sha256", password.encode("utf-8"), user.salt, N_ITERATIONS
    )

    if hashed_password != user.password_hash:
        raise InvalidUserCredentials()

    user_token = UserToken.create(
        user=user,
        token=uuid.uuid4().hex,
        expiry=datetime.datetime.now() + datetime.timedelta(days=7),
    )
    return user_token


def logout(user_token: str) -> None:
    validate_token(user_token)
    UserToken.get(UserToken.token == user_token).delete_instance()


def change_password(user_token: str, old_password: str, new_password: str) -> None:
    validate_token(user_token)

    user = (
        User.select(User.salt, User.password_hash)
        .join(UserToken)
        .get(UserToken.token == user_token)
    )
    hashed_old_password = pbkdf2_hmac(
        "sha256", old_password.encode("utf-8"), user.salt, N_ITERATIONS
    )
    if hashed_old_password != user.password_hash:
        raise InvalidUserCredentials()

    hashed_new_password = pbkdf2_hmac(
        "sha256", new_password.encode("utf-8"), user.salt, N_ITERATIONS
    )
    user.password_hash = hashed_new_password
    user.save()


def get(user_token: str) -> User:
    validate_token(user_token)
    return UserToken.select(UserToken.user).get(UserToken.token == user_token)


def toggle_one_verse_recitation(user_token: str) -> None:
    user = get(user_token)
    user.one_verse_recitation.db_value(not user.one_verse_recitation)
    user.save()


def toggle_complete_recitation(user_token: str) -> None:
    user = get(user_token)
    user.complete_recitation.db_value(not user.complete_recitation)
    user.save()


def toggle_fast_recitations(user_token: str) -> None:
    user = get(user_token)
    user.fast_recitations.db_value(not user.fast_recitations)
    user.save()


def toggle_include_verse_numbers(user_token: str) -> None:
    user = get(user_token)
    user.include_verse_numbers.db_value(not user.include_verse_numbers)
    user.save()


def set_translation(user_token: str, translation: str) -> None:
    user = get(user_token)

    if translation not in Translations:
        raise InvalidTranslation(translation)

    user.translation.db_value(translation)
    user.save()
