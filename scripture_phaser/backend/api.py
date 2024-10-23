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
import scripture_phaser.backend.user as User
import scripture_phaser.backend.reference as Reference

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


# @api.delete("/remove_reference/")
# def remove_reference(user_token: str, ref: str) -> None:
#     user = UserToken.get(UserToken.token == user_token).user
#     ref = Reference(ref)
#     Ref.get(Ref.user == user & Ref.reference == ref.ref_str).delete_instance()
#
#
# @api.post("/toggle_one_verse_rectitation/")
# def toggle_one_verse_recitation(user_token: str) -> None:
#     user = UserToken.get(UserToken.token == user_token).user
#     user.one_verse_recitation = not user.one_verse_recitation
#     user.save()
#
#
# @api.post("/toggle_complete_recitation/")
# def toggle_complete_recitation(user_token: str) -> None:
#     user = UserToken.get(UserToken.token == user_token).user
#     user.complete_recitation = not user.complete_recitation
#     user.save()
#
#
# @api.post("/toggle_fast_recitations/")
# def toggle_fast_recitations(user_token: str) -> None:
#     user = UserToken.get(UserToken.token == user_token).user
#     user.fast_recitations = not user.fast_recitations
#     user.save()
#
#
# @api.post("/toggle_include_verse_numbers/")
# def toggle_include_verse_numbers(user_token: str) -> None:
#     user = UserToken.get(UserToken.token == user_token).user
#     user.include_verse_numbers = not user.include_verse_numbers
#     user.save()
#
#
# @api.post("/set_translation/")
# def set_translation(user_token: str, translation: str) -> None:
#     if translation not in Translations:
#         raise InvalidTranslation(translation)
#
#     user = UserToken.get(UserToken.token == user_token).user
#     user.translation = translation
#     user.save()
#
#
# @api.get("/list_references/")
# def list_references(user_token: str) -> List[str]:
#     user = UserToken.get(UserToken.token == user_token).user
#     user_references = Ref.select(Ref.reference).where(Reference.user == user)
#     return [ref.reference for ref in user_references]
#
#
# @api.get("/view_reference/")
# def view_reference(
#    ref: Ref, include_verse_numbers: bool = False, include_ref: bool = True
# ) -> str:
#    return ref.view(
#        include_verse_numbers=include_verse_numbers, include_ref=include_ref
#    )
#
#
# def get_reference(self) -> Reference:
#    if len(self.references) == 0:
#        raise NoReferences()
#
#    chosen_reference = rd.choice(self.references)
#    if not self.complete_recitation:
#        if self.one_verse_recitation:
#            chosen_id = rd.randrange(chosen_reference.start_id, chosen_reference.end_id + 1)
#            return Reference(self.translation, id=chosen_id)
#        else:
#            chosen_start_id = rd.randrange(chosen_reference.start_id, chosen_reference.end_id + 1)
#            chosen_end_id = rd.randrange(chosen_start_id, chosen_reference.end_id + 1)
#            return Reference(self.translation, id=chosen_start_id, end_id=chosen_end_id)
#    else:
#        return chosen_reference
#
# def recite(self, reference: Reference, text: str) -> Attempt:
#    if self.fast_recitations:
#        ans = reference.view_first_letter(self.include_verse_numbers)
#
#        if text == ans:
#            score = 1
#        else:
#            n_correct = sum([1 for i in range(len(ans)) if text[i] == ans[i]])
#            score = n_correct / len(ans)
#    else:
#        ans = reference.view(self.include_verse_numbers, include_ref=False)
#
#        if text == ans:
#            score = 1
#        else:
#            n_correct_chars, n_incorrect_chars = 0, 0
#            result = SequenceMatcher(a=text, b=ans).get_opcodes()
#            for tag, i1, i2, j1, j2 in result:
#                if tag == "replace":
#                    n_incorrect_chars += max([(j2 - j1), (i2 - i1)])
#                elif tag == "delete":
#                    n_incorrect_chars += i2 - i1
#                elif tag == "insert":
#                    n_incorrect_chars += j2 - j1
#                elif tag == "equal":
#                    n_correct_chars += i2 - i1
#
#            score = n_correct_chars / (n_correct_chars + n_incorrect_chars)
#
#    return Attempt.create(
#        reference=reference.ref_str,
#        score=score,
#        attempt=text,
#        datetime=datetime.datetime.now()
#    )
