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

import datetime
from enum import Enum
from difflib import SequenceMatcher
from scripture_phaser.backend.passage import Passage
from scripture_phaser.backend.models import Recitation as RecitationTable


class Recitation(Enum):
    RAW_TEXT = 1
    NUMBERED_TEXT = 2
    REFERENCE_TEXT = 3
    FULL_TEXT = 4
    RAW_INITIALISM = 5
    NUMBERED_INITIALISM = 6


def record_recitation(passage: Passage, type: int, attempt: str) -> None:
    timestamp = datetime.datetime.now()
    score = grade_attempt(passage, type, attempt)
    RecitationTable.create(
        datetime=timestamp,
        reference=passage.reference,
        translation=passage.translation,
        recitation_type=type,
        score=score,
        recitation=attempt,
    )


def grade_attempt(passage: Passage, recitation: int, attempt: str) -> float:
    solution: str | list[str]

    if recitation == Recitation.RAW_TEXT.value:
        solution = passage.raw_text
        grade_str = True
        grade_list = False
    elif recitation == Recitation.NUMBERED_TEXT.value:
        solution = passage.numbered_text
        grade_str = True
        grade_list = False
    elif recitation == Recitation.REFERENCE_TEXT.value:
        solution = passage.reference_text
        grade_str = True
        grade_list = False
    elif recitation == Recitation.FULL_TEXT.value:
        solution = passage.full_text
        grade_str = True
        grade_list = False
    elif recitation == Recitation.RAW_INITIALISM.value:
        solution = passage.raw_initialism
        grade_str = False
        grade_list = True
    elif recitation == Recitation.NUMBERED_INITIALISM.value:
        solution = passage.numbered_initialism
        grade_str = False
        grade_list = True

    if grade_str:
        if attempt == solution:
            score = 1.0
        else:
            n_correct_chars, n_incorrect_chars = 0, 0
            result = SequenceMatcher(a=attempt, b=solution).get_opcodes()
            for tag, i1, i2, j1, j2 in result:
                if tag == "replace":
                    n_incorrect_chars += max([(j2 - j1), (i2 - i1)])
                elif tag == "delete":
                    n_incorrect_chars += i2 - i1
                elif tag == "insert":
                    n_incorrect_chars += j2 - j1
                elif tag == "equal":
                    n_correct_chars += i2 - i1

            score = n_correct_chars / (n_correct_chars + n_incorrect_chars)

    elif grade_list:
        if attempt == solution:
            score = 1.0
        else:
            n_correct = sum(
                [1 for i in range(len(solution)) if attempt[i] == solution[i]]
            )
            score = n_correct / len(solution)

    return score
