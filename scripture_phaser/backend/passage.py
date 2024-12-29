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

from dataclasses import dataclass
from scripture_phaser.backend.reference import Reference
from scripture_phaser.backend.translations import Translation
import scripture_phaser.backend.translations as Translations


@dataclass
class Verse:
    raw: str
    number: str
    reference: str
    full: str
    initialism: list[str]
    numbered_initialism: list[str]


@dataclass
class Passage:
    reference: str
    translation: Translation
    verse: Verse


def passage_from_reference(translation: str, reference: Reference) -> Passage:
    translation = getattr(Translations, translation)
    texts = Translations[translation].fetch(reference.start_id, reference.end_id)
    raw = _format_passage(
        reference, texts, include_verse_numbers=False, include_ref=False
    )
    number = _format_passage(
        reference, texts, include_verse_numbers=True, include_ref=False
    )
    reference = _format_passage(
        reference, texts, include_verse_numbers=False, include_ref=True
    )
    full = _format_passage(
        reference, texts, include_verse_numbers=True, include_ref=True
    )
    initialism = _format_passage_initialism(
        reference, texts, include_verse_numbers=False
    )
    numbered_initialism = _format_passage_initialism(
        reference, texts, include_verse_numbers=True
    )
    verse = Verse(raw, number, reference, full, initialism, numbered_initialism)
    return Passage(reference, translation, verse)


def _format_passage(
    reference: Reference,
    texts: list[str],
    include_verse_numbers: bool,
    include_ref: bool,
) -> str:
    if not include_verse_numbers:
        text = f"{' '.join(texts)}".replace("\n ", "\n")
    else:
        text = ""
        for i, content in enumerate(texts):
            _, _, verse_num = Reference.id_to_reference(reference.start_id + i)
            text += f" [{verse_num + 1}] {content}"
        text = text.strip()

    if include_ref:
        return f"{text} - {reference.ref_str}"
    else:
        return f"{text}".replace("\n ", "\n")


def _format_passage_initialism(
    reference: Reference, texts: list[str], include_verse_numbers: bool
) -> list[str]:
    if not include_verse_numbers:
        text = texts
    else:
        text = ""
        for i, content in enumerate(texts):
            _, _, verse_num = Reference.id_to_reference(reference.start_id + i)
            text += f"[{verse_num + 1}] {content}"

    text = "".join([char for char in text if char.isalnum() or char.isspace()])
    return [word[0] for word in text.split()]