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

import uuid
import datetime
from os import urandom
from hashlib import pbkdf2_hmac
from scripture_phaser.backend.models import User, UserToken
from scripture_phaser.backend.exceptions import (
    UsernameAlreadyTaken,
    EmailAlreadyTaken,
)


def create(username: str, password: str, email: str) -> UserToken:
    username_already_taken = User.get_or_none(User.username == username) is not None
    if username_already_taken:
        raise UsernameAlreadyTaken()

    email_already_taken = User.get_or_none(User.email == email) is not None
    if email_already_taken:
        raise EmailAlreadyTaken()

    salt = urandom(16)
    password_hash = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    new_user = User.create(
        username=username,
        password_hash=password_hash,
        salt=salt,
        hash_algorithm="PBKDF2",
        iterations=100000,
        email=email,
    )
    token = uuid.uuid4().hex
    return UserToken.create(
        user=new_user,
        token=token,
        expiry=datetime.datetime.now() + datetime.timedelta(days=7),
    )
