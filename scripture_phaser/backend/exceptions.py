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

from typing import Optional


class InvalidReference(Exception):
    def __init__(
        self,
        ref_string: Optional[str] = None,
        id: Optional[int] = None,
        end_id: Optional[int] = None,
    ) -> None:
        if ref_string is not None:
            Exception.__init__(self, f"{ref_string} is not a valid Bible reference")
        elif id is not None and end_id is not None:
            Exception.__init__(
                self, f"End Verse id ({end_id}) is greater than start verse id ({id})"
            )


class InvalidTranslation(Exception):
    def __init__(self, translation: str) -> None:
        Exception.__init__(self, f"{translation} is not a valid translation")


class EditorNotFound(Exception):
    def __init__(self) -> None:
        Exception.__init__(
            self,
            "Text editor not found; set the 'EDITOR' environmental variable and try again",
        )


class NoReferences(Exception):
    def __init__(self) -> None:
        Exception.__init__(self, "No available references")


class UsernameAlreadyTaken(Exception):
    def __init__(self) -> None:
        Exception.__init__(self, "Username already taken")


class EmailAlreadyTaken(Exception):
    def __init__(self) -> None:
        Exception.__init__(self, "Email already taken")