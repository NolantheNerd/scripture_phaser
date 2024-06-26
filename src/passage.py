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

from src.agents import Agents
from src.reference import Reference


class Passage:
    def __init__(self, reference, translation, require_passage_numbers=False):
        self.agent = Agents[translation]
        self.reference = reference
        self.texts = []
        self.populated = False
        self.require_passage_numbers = require_passage_numbers

    def populate(self):
        self.populated = True
        self.texts = self.agent.fetch(self.reference)

    def show(self, index=None, with_verse=False, with_ref=False):
        if not self.populated:
            return ""
        else:
            if index is None:
                if with_verse or self.require_passage_numbers:
                    text = ""
                    for i, content in enumerate(self.texts):
                        _, _, verse_num = Reference.id_to_reference(self.reference.start_id + i)
                        text += f"[{verse_num + 1}] " + content
                else:
                    text = " ".join(self.texts)

                if with_ref:
                    text = f"{text} - {self.reference.ref_str}"

            else:
                if with_verse or self.require_passage_numbers:
                    _, _, verse_num = Reference.id_to_reference(self.reference.start_id + index)
                    text = f"[{verse_num + 1}]" + self.texts[index]
                else:
                    text = self.texts[index]

                if with_ref:
                    text = f"{text} - {Reference(id=index).ref_str}"

            # Spaces after new lines are no good
            text = text.replace("\n ", "\n")

            return text
