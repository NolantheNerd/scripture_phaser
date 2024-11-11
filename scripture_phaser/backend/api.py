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

from fastapi import FastAPI
from typing import List
import scripture_phaser.backend.user as User
import scripture_phaser.backend.reference as Reference
from scripture_phaser.backend.enum import Translations

api = FastAPI()


@api.post("/create_account")
def new_user(username: str, password: str, email: str) -> str:
    user_token = User.create(username=username, password=password, email=email)
    return user_token.token


@api.get("/login")
def login(username: str, password: str) -> str:
    user_token = User.login(username=username, password=password)
    return user_token.token


@api.delete("/logout")
def logout(user_token: str) -> None:
    User.logout(user_token)


@api.post("/change_password")
def change_password(user_token: str, old_password: str, new_password: str) -> None:
    User.change_password(
        user_token=user_token, old_password=old_password, new_password=new_password
    )


@api.post("/new_reference")
def add_reference(user_token: str, ref: str) -> None:
    user = User.get(user_token)
    Reference.add(user, ref)


@api.delete("/remove_reference")
def remove_reference(user_token: str, ref: str) -> None:
    user = User.get(user_token)
    Reference.delete(user, ref)


@api.get("/view_reference")
def view_reference(user_token: str, ref: str) -> None:
    user = User.get(user_token)
    return Reference.view(user, ref)


@api.get("/list_references")
def list_references(user_token: str) -> List[str]:
    user = User.get(user_token)
    return Reference.list_references(user)


@api.get("/list_translations")
def list_translations(user_token: str) -> List[str]:
    return Translations


@api.post("/toggle_one_verse_rectitation")
def toggle_one_verse_recitation(user_token: str) -> None:
    User.toggle_one_verse_recitation(user_token)


@api.post("/toggle_complete_recitation")
def toggle_complete_recitation(user_token: str) -> None:
    User.toggle_complete_recitation(user_token)


@api.post("/toggle_fast_recitations")
def toggle_fast_recitations(user_token: str) -> None:
    User.toggle_fast_recitations(user_token)


@api.post("/toggle_include_verse_numbers")
def toggle_include_verse_numbers(user_token: str) -> None:
    User.toggle_include_verse_numbers(user_token)


@api.post("/set_translation")
def set_translation(user_token: str, translation: str) -> None:
    User.set_translation(user_token, translation)


@api.post("/recite_reference")
def recite_reference(user_token: str, reference: str, recitation: str) -> None:
    user = User.get(user_token)
    grade_recitation(user, reference, recitation)
