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

import datetime
from src.models import Attempt


class Stats:
    def __init__(self):
        self.start_date = None
        self.end_date = None

    def apply_filters(self, query):
        if self.start_date is not None:
            query = query.where(Attempt.datetime >= self.start_date)
        if self.end_date is not None:
            query = query.where(Attempt.datetime <= self.end_date)
        return query

    def all_attempted_verses(self):
        attempts = self.apply_filters(Attempt.select(Attempt.reference))
        return {attempt.reference for attempt in attempts}

    def all_verses_ranked(self):
        verses = {}
        for ref in self.all_attempted_verses():
            attempts = self.apply_filters(
                Attempt.select(Attempt.score).where(Attempt.reference == ref)
            )
            scores = [attempt.score for attempt in attempts]
            verses[ref] = sum(scores) / len(scores)
        return verses

    def verse_by_reference(self, ref):
        attempts = self.apply_filters(
            Attempt.select(Attempt.datetime, Attempt.score).where(Attempt.reference == ref).order_by(Attempt.id)
        )
        return [(a.datetime, a.score) for a in attempts]
