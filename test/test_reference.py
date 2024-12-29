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

from unittest import TestCase, skip
from unittest.mock import patch
from scripture_phaser.backend.reference import Reference, reference_from_id, reference_from_string, _interpret_reference, _standardize_reference
from scripture_phaser.backend.exceptions import InvalidReference


class ReferenceTests(TestCase):
    """
    Test the Reference Implementation
    """
    def test_interpret_reference(self) -> None:
        """
        Can reference strings be interpreted?
        """
        verse_string1 = "1 John 3:5"
        expected1 = (61, 2, 4, 61, 2, 4)
        self.assertEqual(_interpret_reference(verse_string1), expected1)

        verse_string2 = "genesis 5:1"
        expected2 = (0, 4, 0, 0, 4, 0)
        self.assertEqual(_interpret_reference(verse_string2), expected2)

        verse_string3 = "exodus 1 -   2"
        expected3 = (1, 0, 0, 1, 1, 24)
        self.assertEqual(_interpret_reference(verse_string3), expected3)

        verse_string4 = "First Peter - 2 peter 1 : 5"
        expected4 = (59, 0, 0, 60, 0, 4)
        self.assertEqual(_interpret_reference(verse_string4), expected4)

        verse_string5 = "psalm-proverbs"
        expected5 = (18, 0, 0, 19, 30, 30)
        self.assertEqual(_interpret_reference(verse_string5), expected5)

        verse_string6 = "Ezra 1 : 2-2 : 1"
        expected6 = (14, 0, 1, 14, 1, 0)
        self.assertEqual(_interpret_reference(verse_string6), expected6)

        verse_string7 = "First Peter 1:1 - 1 peter 1 : 5"
        expected7 = (59, 0, 0, 59, 0, 4)
        self.assertEqual(_interpret_reference(verse_string7), expected7)

        verse_string8 = "1 Peter 1:1 - 1 : 5"
        expected8 = (59, 0, 0, 59, 0, 4)
        self.assertEqual(_interpret_reference(verse_string8), expected8)

        verse_string9 = "1 Peter 1:1 - 2 peter 1 : 5"
        expected9 = (59, 0, 0, 60, 0, 4)
        self.assertEqual(_interpret_reference(verse_string9), expected9)

        verse_string10 = "1pet1:1 -2 pet 1 : 5"
        expected10 = (59, 0, 0, 60, 0, 4)
        self.assertEqual(_interpret_reference(verse_string10), expected10)

        verse_string11 = "philem 10 - pHiLeM 11"
        expected11 = (56, 0, 9, 56, 0, 10)
        self.assertEqual(_interpret_reference(verse_string11), expected11)

        verse_string12 = "First  Peter -  2  peter  1  :  5"
        expected12 = (59, 0, 0, 60, 0, 4)
        self.assertEqual(_interpret_reference(verse_string12), expected12)

        verse_string13 = "1 Peter 1:1 - 2 : 5"
        expected13 = (59, 0, 0, 59, 1, 4)
        self.assertEqual(_interpret_reference(verse_string13), expected13)

        verse_string14 = "1Peter1:1 - 2 : 5"
        expected14 = (59, 0, 0, 59, 1, 4)
        self.assertEqual(_interpret_reference(verse_string14), expected14)

        verse_string15 = "Obadiah 5 - Jude 20"
        expected15 = (30, 0, 4, 64, 0, 19)
        self.assertEqual(_interpret_reference(verse_string15), expected15)

        verse_string16 = "Obadiah5-Jonah2:2"
        expected16 = (30, 0, 4, 31, 1, 1)
        self.assertEqual(_interpret_reference(verse_string16), expected16)

        verse_string17 = "1 John 1:1 - 2 John 13"
        expected17 = (61, 0, 0, 62, 0, 12)
        self.assertEqual(_interpret_reference(verse_string17), expected17)

    def test_standardize_reference(self) -> None:
        """
        Can reference strings be standardized?
        """
        input1 = (61, 2, 4, 61, 2, 4)
        expected_string1 = "1 John 3:5"
        self.assertEqual(_standardize_reference(*input1), expected_string1)

        input2 = (0, 4, 0, 0, 4, 0)
        expected_string2 = "Genesis 5:1"
        self.assertEqual(_standardize_reference(*input2), expected_string2)

        input3 = (1, 0, 0, 1, 1, 24)
        expected_string3 = "Exodus 1-2"
        self.assertEqual(_standardize_reference(*input3), expected_string3)

        input4 = (59, 0, 0, 60, 0, 4)
        expected_string4 = "1 Peter 1:1 - 2 Peter 1:5"
        self.assertEqual(_standardize_reference(*input4), expected_string4)

        input5 = (18, 0, 0, 19, 30, 30)
        expected_string5 = "Psalms - Proverbs"
        self.assertEqual(_standardize_reference(*input5), expected_string5)

        input6 = (14, 0, 1, 14, 1, 0)
        expected_string6 = "Ezra 1:2-2:1"
        self.assertEqual(_standardize_reference(*input6), expected_string6)

        input7 = (59, 0, 0, 59, 0, 4)
        expected_string7 = "1 Peter 1:1-5"
        self.assertEqual(_standardize_reference(*input7), expected_string7)

        input8 = (59, 0, 0, 59, 0, 4)
        expected_string8 = "1 Peter 1:1-5"
        self.assertEqual(_standardize_reference(*input8), expected_string8)

        input9 = (59, 0, 0, 60, 0, 4)
        expected_string9 = "1 Peter 1:1 - 2 Peter 1:5"
        self.assertEqual(_standardize_reference(*input9), expected_string9)

        input10 = (59, 0, 0, 60, 0, 4)
        expected_string10 = "1 Peter 1:1 - 2 Peter 1:5"
        self.assertEqual(_standardize_reference(*input10), expected_string10)

        input11 = (56, 0, 9, 56, 0, 10)
        expected_string11 = "Philemon 10-11"
        self.assertEqual(_standardize_reference(*input11), expected_string11)

        input12 = (59, 0, 0, 60, 0, 4)
        expected_string12 = "1 Peter 1:1 - 2 Peter 1:5"
        self.assertEqual(_standardize_reference(*input12), expected_string12)

        input13 = (59, 0, 0, 59, 1, 4)
        expected_string13 = "1 Peter 1:1-2:5"
        self.assertEqual(_standardize_reference(*input13), expected_string13)

        input14 = (59, 0, 0, 59, 1, 4)
        expected_string14 = "1 Peter 1:1-2:5"
        self.assertEqual(_standardize_reference(*input14), expected_string14)

        input15 = (30, 0, 4, 64, 0, 19)
        expected_string15 = "Obadiah 5 - Jude 20"
        self.assertEqual(_standardize_reference(*input15), expected_string15)

        input16 = (30, 0, 4, 31, 1, 1)
        expected_string16 = "Obadiah 5 - Jonah 2:2"
        self.assertEqual(_standardize_reference(*input16), expected_string16)

        input17 = (61, 0, 0, 62, 0, 12)
        expected_string17 = "1 John - 2 John"
        self.assertEqual(_standardize_reference(*input17), expected_string17)

    def test_reference_from_string(self) -> None:
        """
        Can verse strings be interpreted?
        """
        verse_string1 = "1 John 3:5"
        expected_ref1 = Reference(verse_string1, 30585, 30585, 61, 61, 2, 2, 4, 4)
        actual_ref1 = reference_from_string(verse_string1)
        self.assertEqual(actual_ref1, expected_ref1)

        verse_string2 = "Genesis 49:2-8"
        expected_ref2 = Reference(verse_string2, 1475, 1481, 0, 0, 48, 48, 1, 7)
        actual_ref2 = reference_from_string(verse_string2)
        self.assertEqual(actual_ref2, expected_ref2)

        verse_string3 = "Esther 3:7-10"
        expected_ref3 = Reference(verse_string3, 12754, 12757, 16, 16, 2, 2, 6, 9)
        actual_ref3 = reference_from_string(verse_string3)
        self.assertEqual(actual_ref3, expected_ref3)

        verse_string4 = "1 Kings 4"
        expected_ref4 = Reference(verse_string4, 8845, 8878, 10, 10, 3, 3, 0, 33)
        actual_ref4 = reference_from_string(verse_string4)
        self.assertEqual(actual_ref4, expected_ref4)

        verse_string5 = "Exodus 3:1-4:3"
        expected_ref5 = Reference(verse_string5, 1580, 1604, 1, 1, 2, 3, 0, 2)
        actual_ref5 = reference_from_string(verse_string5)
        self.assertEqual(actual_ref5, expected_ref5)

        verse_string6 = "Jude 10"
        expected_ref6 = Reference(verse_string6, 30683, 30683, 64, 64, 0, 0, 9, 9)
        actual_ref6 = reference_from_string(verse_string6)
        self.assertEqual(actual_ref6, expected_ref6)

        verse_string7 = "Genesis"
        expected_ref7 = Reference(verse_string7, 0, 1532, 0, 0, 0, 49, 0, 25)
        actual_ref7 = reference_from_string(verse_string7)
        self.assertEqual(actual_ref7, expected_ref7)

        verse_string8 = "Genesis - Leviticus"
        expected_ref8 = Reference(verse_string8, 0, 3604, 0, 2, 0, 26, 0, 33)
        actual_ref8 = reference_from_string(verse_string8)
        self.assertEqual(actual_ref8, expected_ref8)

        verse_string9 = "Exodus 3-4"
        expected_ref9 = Reference(verse_string9, 1580, 1632, 1, 1, 2, 3, 0, 30)
        actual_ref9 = reference_from_string(verse_string9)
        self.assertEqual(actual_ref9, expected_ref9)

        verse_string10 = "Jude 10-11"
        expected_ref10 = Reference(verse_string10, 30683, 30684, 64, 64, 0, 0, 9, 10)
        actual_ref10 = reference_from_string(verse_string10)
        self.assertEqual(actual_ref10, expected_ref10)

        verse_string11 = "Genesis 50 - Exodus 1"
        expected_ref11 = Reference(verse_string11, 1507, 1554, 0, 1, 49, 0, 0, 21)
        actual_ref11 = reference_from_string(verse_string11)
        self.assertEqual(actual_ref11, expected_ref11)

        verse_string12 = "Jude - Revelation 1"
        expected_ref12 = Reference(verse_string12, 30674, 30718, 64, 65, 0, 0, 0, 19)
        actual_ref12 = reference_from_string(verse_string12)
        self.assertEqual(actual_ref12, expected_ref12)

        verse_string13 = "Billy"
        with self.assertRaises(InvalidReference):
            reference_from_string(verse_string13)

        verse_string14 = "Genesis 1:1 - Billy"
        with self.assertRaises(InvalidReference):
            reference_from_string(verse_string14)

        verse_string15 = "Zedekiah 14:7 - Leviticus 1:5"
        with self.assertRaises(InvalidReference):
            reference_from_string(verse_string15)

        verse_string16 = "Zedekiah 14:7 - JimBob 11:109"
        with self.assertRaises(InvalidReference):
            reference_from_string(verse_string16)

        with self.assertRaises(InvalidReference):
            reference_from_string("1 Samuel 1:200")

        with self.assertRaises(InvalidReference):
            reference_from_string("Psalm 151:1")

        with self.assertRaises(InvalidReference):
            reference_from_string("2 Samuel 1:1 - 1 Samuel 1:1")

    def test_reference_from_id(self) -> None:
        # Genesis 1:1
        start_id1 = 0
        expected_ref1 = Reference("Genesis 1:1", start_id1, start_id1, 0, 0, 0, 0, 0, 0)
        actual_ref1 = reference_from_id(start_id=start_id1)
        self.assertEqual(actual_ref1, expected_ref1)

        # Exodus 1:1
        start_id2 = 1533
        expected_ref2 = Reference("Exodus 1:1", start_id2, start_id2, 1, 1, 0, 0, 0, 0)
        actual_ref2 = reference_from_id(start_id=start_id2)
        self.assertEqual(actual_ref2, expected_ref2)

        # Exodus 1:1 - Leviticus 1:1
        start_id3 = 1533
        end_id3 = 2746
        expected_ref3 = Reference("Exodus 1:1 - Leviticus 1:1", start_id3, end_id3, 1, 2, 0, 0, 0, 0)
        actual_ref3 = reference_from_id(start_id=start_id3, end_id=end_id3)
        self.assertEqual(actual_ref3, expected_ref3)

        # Revelation 22:21
        start_id4 = 31102
        expected_ref4 = Reference("Revelation 22:21", start_id4, start_id4, 65, 65, 21, 21, 20, 20)
        actual_ref4 = reference_from_id(start_id=start_id4)
        self.assertEqual(actual_ref4, expected_ref4)

        with self.assertRaises(InvalidReference):
            reference_from_id(start_id=100, end_id=99)

    @skip("Not Yet")
    @patch("scripture_phaser.backend.translations.OfflineAgent.fetch")
    def test_view(self, mock_fetch) -> None:
        """
        Do passages display their content properly?
        """
        translation = "KJV"

        reference = Reference(translation, "1 Peter 1:2 - 1:3")

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

        expected_clean = (
            "Elect according to the foreknowledge of God the Father, "
            + "through sanctification of the Spirit, unto obedience and "
            + "sprinkling of the blood of Jesus Christ: Grace unto you, "
            + "and peace, be multiplied. "
            + "Blessed be the God and Father of our Lord Jesus Christ, which "
            + "according to his abundant mercy hath begotten us again unto "
            + "a lively hope by the resurrection of Jesus Christ from the dead,"
        )

        expected_verse = (
            "[2] Elect according to the foreknowledge of God the Father, "
            + "through sanctification of the Spirit, unto obedience and "
            + "sprinkling of the blood of Jesus Christ: Grace unto you, "
            + "and peace, be multiplied. "
            + "[3] Blessed be the God and Father of our Lord Jesus Christ, which "
            + "according to his abundant mercy hath begotten us again unto "
            + "a lively hope by the resurrection of Jesus Christ from the dead,"
        )

        expected_ref = (
            "Elect according to the foreknowledge of God the Father, "
            + "through sanctification of the Spirit, unto obedience and "
            + "sprinkling of the blood of Jesus Christ: Grace unto you, "
            + "and peace, be multiplied. "
            + "Blessed be the God and Father of our Lord Jesus Christ, which "
            + "according to his abundant mercy hath begotten us again unto "
            + "a lively hope by the resurrection of Jesus Christ from the dead,"
            + " - 1 Peter 1:2-3"
        )

        expected_full = (
            "[2] Elect according to the foreknowledge of God the Father, "
            + "through sanctification of the Spirit, unto obedience and "
            + "sprinkling of the blood of Jesus Christ: Grace unto you, "
            + "and peace, be multiplied. "
            + "[3] Blessed be the God and Father of our Lord Jesus Christ, which "
            + "according to his abundant mercy hath begotten us again unto "
            + "a lively hope by the resurrection of Jesus Christ from the dead,"
            + " - 1 Peter 1:2-3"
        )

        reference.populate()

        self.assertEqual(
            reference.view(include_verse_numbers=False, include_ref=True),
            expected_ref,
        )
        self.assertEqual(
            reference.view(include_verse_numbers=True, include_ref=True),
            expected_full,
        )
        self.assertEqual(
            reference.view(include_verse_numbers=False, include_ref=False),
            expected_clean,
        )
        self.assertEqual(
            reference.view(include_verse_numbers=True, include_ref=False),
            expected_verse,
        )

    @skip("Passage")
    @patch("scripture_phaser.backend.translations.OfflineAgent.fetch")
    def test_get_fast_recitation_ans(self, mock_fetch) -> None:
        """
        Can the Reference fetch the first letter of each word in a passage?
        """
        reference = Reference("KJV", "2 Timothy 3:16-17")

        content = (
            "All scripture is given by inspiration of God, and is profitable "
            + "for doctrine, for reproof, for correction, for instruction in "
            + "righteousness: That the man of God may be perfect, throughly "
            + "furnished unto all good works."
        )
        mock_fetch.return_value = content
        # reference.agent.fetch = MagicMock(return_value=content)

        expected = [
            "A",
            "s",
            "i",
            "g",
            "b",
            "i",
            "o",
            "G",
            "a",
            "i",
            "p",
            "f",
            "d",
            "f",
            "r",
            "f",
            "c",
            "f",
            "i",
            "i",
            "r",
            "T",
            "t",
            "m",
            "o",
            "G",
            "m",
            "b",
            "p",
            "t",
            "f",
            "u",
            "a",
            "g",
            "w",
        ]

        self.assertEqual(
            reference.view_first_letter(include_verse_numbers=False), expected
        )
