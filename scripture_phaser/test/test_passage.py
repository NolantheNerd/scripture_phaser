import unittest
from scripture_phaser.verse import Verse
from scripture_phaser.passage import Passage

class PassageTests(unittest.TestCase):
    def test_reference_to_verses(self):
        verse_string1 = "One John 3:5"
        expected_start_verse1 = Verse(61, 2, 5)
        expected_end_verse1 = Verse(61, 2, 5)
        actual_verses = Passage.reference_to_verses(verse_string1)
        self.assertTrue(Verse.verse_equal(expected_start_verse1, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse1, actual_verses[-1]))

        verse_string2 = "Genesis 49:2 - 49:8"
        expected_start_verse2 = Verse(0, 48, 2)
        expected_end_verse2 = Verse(0, 48, 8)
        actual_verses = Passage.reference_to_verses(verse_string2)
        self.assertTrue(Verse.verse_equal(expected_start_verse2, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse2, actual_verses[-1]))

        verse_string3 = "Esther 3:7 - 4"
        expected_start_verse3 = Verse(16, 2, 7)
        expected_end_verse3 = Verse(16, 3, 17)
        actual_verses = Passage.reference_to_verses(verse_string3)
        self.assertTrue(Verse.verse_equal(expected_start_verse3, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse3, actual_verses[-1]))

        verse_string4 = "One Kings 4"
        expected_start_verse4 = Verse(10, 3, 1)
        expected_end_verse4 = Verse(10, 3, 34)
        actual_verses = Passage.reference_to_verses(verse_string4)
        self.assertTrue(Verse.verse_equal(expected_start_verse4, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse4, actual_verses[-1]))

        verse_string5 = "Exodus 3-4:3"
        expected_start_verse5 = Verse(1, 2, 1)
        expected_end_verse5 = Verse(1, 3, 3)
        actual_verses = Passage.reference_to_verses(verse_string5)
        self.assertTrue(Verse.verse_equal(expected_start_verse5, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse5, actual_verses[-1]))

        verse_string6 = "Jude 10"
        expected_start_verse6 = Verse(64, 0, 10)
        expected_end_verse6 = Verse(64, 0, 10)
        actual_verses = Passage.reference_to_verses(verse_string6)
        self.assertTrue(Verse.verse_equal(expected_start_verse6, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse6, actual_verses[-1]))

        verse_string7 = "Genesis"
        expected_start_verse7 = Verse(0, 0, 1)
        expected_end_verse7 = Verse(0, 49, 26)
        actual_verses = Passage.reference_to_verses(verse_string7)
        self.assertTrue(Verse.verse_equal(expected_start_verse7, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse7, actual_verses[-1]))

        verse_string8 = "Genesis - Leviticus"
        expected_start_verse8 = Verse(0, 0, 1)
        expected_end_verse8 = Verse(2, 26, 34)
        actual_verses = Passage.reference_to_verses(verse_string8)
        self.assertTrue(Verse.verse_equal(expected_start_verse8, actual_verses[0]))
        self.assertTrue(Verse.verse_equal(expected_end_verse8, actual_verses[-1]))

    @unittest.skip("")
    def test_validate_verse_pair(self):
        ref1 = ("Job", "1", "11")
        ref2 = ("Job", "1", "12")
        ref3 = ("Job", "1", "13")
        ref4 = ("Proverbs", "30", "5")

        self.assertTrue(Passage.validate_verse_pair(ref1, ref1))
        self.assertTrue(Passage.validate_verse_pair(ref1, ref2))
        self.assertTrue(Passage.validate_verse_pair(ref1, ref3))
        self.assertFalse(Passage.validate_verse_pair(ref1, ref4))
        self.assertFalse(Passage.validate_verse_pair(ref2, ref1))
        self.assertTrue(Passage.validate_verse_pair(ref2, ref2))
        self.assertTrue(Passage.validate_verse_pair(ref2, ref3))
        self.assertFalse(Passage.validate_verse_pair(ref2, ref4))
        self.assertFalse(Passage.validate_verse_pair(ref3, ref1))
        self.assertFalse(Passage.validate_verse_pair(ref3, ref2))
        self.assertTrue(Passage.validate_verse_pair(ref3, ref3))
        self.assertFalse(Passage.validate_verse_pair(ref3, ref4))
        self.assertFalse(Passage.validate_verse_pair(ref4, ref1))
        self.assertFalse(Passage.validate_verse_pair(ref4, ref2))
        self.assertFalse(Passage.validate_verse_pair(ref4, ref3))
        self.assertTrue(Passage.validate_verse_pair(ref4, ref4))
