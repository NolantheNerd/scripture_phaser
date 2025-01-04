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
from scripture_phaser.backend.reference import (
    Reference,
    PassageID,
    VerseTriplet,
    id_to_reference,
    string_to_reference,
    _interpret_reference,
    _standardize_reference,
)
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
        expected_first_verse1 = VerseTriplet(61, 2, 4)
        expected_last_verse1 = VerseTriplet(61, 2, 4)
        self.assertEqual(
            _interpret_reference(verse_string1),
            (expected_first_verse1, expected_last_verse1),
        )

        verse_string2 = "genesis 5:1"
        expected_first_verse2 = VerseTriplet(0, 4, 0)
        expected_last_verse2 = VerseTriplet(0, 4, 0)
        self.assertEqual(
            _interpret_reference(verse_string2),
            (expected_first_verse2, expected_last_verse2),
        )

        verse_string3 = "exodus 1 -   2"
        expected_first_verse3 = VerseTriplet(1, 0, 0)
        expected_last_verse3 = VerseTriplet(1, 1, 24)
        self.assertEqual(
            _interpret_reference(verse_string3),
            (expected_first_verse3, expected_last_verse3),
        )

        verse_string4 = "First Peter - 2 peter 1 : 5"
        expected_first_verse4 = VerseTriplet(59, 0, 0)
        expected_last_verse4 = VerseTriplet(60, 0, 4)
        self.assertEqual(
            _interpret_reference(verse_string4),
            (expected_first_verse4, expected_last_verse4),
        )

        verse_string5 = "psalm-proverbs"
        expected_first_verse5 = VerseTriplet(18, 0, 0)
        expected_last_verse5 = VerseTriplet(19, 30, 30)
        self.assertEqual(
            _interpret_reference(verse_string5),
            (expected_first_verse5, expected_last_verse5),
        )

        verse_string6 = "Ezra 1 : 2-2 : 1"
        expected_first_verse6 = VerseTriplet(14, 0, 1)
        expected_last_verse6 = VerseTriplet(14, 1, 0)
        self.assertEqual(
            _interpret_reference(verse_string6),
            (expected_first_verse6, expected_last_verse6),
        )

        verse_string7 = "First Peter 1:1 - 1 peter 1 : 5"
        expected_first_verse7 = VerseTriplet(59, 0, 0)
        expected_last_verse7 = VerseTriplet(59, 0, 4)
        self.assertEqual(
            _interpret_reference(verse_string7),
            (expected_first_verse7, expected_last_verse7),
        )

        verse_string8 = "1 Peter 1:1 - 1 : 5"
        expected_first_verse8 = VerseTriplet(59, 0, 0)
        expected_last_verse8 = VerseTriplet(59, 0, 4)
        self.assertEqual(
            _interpret_reference(verse_string8),
            (expected_first_verse8, expected_last_verse8),
        )

        verse_string9 = "1 Peter 1:1 - 2 peter 1 : 5"
        expected_first_verse9 = VerseTriplet(59, 0, 0)
        expected_last_verse9 = VerseTriplet(60, 0, 4)
        self.assertEqual(
            _interpret_reference(verse_string9),
            (expected_first_verse9, expected_last_verse9),
        )

        verse_string10 = "1pet1:1 -2 pet 1 : 5"
        expected_first_verse10 = VerseTriplet(59, 0, 0)
        expected_last_verse10 = VerseTriplet(60, 0, 4)
        self.assertEqual(
            _interpret_reference(verse_string10),
            (expected_first_verse10, expected_last_verse10),
        )

        verse_string11 = "philem 10 - pHiLeM 11"
        expected_first_verse11 = VerseTriplet(56, 0, 9)
        expected_last_verse11 = VerseTriplet(56, 0, 10)
        self.assertEqual(
            _interpret_reference(verse_string11),
            (expected_first_verse11, expected_last_verse11),
        )

        verse_string12 = "First  Peter -  2  peter  1  :  5"
        expected_first_verse12 = VerseTriplet(59, 0, 0)
        expected_last_verse12 = VerseTriplet(60, 0, 4)
        self.assertEqual(
            _interpret_reference(verse_string12),
            (expected_first_verse12, expected_last_verse12),
        )

        verse_string13 = "1 Peter 1:1 - 2 : 5"
        expected_first_verse13 = VerseTriplet(59, 0, 0)
        expected_last_verse13 = VerseTriplet(59, 1, 4)
        self.assertEqual(
            _interpret_reference(verse_string13),
            (expected_first_verse13, expected_last_verse13),
        )

        verse_string14 = "1Peter1:1 - 2 : 5"
        expected_first_verse14 = VerseTriplet(59, 0, 0)
        expected_last_verse14 = VerseTriplet(59, 1, 4)
        self.assertEqual(
            _interpret_reference(verse_string14),
            (expected_first_verse14, expected_last_verse14),
        )

        verse_string15 = "Obadiah 5 - Jude 20"
        expected_first_verse15 = VerseTriplet(30, 0, 4)
        expected_last_verse15 = VerseTriplet(64, 0, 19)
        self.assertEqual(
            _interpret_reference(verse_string15),
            (expected_first_verse15, expected_last_verse15),
        )

        verse_string16 = "Obadiah5-Jonah2:2"
        expected_first_verse16 = VerseTriplet(30, 0, 4)
        expected_last_verse16 = VerseTriplet(31, 1, 1)
        self.assertEqual(
            _interpret_reference(verse_string16),
            (expected_first_verse16, expected_last_verse16),
        )

        verse_string17 = "1 John 1:1 - 2 John 13"
        expected_first_verse17 = VerseTriplet(61, 0, 0)
        expected_last_verse17 = VerseTriplet(62, 0, 12)
        self.assertEqual(
            _interpret_reference(verse_string17),
            (expected_first_verse17, expected_last_verse17),
        )

    def test_standardize_reference(self) -> None:
        """
        Can reference strings be standardized?
        """
        first_verse1 = VerseTriplet(61, 2, 4)
        last_verse1 = VerseTriplet(61, 2, 4)
        expected_string1 = "1 John 3:5"
        self.assertEqual(
            _standardize_reference(first_verse1, last_verse1), expected_string1
        )

        first_verse2 = VerseTriplet(0, 4, 0)
        last_verse2 = VerseTriplet(0, 4, 0)
        expected_string2 = "Genesis 5:1"
        self.assertEqual(
            _standardize_reference(first_verse2, last_verse2), expected_string2
        )

        first_verse3 = VerseTriplet(1, 0, 0)
        last_verse3 = VerseTriplet(1, 1, 24)
        expected_string3 = "Exodus 1-2"
        self.assertEqual(
            _standardize_reference(first_verse3, last_verse3), expected_string3
        )

        first_verse4 = VerseTriplet(59, 0, 0)
        last_verse4 = VerseTriplet(60, 0, 4)
        expected_string4 = "1 Peter 1:1 - 2 Peter 1:5"
        self.assertEqual(
            _standardize_reference(first_verse4, last_verse4), expected_string4
        )

        first_verse5 = VerseTriplet(18, 0, 0)
        last_verse5 = VerseTriplet(19, 30, 30)
        expected_string5 = "Psalms - Proverbs"
        self.assertEqual(
            _standardize_reference(first_verse5, last_verse5), expected_string5
        )

        first_verse6 = VerseTriplet(14, 0, 1)
        last_verse6 = VerseTriplet(14, 1, 0)
        expected_string6 = "Ezra 1:2-2:1"
        self.assertEqual(
            _standardize_reference(first_verse6, last_verse6), expected_string6
        )

        first_verse7 = VerseTriplet(59, 0, 0)
        last_verse7 = VerseTriplet(59, 0, 4)
        expected_string7 = "1 Peter 1:1-5"
        self.assertEqual(
            _standardize_reference(first_verse7, last_verse7), expected_string7
        )

        first_verse8 = VerseTriplet(59, 0, 0)
        last_verse8 = VerseTriplet(59, 0, 4)
        expected_string8 = "1 Peter 1:1-5"
        self.assertEqual(
            _standardize_reference(first_verse8, last_verse8), expected_string8
        )

        first_verse9 = VerseTriplet(59, 0, 0)
        last_verse9 = VerseTriplet(60, 0, 4)
        expected_string9 = "1 Peter 1:1 - 2 Peter 1:5"
        self.assertEqual(
            _standardize_reference(first_verse9, last_verse9), expected_string9
        )

        first_verse10 = VerseTriplet(59, 0, 0)
        last_verse10 = VerseTriplet(60, 0, 4)
        expected_string10 = "1 Peter 1:1 - 2 Peter 1:5"
        self.assertEqual(
            _standardize_reference(first_verse10, last_verse10), expected_string10
        )

        first_verse11 = VerseTriplet(56, 0, 9)
        last_verse11 = VerseTriplet(56, 0, 10)
        expected_string11 = "Philemon 10-11"
        self.assertEqual(
            _standardize_reference(first_verse11, last_verse11), expected_string11
        )

        first_verse12 = VerseTriplet(59, 0, 0)
        last_verse12 = VerseTriplet(60, 0, 4)
        expected_string12 = "1 Peter 1:1 - 2 Peter 1:5"
        self.assertEqual(
            _standardize_reference(first_verse12, last_verse12), expected_string12
        )

        first_verse13 = VerseTriplet(59, 0, 0)
        last_verse13 = VerseTriplet(59, 1, 4)
        expected_string13 = "1 Peter 1:1-2:5"
        self.assertEqual(
            _standardize_reference(first_verse13, last_verse13), expected_string13
        )

        first_verse14 = VerseTriplet(59, 0, 0)
        last_verse14 = VerseTriplet(59, 1, 4)
        expected_string14 = "1 Peter 1:1-2:5"
        self.assertEqual(
            _standardize_reference(first_verse14, last_verse14), expected_string14
        )

        first_verse15 = VerseTriplet(30, 0, 4)
        last_verse15 = VerseTriplet(64, 0, 19)
        expected_string15 = "Obadiah 5 - Jude 20"
        self.assertEqual(
            _standardize_reference(first_verse15, last_verse15), expected_string15
        )

        first_verse16 = VerseTriplet(30, 0, 4)
        last_verse16 = VerseTriplet(31, 1, 1)
        expected_string16 = "Obadiah 5 - Jonah 2:2"
        self.assertEqual(
            _standardize_reference(first_verse16, last_verse16), expected_string16
        )

        first_verse17 = VerseTriplet(61, 0, 0)
        last_verse17 = VerseTriplet(62, 0, 12)
        expected_string17 = "1 John - 2 John"
        self.assertEqual(
            _standardize_reference(first_verse17, last_verse17), expected_string17
        )

    def test_string_to_reference(self) -> None:
        """
        Can verse strings be interpreted?
        """
        verse_string1 = "1 John 3:5"
        expected_ref1 = Reference(
            verse_string1,
            PassageID(30585, 30585),
            VerseTriplet(61, 2, 4),
            VerseTriplet(61, 2, 4),
        )
        actual_ref1 = string_to_reference(verse_string1)
        self.assertEqual(actual_ref1, expected_ref1)

        verse_string2 = "Genesis 49:2-8"
        expected_ref2 = Reference(
            verse_string2,
            PassageID(1475, 1481),
            VerseTriplet(0, 48, 1),
            VerseTriplet(0, 48, 7),
        )
        actual_ref2 = string_to_reference(verse_string2)
        self.assertEqual(actual_ref2, expected_ref2)

        verse_string3 = "Esther 3:7-10"
        expected_ref3 = Reference(
            verse_string3,
            PassageID(12754, 12757),
            VerseTriplet(16, 2, 6),
            VerseTriplet(16, 2, 9),
        )
        actual_ref3 = string_to_reference(verse_string3)
        self.assertEqual(actual_ref3, expected_ref3)

        verse_string4 = "1 Kings 4"
        expected_ref4 = Reference(
            verse_string4,
            PassageID(8845, 8878),
            VerseTriplet(10, 3, 0),
            VerseTriplet(10, 3, 33),
        )
        actual_ref4 = string_to_reference(verse_string4)
        self.assertEqual(actual_ref4, expected_ref4)

        verse_string5 = "Exodus 3:1-4:3"
        expected_ref5 = Reference(
            verse_string5,
            PassageID(1580, 1604),
            VerseTriplet(1, 2, 0),
            VerseTriplet(1, 3, 2),
        )
        actual_ref5 = string_to_reference(verse_string5)
        self.assertEqual(actual_ref5, expected_ref5)

        verse_string6 = "Jude 10"
        expected_ref6 = Reference(
            verse_string6,
            PassageID(30683, 30683),
            VerseTriplet(64, 0, 9),
            VerseTriplet(64, 0, 9),
        )
        actual_ref6 = string_to_reference(verse_string6)
        self.assertEqual(actual_ref6, expected_ref6)

        verse_string7 = "Genesis"
        expected_ref7 = Reference(
            verse_string7,
            PassageID(0, 1532),
            VerseTriplet(0, 0, 0),
            VerseTriplet(0, 49, 25),
        )
        actual_ref7 = string_to_reference(verse_string7)
        self.assertEqual(actual_ref7, expected_ref7)

        verse_string8 = "Genesis - Leviticus"
        expected_ref8 = Reference(
            verse_string8,
            PassageID(0, 3604),
            VerseTriplet(0, 0, 0),
            VerseTriplet(2, 26, 33),
        )
        actual_ref8 = string_to_reference(verse_string8)
        self.assertEqual(actual_ref8, expected_ref8)

        verse_string9 = "Exodus 3-4"
        expected_ref9 = Reference(
            verse_string9,
            PassageID(1580, 1632),
            VerseTriplet(1, 2, 0),
            VerseTriplet(1, 3, 30),
        )
        actual_ref9 = string_to_reference(verse_string9)
        self.assertEqual(actual_ref9, expected_ref9)

        verse_string10 = "Jude 10-11"
        expected_ref10 = Reference(
            verse_string10,
            PassageID(30683, 30684),
            VerseTriplet(64, 0, 9),
            VerseTriplet(64, 0, 10),
        )
        actual_ref10 = string_to_reference(verse_string10)
        self.assertEqual(actual_ref10, expected_ref10)

        verse_string11 = "Genesis 50 - Exodus 1"
        expected_ref11 = Reference(
            verse_string11,
            PassageID(1507, 1554),
            VerseTriplet(0, 49, 0),
            VerseTriplet(1, 0, 21),
        )
        actual_ref11 = string_to_reference(verse_string11)
        self.assertEqual(actual_ref11, expected_ref11)

        verse_string12 = "Jude - Revelation 1"
        expected_ref12 = Reference(
            verse_string12,
            PassageID(30674, 30718),
            VerseTriplet(64, 0, 0),
            VerseTriplet(65, 0, 19),
        )
        actual_ref12 = string_to_reference(verse_string12)
        self.assertEqual(actual_ref12, expected_ref12)

        verse_string13 = "Billy"
        with self.assertRaises(InvalidReference):
            string_to_reference(verse_string13)

        verse_string14 = "Genesis 1:1 - Billy"
        with self.assertRaises(InvalidReference):
            string_to_reference(verse_string14)

        verse_string15 = "Zedekiah 14:7 - Leviticus 1:5"
        with self.assertRaises(InvalidReference):
            string_to_reference(verse_string15)

        verse_string16 = "Zedekiah 14:7 - JimBob 11:109"
        with self.assertRaises(InvalidReference):
            string_to_reference(verse_string16)

        with self.assertRaises(InvalidReference):
            string_to_reference("1 Samuel 1:200")

        with self.assertRaises(InvalidReference):
            string_to_reference("Psalm 151:1")

        with self.assertRaises(InvalidReference):
            string_to_reference("2 Samuel 1:1 - 1 Samuel 1:1")

    def test_id_to_reference(self) -> None:
        """
        Can a reference be created from an id?
        """
        # Genesis 1:1
        start_id1 = 0
        expected_ref1 = Reference(
            "Genesis 1:1",
            PassageID(start_id1, start_id1),
            VerseTriplet(0, 0, 0),
            VerseTriplet(0, 0, 0),
        )
        actual_ref1 = id_to_reference(start_id=start_id1)
        self.assertEqual(actual_ref1, expected_ref1)

        # Exodus 1:1
        start_id2 = 1533
        expected_ref2 = Reference(
            "Exodus 1:1",
            PassageID(start_id2, start_id2),
            VerseTriplet(1, 0, 0),
            VerseTriplet(1, 0, 0),
        )
        actual_ref2 = id_to_reference(start_id=start_id2)
        self.assertEqual(actual_ref2, expected_ref2)

        # Exodus 1:1 - Leviticus 1:1
        start_id3 = 1533
        end_id3 = 2746
        expected_ref3 = Reference(
            "Exodus 1:1 - Leviticus 1:1",
            PassageID(start_id3, end_id3),
            VerseTriplet(1, 0, 0),
            VerseTriplet(2, 0, 0),
        )
        actual_ref3 = id_to_reference(start_id=start_id3, end_id=end_id3)
        self.assertEqual(actual_ref3, expected_ref3)

        # Revelation 22:21
        start_id4 = 31102
        expected_ref4 = Reference(
            "Revelation 22:21",
            PassageID(start_id4, start_id4),
            VerseTriplet(65, 21, 20),
            VerseTriplet(65, 21, 20),
        )
        actual_ref4 = id_to_reference(start_id=start_id4)
        self.assertEqual(actual_ref4, expected_ref4)

        with self.assertRaises(InvalidReference):
            id_to_reference(start_id=100, end_id=99)
