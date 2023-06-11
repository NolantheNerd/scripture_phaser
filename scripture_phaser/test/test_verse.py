import unittest
from scripture_phaser.verse import Verse

class VerseTests(unittest.TestCase):
    def test_validate(self):
        # Job 1:1
        ref1 = Verse(17, 0, 0)
        # Psalm 151:1
        ref2 = Verse(18, 150, 0)
        # 1 Samuel 1:200
        ref3 = Verse(8, 0, 200)
        # 3 John 1:5
        ref4 = Verse(63, 0, 4)
        # Steven 1:1
        ref5 = Verse(-1, 0, 0)

        self.assertTrue(Verse.validate(ref1))
        self.assertFalse(Verse.validate(ref2))
        self.assertFalse(Verse.validate(ref3))
        self.assertTrue(Verse.validate(ref4))
        self.assertFalse(Verse.validate(ref5))
