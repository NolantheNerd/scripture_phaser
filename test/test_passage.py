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

from unittest import TestCase
from unittest.mock import patch
from scripture_phaser.backend.reference import reference_from_string
from scripture_phaser.backend.passage import passage_from_reference, Passage

class PassageTests(TestCase):
    @patch("scripture_phaser.backend.translations.KJV.fetch")
    def test_passage(self, mock_fetch) -> None:
        """
        Do passages populate properly?
        """
        reference = reference_from_string("1 Peter 1:2 - 1:3")

        mock_api_return = [
            (
                "Elect according to the foreknowledge of God the Father, "
                + "through sanctification of the Spirit, unto obedience and "
                + "sprinkling of the blood of Jesus Christ: Grace unto you, "
                + "and peace, be multiplied."
            ),
            (
                "Blessed be the God and Father of our Lord Jesus Christ, which "
                + "according to his abundant mercy hath begotten us again unto "
                + "a lively hope by the resurrection of Jesus Christ from the dead,"
            ),
        ]
        mock_fetch.return_value = mock_api_return
        # reference.agent.fetch = MagicMock(return_value=mock_api_return)
        passage = passage_from_reference("KJV", reference)

        raw = (
            "Elect according to the foreknowledge of God the Father, "
            + "through sanctification of the Spirit, unto obedience and "
            + "sprinkling of the blood of Jesus Christ: Grace unto you, "
            + "and peace, be multiplied. "
            + "Blessed be the God and Father of our Lord Jesus Christ, which "
            + "according to his abundant mercy hath begotten us again unto "
            + "a lively hope by the resurrection of Jesus Christ from the dead,"
        )

        number = (
            "[2] Elect according to the foreknowledge of God the Father, "
            + "through sanctification of the Spirit, unto obedience and "
            + "sprinkling of the blood of Jesus Christ: Grace unto you, "
            + "and peace, be multiplied. "
            + "[3] Blessed be the God and Father of our Lord Jesus Christ, which "
            + "according to his abundant mercy hath begotten us again unto "
            + "a lively hope by the resurrection of Jesus Christ from the dead,"
        )

        ref = (
            "Elect according to the foreknowledge of God the Father, "
            + "through sanctification of the Spirit, unto obedience and "
            + "sprinkling of the blood of Jesus Christ: Grace unto you, "
            + "and peace, be multiplied. "
            + "Blessed be the God and Father of our Lord Jesus Christ, which "
            + "according to his abundant mercy hath begotten us again unto "
            + "a lively hope by the resurrection of Jesus Christ from the dead,"
            + " - 1 Peter 1:2-3"
        )

        full = (
            "[2] Elect according to the foreknowledge of God the Father, "
            + "through sanctification of the Spirit, unto obedience and "
            + "sprinkling of the blood of Jesus Christ: Grace unto you, "
            + "and peace, be multiplied. "
            + "[3] Blessed be the God and Father of our Lord Jesus Christ, which "
            + "according to his abundant mercy hath begotten us again unto "
            + "a lively hope by the resurrection of Jesus Christ from the dead,"
            + " - 1 Peter 1:2-3"
        )

        initialism = [
            "E", "a", "t", "t", "f", "o", "G", "t", "F", "t", "s", "o", "t", "S", "u", "o", "a", "s", "o", "t", "b", "o", "J", "C", "G", "u", "y", "a", "p", "b", "m", "B", "b", "t", "G", "a", "F", "o", "o", "L", "J", "C", "w", "a", "t", "h", "a", "m", "h", "b", "u", "a", "u", "a", "l", "h", "b", "t", "r", "o", "J", "C", "f", "t", "d"
        ]

        numbered_initialism = [
            "2", "E", "a", "t", "t", "f", "o", "G", "t", "F", "t", "s", "o", "t", "S", "u", "o", "a", "s", "o", "t", "b", "o", "J", "C", "G", "u", "y", "a", "p", "b", "m", "3", "B", "b", "t", "G", "a", "F", "o", "o", "L", "J", "C", "w", "a", "t", "h", "a", "m", "h", "b", "u", "a", "u", "a", "l", "h", "b", "t", "r", "o", "J", "C", "f", "t", "d"
        ]

        expected_passage = Passage(reference, "KJV",  raw, number, ref, full, initialism, numbered_initialism)

        self.assertEqual(passage, expected_passage)
