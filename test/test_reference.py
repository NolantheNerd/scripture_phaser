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

from unittest.mock import patch
from test.test_base import BaseTest
from scripture_phaser.backend.reference import Reference
from scripture_phaser.backend.exceptions import InvalidReference


class ReferenceTests(BaseTest):
    """
    Test the Reference Object
    """

    def test_standardize_reference(self) -> None:
        """
        Can reference strings be standardized?
        """
        translation = "KJV"

        verse_string1 = "1 John 3:5"
        expected_string1 = "1 John 3:5"
        ref1 = Reference(translation, verse_string1)
        self.assertEqual(ref1.ref_str, expected_string1)

        verse_string2 = "genesis 5:1"
        expected_string2 = "Genesis 5:1"
        ref2 = Reference(translation, verse_string2)
        self.assertEqual(ref2.ref_str, expected_string2)

        verse_string3 = "exodus 1 -   2"
        expected_string3 = "Exodus 1:1-2:25"
        ref3 = Reference(translation, verse_string3)
        self.assertEqual(ref3.ref_str, expected_string3)

        verse_string4 = "First Peter - 2 peter 1 : 5"
        expected_string4 = "1 Peter 1:1 - 2 Peter 1:5"
        ref4 = Reference(translation, verse_string4)
        self.assertEqual(ref4.ref_str, expected_string4)

        verse_string5 = "psalm-proverbs"
        expected_string5 = "Psalms 1:1 - Proverbs 31:31"
        ref5 = Reference(translation, verse_string5)
        self.assertEqual(ref5.ref_str, expected_string5)

        verse_string6 = "Ezra 1 : 2-2 : 1"
        expected_string6 = "Ezra 1:2-2:1"
        ref6 = Reference(translation, verse_string6)
        self.assertEqual(ref6.ref_str, expected_string6)

        verse_string7 = "First Peter - 2 peter 1 : 5"
        expected_string7 = "1 Peter 1:1 - 2 Peter 1:5"
        ref7 = Reference(translation, verse_string7)
        self.assertEqual(ref7.ref_str, expected_string7)

        verse_string8 = "First Peter 1:1 - 1 peter 1 : 5"
        expected_string8 = "1 Peter 1:1-5"
        ref8 = Reference(translation, verse_string8)
        self.assertEqual(ref8.ref_str, expected_string8)

        verse_string9 = "1 Peter 1:1 - 1 : 5"
        expected_string9 = "1 Peter 1:1-5"
        ref9 = Reference(translation, verse_string9)
        self.assertEqual(ref9.ref_str, expected_string9)

        verse_string10 = "1 Peter 1:1 - 2 peter 1 : 5"
        expected_string10 = "1 Peter 1:1 - 2 Peter 1:5"
        ref10 = Reference(translation, verse_string10)
        self.assertEqual(ref10.ref_str, expected_string10)

        verse_string11 = "1pet1:1 -2 pet 1 : 5"
        expected_string11 = "1 Peter 1:1 - 2 Peter 1:5"
        ref11 = Reference(translation, verse_string11)
        self.assertEqual(ref11.ref_str, expected_string11)

        verse_string12 = "philem 10 - pHiLeM 11"
        expected_string12 = "Philemon 10-11"
        ref12 = Reference(translation, verse_string12)
        self.assertEqual(ref12.ref_str, expected_string12)

        verse_string13 = "First  Peter -  2  peter  1  :  5"
        expected_string13 = "1 Peter 1:1 - 2 Peter 1:5"
        ref13 = Reference(translation, verse_string13)
        self.assertEqual(ref13.ref_str, expected_string13)

        verse_string14 = "1 Peter 1:1 - 2 : 5"
        expected_string14 = "1 Peter 1:1-2:5"
        ref14 = Reference(translation, verse_string14)
        self.assertEqual(ref14.ref_str, expected_string14)

        verse_string15 = "1Peter1:1 - 2 : 5"
        expected_string15 = "1 Peter 1:1-2:5"
        ref15 = Reference(translation, verse_string15)
        self.assertEqual(ref15.ref_str, expected_string15)

        verse_string16 = "Obadiah 5 - Jude 20"
        expected_string16 = "Obadiah 5 - Jude 20"
        ref16 = Reference(translation, verse_string16)
        self.assertEqual(ref16.ref_str, expected_string16)

        verse_string17 = "Obadiah5-Jonah2:2"
        expected_string17 = "Obadiah 5 - Jonah 2:2"
        ref17 = Reference(translation, verse_string17)
        self.assertEqual(ref17.ref_str, expected_string17)

        verse_string18 = "1 John 1:1 - 2 John 13"
        expected_string18 = "1 John 1:1 - 2 John 13"
        ref18 = Reference(translation, verse_string18)
        self.assertEqual(ref18.ref_str, expected_string18)

    def test_interpret_reference(self) -> None:
        """
        Can verse strings be interpreted?
        """
        translation = "KJV"

        verse_string1 = "1 John 3:5"
        eb1, ec1, ev1, eb2, ec2, ev2 = 61, 2, 4, 61, 2, 4
        ref1 = Reference(translation, verse_string1)
        self.assertEqual(eb1, ref1.book_start)
        self.assertEqual(ec1, ref1.chapter_start)
        self.assertEqual(ev1, ref1.verse_start)
        self.assertEqual(eb2, ref1.book_end)
        self.assertEqual(ec2, ref1.chapter_end)
        self.assertEqual(ev2, ref1.verse_end)

        verse_string2 = "Genesis 49:2 - 49:8"
        eb1, ec1, ev1, eb2, ec2, ev2 = 0, 48, 1, 0, 48, 7
        ref2 = Reference(translation, verse_string2)
        self.assertEqual(eb1, ref2.book_start)
        self.assertEqual(ec1, ref2.chapter_start)
        self.assertEqual(ev1, ref2.verse_start)
        self.assertEqual(eb2, ref2.book_end)
        self.assertEqual(ec2, ref2.chapter_end)
        self.assertEqual(ev2, ref2.verse_end)

        verse_string3 = "Esther 3:7 - 10"
        eb1, ec1, ev1, eb2, ec2, ev2 = 16, 2, 6, 16, 2, 9
        ref3 = Reference(translation, verse_string3)
        self.assertEqual(eb1, ref3.book_start)
        self.assertEqual(ec1, ref3.chapter_start)
        self.assertEqual(ev1, ref3.verse_start)
        self.assertEqual(eb2, ref3.book_end)
        self.assertEqual(ec2, ref3.chapter_end)
        self.assertEqual(ev2, ref3.verse_end)

        verse_string4 = "1 Kings 4"
        eb1, ec1, ev1, eb2, ec2, ev2 = 10, 3, 0, 10, 3, 33
        ref4 = Reference(translation, verse_string4)
        self.assertEqual(eb1, ref4.book_start)
        self.assertEqual(ec1, ref4.chapter_start)
        self.assertEqual(ev1, ref4.verse_start)
        self.assertEqual(eb2, ref4.book_end)
        self.assertEqual(ec2, ref4.chapter_end)
        self.assertEqual(ev2, ref4.verse_end)

        verse_string5 = "Exodus 3 - 4:3"
        eb1, ec1, ev1, eb2, ec2, ev2 = 1, 2, 0, 1, 3, 2
        ref5 = Reference(translation, verse_string5)
        self.assertEqual(eb1, ref5.book_start)
        self.assertEqual(ec1, ref5.chapter_start)
        self.assertEqual(ev1, ref5.verse_start)
        self.assertEqual(eb2, ref5.book_end)
        self.assertEqual(ec2, ref5.chapter_end)
        self.assertEqual(ev2, ref5.verse_end)

        verse_string6 = "Jude 10"
        eb1, ec1, ev1, eb2, ec2, ev2 = 64, 0, 9, 64, 0, 9
        ref6 = Reference(translation, verse_string6)
        self.assertEqual(eb1, ref6.book_start)
        self.assertEqual(ec1, ref6.chapter_start)
        self.assertEqual(ev1, ref6.verse_start)
        self.assertEqual(eb2, ref6.book_end)
        self.assertEqual(ec2, ref6.chapter_end)
        self.assertEqual(ev2, ref6.verse_end)

        verse_string7 = "Genesis"
        eb1, ec1, ev1, eb2, ec2, ev2 = 0, 0, 0, 0, 49, 25
        ref7 = Reference(translation, verse_string7)
        self.assertEqual(eb1, ref7.book_start)
        self.assertEqual(ec1, ref7.chapter_start)
        self.assertEqual(ev1, ref7.verse_start)
        self.assertEqual(eb2, ref7.book_end)
        self.assertEqual(ec2, ref7.chapter_end)
        self.assertEqual(ev2, ref7.verse_end)

        verse_string8 = "Genesis - Leviticus"
        eb1, ec1, ev1, eb2, ec2, ev2 = 0, 0, 0, 2, 26, 33
        ref8 = Reference(translation, verse_string8)
        self.assertEqual(eb1, ref8.book_start)
        self.assertEqual(ec1, ref8.chapter_start)
        self.assertEqual(ev1, ref8.verse_start)
        self.assertEqual(eb2, ref8.book_end)
        self.assertEqual(ec2, ref8.chapter_end)
        self.assertEqual(ev2, ref8.verse_end)

        verse_string9 = "Exodus 3 - 4"
        eb1, ec1, ev1, eb2, ec2, ev2 = 1, 2, 0, 1, 3, 30
        ref9 = Reference(translation, verse_string9)
        self.assertEqual(eb1, ref9.book_start)
        self.assertEqual(ec1, ref9.chapter_start)
        self.assertEqual(ev1, ref9.verse_start)
        self.assertEqual(eb2, ref9.book_end)
        self.assertEqual(ec2, ref9.chapter_end)
        self.assertEqual(ev2, ref9.verse_end)

        verse_string10 = "Jude 10 - 11"
        eb1, ec1, ev1, eb2, ec2, ev2 = 64, 0, 9, 64, 0, 10
        ref10 = Reference(translation, verse_string10)
        self.assertEqual(eb1, ref10.book_start)
        self.assertEqual(ec1, ref10.chapter_start)
        self.assertEqual(ev1, ref10.verse_start)
        self.assertEqual(eb2, ref10.book_end)
        self.assertEqual(ec2, ref10.chapter_end)
        self.assertEqual(ev2, ref10.verse_end)

        verse_string11 = "Genesis 50 - Exodus 1"
        eb1, ec1, ev1, eb2, ec2, ev2 = 0, 49, 0, 1, 0, 21
        ref11 = Reference(translation, verse_string11)
        self.assertEqual(eb1, ref11.book_start)
        self.assertEqual(ec1, ref11.chapter_start)
        self.assertEqual(ev1, ref11.verse_start)
        self.assertEqual(eb2, ref11.book_end)
        self.assertEqual(ec2, ref11.chapter_end)
        self.assertEqual(ev2, ref11.verse_end)

        verse_string12 = "Jude - Revelation 1"
        eb1, ec1, ev1, eb2, ec2, ev2 = 64, 0, 0, 65, 0, 19
        ref12 = Reference(translation, verse_string12)
        self.assertEqual(eb1, ref12.book_start)
        self.assertEqual(ec1, ref12.chapter_start)
        self.assertEqual(ev1, ref12.verse_start)
        self.assertEqual(eb2, ref12.book_end)
        self.assertEqual(ec2, ref12.chapter_end)
        self.assertEqual(ev2, ref12.verse_end)

        verse_string13 = "Billy"
        with self.assertRaises(InvalidReference):
            Reference(translation, verse_string13)

        verse_string14 = "Genesis 1:1 - Billy"
        with self.assertRaises(InvalidReference):
            Reference(translation, verse_string14)

        verse_string15 = "Zedekiah 14:7 - Leviticus 1:5"
        with self.assertRaises(InvalidReference):
            Reference(translation, verse_string15)

        verse_string16 = "Zedekiah 14:7 - JimBob 11:109"
        with self.assertRaises(InvalidReference):
            Reference(translation, verse_string16)

    def test_interpret_id(self) -> None:
        translation = "KJV"

        # Genesis 1:1
        start_id1 = 0
        eb1, ec1, ev1, eb2, ec2, ev2 = 0, 0, 0, 0, 0, 0
        ref1 = Reference(translation, id=start_id1)
        self.assertEqual(eb1, ref1.book_start)
        self.assertEqual(ec1, ref1.chapter_start)
        self.assertEqual(ev1, ref1.verse_start)
        self.assertEqual(eb2, ref1.book_end)
        self.assertEqual(ec2, ref1.chapter_end)
        self.assertEqual(ev2, ref1.verse_end)

        # Exodus 1:1
        start_id2 = 1533
        eb1, ec1, ev1, eb2, ec2, ev2 = 1, 0, 0, 1, 0, 0
        ref2 = Reference(translation, id=start_id2)
        self.assertEqual(eb1, ref2.book_start)
        self.assertEqual(ec1, ref2.chapter_start)
        self.assertEqual(ev1, ref2.verse_start)
        self.assertEqual(eb2, ref2.book_end)
        self.assertEqual(ec2, ref2.chapter_end)
        self.assertEqual(ev2, ref2.verse_end)

        # Exodus 1:1 - Leviticus 1:1
        start_id3 = 1533
        end_id3 = 2746
        eb1, ec1, ev1, eb2, ec2, ev2 = 1, 0, 0, 2, 0, 0
        ref3 = Reference(translation, id=start_id3, end_id=end_id3)
        self.assertEqual(eb1, ref3.book_start)
        self.assertEqual(ec1, ref3.chapter_start)
        self.assertEqual(ev1, ref3.verse_start)
        self.assertEqual(eb2, ref3.book_end)
        self.assertEqual(ec2, ref3.chapter_end)
        self.assertEqual(ev2, ref3.verse_end)

        # Revelation 22:21
        start_id4 = 31102
        eb1, ec1, ev1, eb2, ec2, ev2 = 65, 21, 20, 65, 21, 20
        ref4 = Reference(translation, id=start_id4)
        self.assertEqual(eb1, ref4.book_start)
        self.assertEqual(ec1, ref4.chapter_start)
        self.assertEqual(ev1, ref4.verse_start)
        self.assertEqual(eb2, ref4.book_end)
        self.assertEqual(ec2, ref4.chapter_end)
        self.assertEqual(ev2, ref4.verse_end)

        with self.assertRaises(InvalidReference):
            Reference(translation, id=100, end_id=99)

        with self.assertRaises(InvalidReference):
            Reference(translation, "1 Samuel 1:200")

        with self.assertRaises(InvalidReference):
            Reference(translation, "Psalm 151:1")

        with self.assertRaises(InvalidReference):
            Reference(translation, "2 Samuel 1:1 - 1 Samuel 1:1")

    @patch("scripture_phaser.backend.agents.OfflineAgent.fetch")
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

    @patch("scripture_phaser.backend.agents.OfflineAgent.fetch")
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
