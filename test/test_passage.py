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

from unittest.mock import MagicMock
from src.enums import App
from src.verse import Verse
from src.passage import Passage
from src.translations import ESV
from src.exceptions import InvalidReference
from test.test_base import BaseTest


class PassageTests(BaseTest):
    """
    Test the Passage Object
    """
    def test_clean_reference(self):
        """
        Can reference strings be standardized?
        """
        verse_string1 = "1 John 3:5"
        expected_string1 = "One John 3:5"
        actual_string1 = Passage.clean_reference(
            verse_string1,
            for_verse_selection=True
        )
        self.assertEqual(actual_string1, expected_string1)

        verse_string2 = "genesis 5:1"
        expected_string2 = "Genesis 5:1"
        actual_string2 = Passage.clean_reference(
            verse_string2,
            for_verse_selection=True
        )
        self.assertEqual(actual_string2, expected_string2)

        verse_string3 = "exodus 1-2"
        expected_string3 = "Exodus 1 - 2"
        actual_string3 = Passage.clean_reference(
            verse_string3,
            for_verse_selection=True
        )
        self.assertEqual(actual_string3, expected_string3)

        verse_string4 = "First Peter - 2 peter 1 : 5"
        expected_string4 = "One Peter - Two Peter 1:5"
        actual_string4 = Passage.clean_reference(
            verse_string4,
            for_verse_selection=True
        )
        self.assertEqual(actual_string4, expected_string4)

        verse_string5 = "psalm-proverbs"
        expected_string5 = "Psalms - Proverbs"
        actual_string5 = Passage.clean_reference(
            verse_string5,
            for_verse_selection=True
        )
        self.assertEqual(actual_string5, expected_string5)

        verse_string6 = "Ezra 1 : 2-2 : 1"
        expected_string6 = "Ezra 1:2 - 2:1"
        actual_string6 = Passage.clean_reference(
            verse_string6,
            for_verse_selection=True
        )
        self.assertEqual(actual_string6, expected_string6)

        verse_string7 = "1 John 3:5"
        expected_string7 = "1 John 3:5"
        actual_string7 = Passage.clean_reference(
            verse_string7,
            for_verse_selection=False
        )
        self.assertEqual(actual_string7, expected_string7)

        verse_string8 = "First Peter - 2 peter 1 : 5"
        expected_string8 = "1 Peter - 2 Peter 1:5"
        actual_string8 = Passage.clean_reference(
            verse_string8,
            for_verse_selection=False
        )
        self.assertEqual(actual_string8, expected_string8)

    def test_interpret_reference(self):
        """
        Can verse strings be interpreted?
        """
        verse_string1 = "One John 3:5"
        eb1, ec1, ev1, eb2, ec2, ev2 = 61, 2, 4, 61, 2, 4
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string1)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string2 = "Genesis 49:2 - 49:8"
        eb1, ec1, ev1, eb2, ec2, ev2 = 0, 48, 1, 0, 48, 7
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string2)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string3 = "Esther 3:7 - 10"
        eb1, ec1, ev1, eb2, ec2, ev2 = 16, 2, 6, 16, 2, 9
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string3)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string4 = "One Kings 4"
        eb1, ec1, ev1, eb2, ec2, ev2 = 10, 3, 0, 10, 3, 33
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string4)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string5 = "Exodus 3 - 4:3"
        eb1, ec1, ev1, eb2, ec2, ev2 = 1, 2, 0, 1, 3, 2
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string5)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string6 = "Jude 10"
        eb1, ec1, ev1, eb2, ec2, ev2 = 64, 0, 9, 64, 0, 9
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string6)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string7 = "Genesis"
        eb1, ec1, ev1, eb2, ec2, ev2 = 0, 0, 0, 0, 49, 25
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string7)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string8 = "Genesis - Leviticus"
        eb1, ec1, ev1, eb2, ec2, ev2 = 0, 0, 0, 2, 26, 33
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string8)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string9 = "Exodus 3 - 4"
        eb1, ec1, ev1, eb2, ec2, ev2 = 1, 2, 0, 1, 3, 30
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string9)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string10 = "Jude 10 - 11"
        eb1, ec1, ev1, eb2, ec2, ev2 = 64, 0, 9, 64, 0, 10
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string10)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string11 = "Genesis 50 - Exodus 1"
        eb1, ec1, ev1, eb2, ec2, ev2 = 0, 49, 0, 1, 0, 21
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string11)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string12 = "Jude - Revelation 1"
        eb1, ec1, ev1, eb2, ec2, ev2 = 64, 0, 0, 65, 0, 19
        b1, c1, v1, b2, c2, v2 = Passage.interpret_reference(verse_string12)
        self.assertEqual(eb1, b1)
        self.assertEqual(ec1, c1)
        self.assertEqual(ev1, v1)
        self.assertEqual(eb2, b2)
        self.assertEqual(ec2, c2)
        self.assertEqual(ev2, v2)

        verse_string13 = "Billy"
        with self.assertRaises(InvalidReference):
            Passage.interpret_reference(verse_string13)

        verse_string14 = "Genesis 1:1 - Billy"
        with self.assertRaises(InvalidReference):
            Passage.interpret_reference(verse_string14)

        verse_string15 = "Zedekiah 14:7 - Leviticus 1:5"
        with self.assertRaises(InvalidReference):
            Passage.interpret_reference(verse_string15)

        verse_string16 = "Zedekiah 14:7 - JimBob 11:109"
        with self.assertRaises(InvalidReference):
            Passage.interpret_reference(verse_string16)

    def test_reference_to_verses(self):
        """
        Can reference strings be converted to Verse() objects?
        """
        verse_string1 = "One John 3:5"
        actual_verses = Passage.reference_to_verses(verse_string1)
        self.assertEqual(len(actual_verses), 1)

        verse_string2 = "Genesis 49:2 - 49:8"
        actual_verses = Passage.reference_to_verses(verse_string2)
        self.assertEqual(len(actual_verses), 7)

        verse_string3 = "Esther 3:7 - 10"
        actual_verses = Passage.reference_to_verses(verse_string3)
        self.assertEqual(len(actual_verses), 4)

        verse_string4 = "One Kings 4"
        actual_verses = Passage.reference_to_verses(verse_string4)
        self.assertEqual(len(actual_verses), 34)

        verse_string5 = "Exodus 3 - 4:3"
        actual_verses = Passage.reference_to_verses(verse_string5)
        self.assertEqual(len(actual_verses), 25)

        verse_string6 = "Jude 10"
        actual_verses = Passage.reference_to_verses(verse_string6)
        self.assertEqual(len(actual_verses), 1)

        verse_string7 = "Genesis"
        actual_verses = Passage.reference_to_verses(verse_string7)
        self.assertEqual(len(actual_verses), 1533)

        verse_string8 = "Genesis - Leviticus"
        actual_verses = Passage.reference_to_verses(verse_string8)
        self.assertEqual(len(actual_verses), 3605)

        verse_string9 = "Exodus 3 - 4"
        actual_verses = Passage.reference_to_verses(verse_string9)
        self.assertEqual(len(actual_verses), 53)

        verse_string10 = "Jude 10 - 11"
        actual_verses = Passage.reference_to_verses(verse_string10)
        self.assertEqual(len(actual_verses), 2)

        verse_string11 = "Genesis 50 - Exodus 1"
        actual_verses = Passage.reference_to_verses(verse_string11)
        self.assertEqual(len(actual_verses), 48)

        verse_string12 = "Jude - Revelation 1"
        actual_verses = Passage.reference_to_verses(verse_string12)
        self.assertEqual(len(actual_verses), 45)

    def test_validate_verse_pair(self):
        """
        Are invalid verse ranges rejected?
        """
        # Job 1:11
        ref1 = Verse(17, 0, 10)
        # Job 1:12
        ref2 = Verse(17, 0, 11)
        # Job 1:13
        ref3 = Verse(17, 0, 12)
        # Proverbs 30:5
        ref4 = Verse(19, 29, 4)

        self.assertTrue(Passage.validate_verse_pair(ref1, ref1))
        self.assertTrue(Passage.validate_verse_pair(ref1, ref2))
        self.assertTrue(Passage.validate_verse_pair(ref1, ref3))
        self.assertTrue(Passage.validate_verse_pair(ref1, ref4))
        self.assertFalse(Passage.validate_verse_pair(ref2, ref1))
        self.assertTrue(Passage.validate_verse_pair(ref2, ref2))
        self.assertTrue(Passage.validate_verse_pair(ref2, ref3))
        self.assertTrue(Passage.validate_verse_pair(ref2, ref4))
        self.assertFalse(Passage.validate_verse_pair(ref3, ref1))
        self.assertFalse(Passage.validate_verse_pair(ref3, ref2))
        self.assertTrue(Passage.validate_verse_pair(ref3, ref3))
        self.assertTrue(Passage.validate_verse_pair(ref3, ref4))
        self.assertFalse(Passage.validate_verse_pair(ref4, ref1))
        self.assertFalse(Passage.validate_verse_pair(ref4, ref2))
        self.assertFalse(Passage.validate_verse_pair(ref4, ref3))
        self.assertTrue(Passage.validate_verse_pair(ref4, ref4))

    def test_populate(self):
        """
        Can a passage be properly populated?
        """
        reference = "John 1:1 - 1:5"
        translation = ESV()
        passage = Passage(reference, translation)

        mock_api_return = '[1] In the beginning was the Word, and the Word was with ' + \
        'God, and the Word was God. [2] He was in the beginning with God. [3] ' + \
        'All things were made through him, and without him was not any thing ' + \
        'made that was made. [4] In him was life, and the life was the light of ' + \
        'men. [5] The light shines in the darkness, and the darkness has not ' + \
        'overcome it.\n\n'
        passage.translation.agent._fetch = MagicMock(return_value=mock_api_return)

        passage.populate()

        expected_verses = [
            Verse(42, 0, 0, 'In the beginning was the Word, and the Word was with God, and the Word was God.'),
            Verse(42, 0, 1, 'He was in the beginning with God.'),
            Verse(42, 0, 2, 'All things were made through him, and without him was not any thing made that was made.'),
            Verse(42, 0, 3, 'In him was life, and the life was the light of men.'),
            Verse(42, 0, 4, 'The light shines in the darkness, and the darkness has not overcome it.')
        ]

        self.assertEqual(len(expected_verses), len(passage.verses))
        for i in range(len(expected_verses)):
            self.assertTrue(Verse.verse_equal(expected_verses[i], passage.verses[i]))

    def test_show(self):
        """
        Do passages display their content properly?
        """
        reference = "1 Peter 1:2 - 1:3"
        translation = ESV()
        passage = Passage(reference, translation)

        mock_api_return = [
        'according to the foreknowledge of God the Father, in the sanctification of '
        'the Spirit, for obedience to Jesus Christ and for sprinkling with his blood:'
        '\nMay grace and peace be multiplied to you. \n', 'Blessed be the God and Father '
        'of our Lord Jesus Christ! According to his great mercy, he has caused us to be '
        'born again to a living hope through the resurrection of Jesus Christ from the dead,'
        ]

        passage.translation.agent._fetch = MagicMock(return_value=mock_api_return)

        expected_clean = 'according to the foreknowledge of God the Father, ' + \
        'in the sanctification of the Spirit, for obedience to Jesus Christ and ' + \
        'for sprinkling with his blood:\nMay grace and peace be multiplied to ' + \
        'you. \nBlessed be the God and Father of our Lord Jesus Christ! ' + \
        'According to his great mercy, he has caused us to be born again to a ' + \
        'living hope through the resurrection of Jesus Christ from the dead,'

        expected_verse = '[2] according to the foreknowledge of God the Father, ' + \
        'in the sanctification of the Spirit, for obedience to Jesus Christ and ' + \
        'for sprinkling with his blood:\nMay grace and peace be multiplied to ' + \
        'you. \n[3] Blessed be the God and Father of our Lord Jesus Christ! ' + \
        'According to his great mercy, he has caused us to be born again to a ' + \
        'living hope through the resurrection of Jesus Christ from the dead,'

        expected_ref = 'according to the foreknowledge of God the Father, ' + \
        'in the sanctification of the Spirit, for obedience to Jesus Christ and ' + \
        'for sprinkling with his blood:\nMay grace and peace be multiplied to ' + \
        'you. \nBlessed be the God and Father of our Lord Jesus Christ! ' + \
        'According to his great mercy, he has caused us to be born again to a ' + \
        'living hope through the resurrection of Jesus Christ from the dead, ' + \
        '- 1 Peter 1:2 - 1:3'

        expected_full = '[2] according to the foreknowledge of God the Father, ' + \
        'in the sanctification of the Spirit, for obedience to Jesus Christ and ' + \
        'for sprinkling with his blood:\nMay grace and peace be multiplied to ' + \
        'you. \n[3] Blessed be the God and Father of our Lord Jesus Christ! ' + \
        'According to his great mercy, he has caused us to be born again to a ' + \
        'living hope through the resurrection of Jesus Christ from the dead, ' + \
        '- 1 Peter 1:2 - 1:3'

        passage.populate()

        self.assertEqual(passage.show(), expected_clean)
        self.assertEqual(passage.show(with_verse=True), expected_verse)
        self.assertEqual(passage.show(with_ref=True), expected_ref)
        self.assertEqual(passage.show(with_verse=True, with_ref=True), expected_full)


if __name__ == "__main__":
    import unittest
    unittest.main()
