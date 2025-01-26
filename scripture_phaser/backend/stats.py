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
from peewee import fn
from scripture_phaser.backend.models import Recitation
from scripture_phaser.backend.reference import Reference


class Stats:
    def __init__(self) -> None:
        if not Recitation.table_exists():
            Recitation.create_table()

    @staticmethod
    def reset_db() -> None:
        if Recitation.table_exists():
            Recitation.drop_table()
        Recitation.create_table()

    @staticmethod
    def get_streak() -> int:
        datetimes = Recitation.select(Recitation.datetime).order_by(
            Recitation.datetime.desc()
        )
        dates = {dt.datetime.date() for dt in datetimes}

        streak = 0
        date = datetime.date.today()
        while True:
            if date in dates:
                streak += 1
                date -= datetime.timedelta(days=1)
            else:
                break

        return streak

    @staticmethod
    def get_num_attempts_past_year() -> int:
        one_year_ago = datetime.date.today() - datetime.timedelta(days=365)
        return int(
            Recitation.select().where(Recitation.datetime > one_year_ago).count()
        )

    @staticmethod
    def get_num_attempts_past_year_by_day() -> list[int]:
        today = datetime.date.today()
        days_since_monday = today.weekday()
        start_date = today - datetime.timedelta(days=days_since_monday, weeks=52)
        results = [0] * ((today - start_date).days + 1)
        day_counts = (
            Recitation.select(Recitation.datetime, fn.COUNT(Recitation).alias("num"))
            .where(Recitation.datetime > start_date)
            .group_by(fn.date_trunc("day", Recitation.datetime))
            .order_by(Recitation.datetime)
        )

        for day in day_counts:
            results[(day.datetime.date() - start_date).days] = day.num

        return results

    @staticmethod
    def all_verses_ranked() -> tuple[dict[Reference, float], dict[Reference, int]]:
        verse_scores, verse_counts = {}, {}
        all_attempts = Recitation.select(Recitation.reference)
        for reference in all_attempts:
            ref = reference.reference
            attempts = Recitation.select(Recitation.score).where(
                Recitation.reference == ref
            )
            scores = [attempt.score for attempt in attempts]
            verse_scores[ref] = sum(scores) / len(scores)
            verse_counts[ref] = len(scores)
        return verse_scores, verse_counts
