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
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from hashlib import pbkdf2_hmac
from scripture_phaser.backend.models import User as UserModel, UserToken
from scripture_phaser.backend.exceptions import InvalidUserToken

api = APIRouter(tags=["User"])
N_ITERATIONS = 100000


class UserCredentials(BaseModel):
    name: str
    username: str
    email: str
    token: str


class NewUserDetails(BaseModel):
    name: str
    username: str
    password: str
    email: str


class SignInCredentials(BaseModel):
    username: str
    password: str


def validate_token(user_token: str) -> None:
    token = UserToken.get_or_none(UserToken.token == user_token)
    if token is None:
        raise InvalidUserToken()

    if token.expiry < datetime.datetime.now():
        token.delete_instance()
        raise InvalidUserToken()


@api.post("/signup")
def create_user(new_user_details: NewUserDetails) -> UserCredentials:
    username_already_taken = (
        UserModel.get_or_none(UserModel.username == new_user_details.username)
        is not None
    )
    if username_already_taken:
        raise HTTPException(status_code=403, detail="Username Already Taken")

    email_already_taken = (
        UserModel.get_or_none(UserModel.email == new_user_details.email) is not None
    )
    if email_already_taken:
        raise HTTPException(status_code=403, detail="Email Already Taken")

    salt = urandom(16)
    password_hash = pbkdf2_hmac(
        "sha256", new_user_details.password.encode("utf-8"), salt, N_ITERATIONS
    )

    new_user = UserModel.create(
        name=new_user_details.name,
        username=new_user_details.username,
        password_hash=password_hash,
        salt=salt,
        email=new_user_details.email,
    )

    # @@@ TODO: Make sure that token is unique in UserToken
    token = uuid.uuid4().hex
    UserToken.create(
        user=new_user,
        token=token,
        expiry=datetime.datetime.now() + datetime.timedelta(days=7),
    )

    return UserCredentials(
        name=new_user_details.name,
        username=new_user_details.username,
        email=new_user_details.email,
        token=token,
    )


@api.delete("/delete_user")
def delete_user(user_credentials: UserCredentials) -> None:
    validate_token(user_credentials.token)
    UserModel.select(
        UserModel.username == user_credentials.username
    ).delete_instance()


@api.post("/login")
def login(login_credentials: SignInCredentials) -> UserCredentials:
    user = UserModel.get_or_none(UserModel.username == login_credentials.username)
    if user is None:
        raise HTTPException(status_code=403, detail="Invalid User Credentials")

    hashed_password = pbkdf2_hmac(
        "sha256", login_credentials.password.encode("utf-8"), user.salt, N_ITERATIONS
    )

    if hashed_password != user.password_hash:
        raise HTTPException(status_code=403, detail="Invalid User Credentials")

    token = uuid.uuid4().hex
    UserToken.create(
        user=user,
        token=token,
        expiry=datetime.datetime.now() + datetime.timedelta(days=7),
    )
    return UserCredentials(
        name=user.name, username=user.username, email=user.email, token=token
    )


@api.delete("/logout")
def logout(user_credentials: UserCredentials) -> None:
    validate_token(user_credentials.token)
    UserToken.get(UserToken.token == user_credentials.token).delete_instance()


@api.post("/change_password")
def change_password(
    user_credentials: UserCredentials, old_password: str, new_password: str
) -> None:
    validate_token(user_credentials.token)

    user_record = (
        UserModel.select()
        .join(UserToken)
        .where(UserToken.token == user_credentials.token)
        .get()
    )
    hashed_old_password = pbkdf2_hmac(
        "sha256", old_password.encode("utf-8"), user_record.salt, N_ITERATIONS
    )
    if hashed_old_password != user_record.password_hash:
        raise HTTPException(status_code=403, detail="Invalid User Credentials")

    hashed_new_password = pbkdf2_hmac(
        "sha256", new_password.encode("utf-8"), user_record.salt, N_ITERATIONS
    )
    user_record.password_hash = hashed_new_password
    user_record.save()
