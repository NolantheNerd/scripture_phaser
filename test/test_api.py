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

import random
from unittest.mock import patch
from unittest.mock import MagicMock
from test.test_base import BaseTest
from src.api import API
from src.passage import Passage
from src.reference import Reference
from src.exceptions import InvalidTranslation


class APITests(BaseTest):
    """
    Test Backend API
    """
    def test_translation_setter(self):
        """
        Are invalid translation selections rejected?
        """
        api = API()
        with self.assertRaises(InvalidTranslation):
            api.set_translation("EESV")

    def test_get_random_verse(self):
        """
        Can random verses be selected from a passage?
        """
        ref = Reference("John 1:1-5")
        translation = "ESV"

        raw_list = [
        'In the beginning was the Word, and the Word was with God, and the ' +
        'Word was God.',
        'He was in the beginning with God.',
        'All things were made through him, and without him was not any ' +
        'thing made that was made.',
        'In him was life, and the life was the light of men.',
        'The light shines in the darkness, and the darkness has not overcome it.'
        ]

        passage = Passage(ref, translation)
        passage.agent.fetch = MagicMock(return_value=raw_list)
        passage.populate()

        api = API()
        api.passage = passage # "Mocking" the Passage Property

        random.seed(45)
        self.assertEqual(api.get_random_verse().ref_str, "John 1:3")

    def test_grade(self):
        """
        Can the correct grade be assigned to a recitation?
        """
        api = API()
        if api.random_single_verse:
            api.set_random_single_verse()

        correct_string = "This is the correct way to write this string."
        attempt_string = "This is an attempted way to write this string."

        expected_score = 0.6923076923076923

        api.reference = MagicMock()
        api.reference.ref_str = "2 Hesitations 7:490"

        api.get_recitation_ans = MagicMock()
        api.get_recitation_ans.return_value = correct_string

        # Prevent this test from adding entries into the DB
        with patch("src.api.Attempt"):
            score = api.finish_recitation(api.reference, attempt_string)

        self.assertAlmostEqual(expected_score, score)

    def test_get_fast_recitation_ans(self):
        """
        Can the API fetch the first letter of each word in a passage?
        """
        api = API()
        content = "All Scripture is breathed out by God and profitable " + \
        "for teaching, for reproof, for correction, and for training in " + \
        "righteousness, that the man of God may be complete, equipped " + \
        "for every good work."

        api.reference = MagicMock()
        api.reference.ref_str = "2 Timothy 3:16-17"

        api.passage = MagicMock()
        api.passage.reference = api.reference
        api.passage.show.return_value = content

        expected = ["A", "S", "i", "b", "o", "b", "G", "a", "p", "f", "t", 
                    "f", "r", "f", "c", "a", "f", "t", "i", "r", "t", "t",
                    "m", "o", "G", "m", "b", "c", "e", "f", "e", "g", "w"]

        self.assertEqual(api.get_fast_recitation_ans(api.reference), expected)
