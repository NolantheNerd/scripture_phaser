import unittest
from scripture_phaser.verse import Verse

class VerseTests(unittest.TestCase):
    """
    Test the Verse Object
    """
    def test_validate(self):
        """
        Are illegitimate verses uninstantiatable?
        """
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

    def test_show(self):
        """
        Do verses preview correctly?
        """
        # John 11:35
        text = "Jesus wept."
        verse = Verse(42, 10, 34, text)

        self.assertEqual(
            verse.show(),
            text
        )

        self.assertEqual(
            verse.show(with_verse=True),
            f"[35] {text}"
        )

        self.assertEqual(
            verse.show(with_ref=True),
            f"{text} - John 11:35"
        )

        self.assertEqual(
            verse.show(with_verse=True, with_ref=True),
            f"[35] {text} - John 11:35"
        )
