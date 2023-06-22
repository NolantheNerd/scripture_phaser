import unittest
from unittest.mock import MagicMock
from scripture_phaser.verse import Verse
from scripture_phaser.passage import Passage
from scripture_phaser.translations import ESV

class PassageTests(unittest.TestCase):
    def test_clean_reference(self):
        verse_string1 = "1 John 3:5"
        expected_string1 = "One John 3:5"
        actual_string1 = Passage.clean_reference(verse_string1)
        self.assertEqual(actual_string1, expected_string1)

        verse_string2 = "genesis 5:1"
        expected_string2 = "Genesis 5:1"
        actual_string2 = Passage.clean_reference(verse_string2)
        self.assertEqual(actual_string2, expected_string2)

        verse_string3 = "exodus 1-2"
        expected_string3 = "Exodus 1 - 2"
        actual_string3 = Passage.clean_reference(verse_string3)
        self.assertEqual(actual_string3, expected_string3)

        verse_string4 = "First Peter - 2 peter 1 : 5"
        expected_string4 = "One Peter - Two Peter 1:5"
        actual_string4 = Passage.clean_reference(verse_string4)
        self.assertEqual(actual_string4, expected_string4)

        verse_string5 = "psalm-proverbs"
        expected_string5 = "Psalms - Proverbs"
        actual_string5 = Passage.clean_reference(verse_string5)
        self.assertEqual(actual_string5, expected_string5)

        verse_string6 = "Ezra 1 : 2-2 : 1"
        expected_string6 = "Ezra 1:2 - 2:1"
        actual_string6 = Passage.clean_reference(verse_string6)
        self.assertEqual(actual_string6, expected_string6)

    def test_reference_to_verses(self):
        verse_string1 = "One John 3:5"
        expected_start_verse1 = Verse(61, 2, 4)
        expected_end_verse1 = Verse(61, 2, 4)
        actual_verses = Passage.reference_to_verses(verse_string1)
        self.assertTrue(Verse.verse_equal(expected_start_verse1, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse1, actual_verses[-1]))

        verse_string2 = "Genesis 49:2 - 49:8"
        expected_start_verse2 = Verse(0, 48, 1)
        expected_end_verse2 = Verse(0, 48, 7)
        actual_verses = Passage.reference_to_verses(verse_string2)
        self.assertTrue(Verse.verse_equal(expected_start_verse2, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse2, actual_verses[-1]))

        verse_string3 = "Esther 3:7 - 4"
        expected_start_verse3 = Verse(16, 2, 6)
        expected_end_verse3 = Verse(16, 3, 16)
        actual_verses = Passage.reference_to_verses(verse_string3)
        self.assertTrue(Verse.verse_equal(expected_start_verse3, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse3, actual_verses[-1]))

        verse_string4 = "One Kings 4"
        expected_start_verse4 = Verse(10, 3, 0)
        expected_end_verse4 = Verse(10, 3, 33)
        actual_verses = Passage.reference_to_verses(verse_string4)
        self.assertTrue(Verse.verse_equal(expected_start_verse4, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse4, actual_verses[-1]))

        verse_string5 = "Exodus 3 - 4:3"
        expected_start_verse5 = Verse(1, 2, 0)
        expected_end_verse5 = Verse(1, 3, 2)
        actual_verses = Passage.reference_to_verses(verse_string5)
        self.assertTrue(Verse.verse_equal(expected_start_verse5, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse5, actual_verses[-1]))

        verse_string6 = "Jude 10"
        expected_start_verse6 = Verse(64, 0, 9)
        expected_end_verse6 = Verse(64, 0, 9)
        actual_verses = Passage.reference_to_verses(verse_string6)
        self.assertTrue(Verse.verse_equal(expected_start_verse6, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse6, actual_verses[-1]))

        verse_string7 = "Genesis"
        expected_start_verse7 = Verse(0, 0, 0)
        expected_end_verse7 = Verse(0, 49, 25)
        actual_verses = Passage.reference_to_verses(verse_string7)
        self.assertTrue(Verse.verse_equal(expected_start_verse7, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse7, actual_verses[-1]))

        verse_string8 = "Genesis - Leviticus"
        expected_start_verse8 = Verse(0, 0, 0)
        expected_end_verse8 = Verse(2, 26, 33)
        actual_verses = Passage.reference_to_verses(verse_string8)
        self.assertTrue(Verse.verse_equal(expected_start_verse8, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse8, actual_verses[-1]))

    def test_validate_verse_pair(self):
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
