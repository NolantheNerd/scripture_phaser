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

class Recitation(Enum):
    RAW_TEXT = 1
    NUMBERED_TEXT = 2
    REFERENCE_TEXT = 3
    FULL_TEXT = 4
    RAW_INITIALISM = 5
    NUMBERED_INITIALISM = 6

def record_recitation(passage: Passage, type: RecitationType, attempt: str) -> None:
    timestamp = datetime.datetime.now()
    score = grade_attempt()

def grade_attempt(passage: Passage, recitation: Recitation, attempt: str) -> float:
    if recitation is Recitation.RAW_TEXT:
        solution = passage.raw_text
        grade_str = True
        grade_list = False
    elif recitation is Recitation.NUMBERED_TEXT:
        solution = passage.numbered_text
        grade_str = True
        grade_list = False
    elif recitation is Recitation.REFERENCE_TEXT:
        soluiton = passage.reference_text
        grade_str = True
        grade_list = False
    elif recitation is Recitation.FULL_TEXT:
        solution = passage.full_text
        grade_str = True
        grade_list = False
    elif recitation is Recitation.RAW_INITIALISM:
        solution = passage.raw_initialism
        grade_str = False
        grade_list = True
    elif recitation is Recitation.NUMBERED_INITIALISM:
        solution = passage.numbered_initialism
        grade_str = False
        grade_list = True

    if grade_str:
        if attempt == solution:
            score = 1
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
            score = 1
        else:
            n_correct = sum(
                [1 for i in range(len(solution)) if attempt[i] == solution[i]]
            )
            score = n_correct / len(solution)

    return score
