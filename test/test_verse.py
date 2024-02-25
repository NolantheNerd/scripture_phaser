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

from src.verse import Verse
from test.test_base import BaseTest


class VerseTests(BaseTest):
    """
    Test the Verse Object
    """
    def test_validate(self):
        """
        Are illegitimate verses uninstantiatable?
        """
        # Job 1:1
        ref1 = Verse(17, 0, 0)
        # Psalm 151:1
        ref2 = Verse(18, 150, 0)
        # 1 Samuel 1:200
        ref3 = Verse(8, 0, 200)
        # 3 John 1:5
        ref4 = Verse(63, 0, 4)
        # Steven 1:1
        ref5 = Verse(-1, 0, 0)

        self.assertTrue(Verse.validate(ref1))
        self.assertFalse(Verse.validate(ref2))
        self.assertFalse(Verse.validate(ref3))
        self.assertTrue(Verse.validate(ref4))
        self.assertFalse(Verse.validate(ref5))

    def test_show(self):
        """
        Do verses preview correctly?
        """
        # John 11:35
        text = "Jesus wept."
        verse = Verse(42, 10, 34, text)

        self.assertEqual(
            verse.show(),
            text
        )

        self.assertEqual(
            verse.show(with_verse=True),
            f"[35] {text}"
        )

        self.assertEqual(
            verse.show(with_ref=True),
            f"{text} - John 11:35"
        )

        self.assertEqual(
            verse.show(with_verse=True, with_ref=True),
            f"[35] {text} - John 11:35"
        )
