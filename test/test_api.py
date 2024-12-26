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

# import random
# from unittest.mock import patch
# from unittest.mock import MagicMock
# from test.test_base import BaseTest
# from scripture_phaser.backend.api import API
# from scripture_phaser.backend.reference import Reference
# from scripture_phaser.backend.exceptions import InvalidTranslation
#
#
# class APITests(BaseTest):
#     """
#     Test Backend API
#     """
#
#     def test_translation_setter(self) -> None:
#         """
#         Are invalid translation selections rejected?
#         """
#         api = API()
#         with self.assertRaises(InvalidTranslation):
#             api.set_translation("EESV")
#
#     def test_get_random_verse(self) -> None:
#         """
#         Can random verses be selected from a passage?
#         """
#         translation = "ESV"
#         ref = Reference(translation, "John 1:1-5")
#
#         raw_list = [
#             "In the beginning was the Word, and the Word was with God, and the "
#             + "Word was God.",
#             "He was in the beginning with God.",
#             "All things were made through him, and without him was not any "
#             + "thing made that was made.",
#             "In him was life, and the life was the light of men.",
#             "The light shines in the darkness, and the darkness has not overcome it.",
#         ]
#
#         ref.agent.fetch = MagicMock(return_value=raw_list)
#         ref.populate()
#
#         api = API()
#
#         if api.complete_recitation:
#             api.toggle_complete_recitation()
#         if not api.one_verse_recitation:
#             api.toggle_one_verse_recitation()
#
#         api.add_reference(ref)
#
#         random.seed(45)
#         self.assertEqual(api.get_reference().ref_str, "John 1:4")
#
#     def test_grade(self) -> None:
#         """
#         Can the correct grade be assigned to a recitation?
#         """
#         api = API()
#
#         if api.one_verse_recitation:
#             api.toggle_one_verse_recitation()
#
#         correct_string = "This is the correct way to write this string."
#         attempt_string = "This is an attempted way to write this string."
#
#         expected_score = 0.6923076923076923
#
#         api.reference = Reference("NIV", "Genesis 1:1")
#         api.reference.agent.fetch = MagicMock(return_value=[correct_string])
#
#         # Prevent this test from adding entries into the DB
#         with patch("scripture_phaser.backend.api.Attempt") as attempt:
#             # This gets the score - its ugly and I wrote it using the debugger
#             _ = api.recite(api.reference, attempt_string)
#             score = attempt.method_calls[0]._get_call_arguments()[1]["score"]
#
#         self.assertAlmostEqual(expected_score, score)
