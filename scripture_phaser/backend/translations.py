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

from pathlib import Path
from typing import TypeAlias


class OfflineAgent:
    def __init__(self, translation: str) -> None:
        self.translation = translation

    def fetch(self, id_start: int, id_end: int) -> list[str]:
        texts = []

        translation_dir = Path(__file__).parent.parent.absolute()

        translation_filepath = translation_dir / (self.translation.lower() + ".txt")
        with open(translation_filepath, "r") as translation_file:
            for _ in range(id_start - 1):
                next(translation_file)
            for _ in range(id_end - id_start + 1):
                texts.append(translation_file.readline())

        return texts


class KJV(OfflineAgent):
    def __init__(self) -> None:
        super().__init__(translation="KJV")


class WEB(OfflineAgent):
    def __init__(self) -> None:
        super().__init__(translation="WEB")


class ERV(OfflineAgent):
    def __init__(self) -> None:
        super().__init__(translation="ERV")


class ASV(OfflineAgent):
    def __init__(self) -> None:
        super().__init__(translation="ASV")

Translation: TypeAlias = (KJV, WEB, ERV, ASV)
