# scripture_phaser helps you to memorize the Bible.
# Copyright (C) 2023-2024 Nolan McMahon
#
# This file is part of scripture_phaser.
#
# scripture_phaser is licensed under the terms of the BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
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
from src.reference import Reference
from src.exceptions import InvalidReference
from test.test_base import BaseTest


class PassageTests(BaseTest):
    """
    Test the Passage Object
    """
    def test_reference_to_verses(self):
        """
        Can reference strings be converted to Verse() objects?
        """
        passage1 = Passage(Reference("1 John 3:5"), "NIV")
        self.assertEqual(len(passage1.verses), 1)

        passage2 = Passage(Reference("Genesis 49:2 - 49:8"), "NIV")
        self.assertEqual(len(passage2.verses), 7)

        passage3 = Passage(Reference("Esther 3:7 - 10"), "NIV")
        self.assertEqual(len(passage3.verses), 4)

        passage4 = Passage(Reference("1 Kings 4"), "NIV")
        self.assertEqual(len(passage4.verses), 34)

        passage5 = Passage(Reference("Exodus 3 - 4:3"), "NIV")
        self.assertEqual(len(passage5.verses), 25)

        passage6 = Passage(Reference("Jude 10"), "NIV")
        self.assertEqual(len(passage6.verses), 1)

        passage7 = Passage(Reference("Genesis"), "NIV")
        self.assertEqual(len(passage7.verses), 1533)

        passage8 = Passage(Reference("Genesis - Leviticus"), "NIV")
        self.assertEqual(len(passage8.verses), 3605)

        passage9 = Passage(Reference("Exodus 3 - 4"), "NIV")
        self.assertEqual(len(passage9.verses), 53)

        passage10 = Passage(Reference("Jude 10 - 11"), "NIV")
        self.assertEqual(len(passage10.verses), 2)

        passage11 = Passage(Reference("Genesis 50 - Exodus 1"), "NIV")
        self.assertEqual(len(passage11.verses), 48)

        passage12 = Passage(Reference("Jude - Revelation 1"), "NIV")
        self.assertEqual(len(passage12.verses), 45)

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
        reference = Reference("John 1:1 - 1:5")
        translation = "ESV"
        passage = Passage(reference, translation)

        mock_api_return = '[1] In the beginning was the Word, and the Word was with ' + \
        'God, and the Word was God. [2] He was in the beginning with God. [3] ' + \
        'All things were made through him, and without him was not any thing ' + \
        'made that was made. [4] In him was life, and the life was the light of ' + \
        'men. [5] The light shines in the darkness, and the darkness has not ' + \
        'overcome it.\n\n'
        passage.agent._fetch = MagicMock(return_value=mock_api_return)

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
        reference = Reference("1 Peter 1:2 - 1:3")
        translation = "ESV"
        passage = Passage(reference, translation)

        mock_api_return = [
        'according to the foreknowledge of God the Father, in the sanctification of '
        'the Spirit, for obedience to Jesus Christ and for sprinkling with his blood:'
        '\nMay grace and peace be multiplied to you. \n', 'Blessed be the God and Father '
        'of our Lord Jesus Christ! According to his great mercy, he has caused us to be '
        'born again to a living hope through the resurrection of Jesus Christ from the dead,'
        ]

        passage.agent._fetch = MagicMock(return_value=mock_api_return)

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
