import unittest
from src.verse import Verse

class VerseTests(unittest.TestCase):
    def test_validate_reference(self):
        self.assertTrue(Verse().validate_reference("Job", "1", "1"))
        self.assertFalse(Verse().validate_reference("Steven", "12", "13"))
        self.assertFalse(Verse().validate_reference("Psalm", "151", "1"))
        self.assertFalse(Verse().validate_reference("One_Samuel", "1", "200"))
        self.assertTrue(Verse().validate_reference("Three_John", "1", "5"))
