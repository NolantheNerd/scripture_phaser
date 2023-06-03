import unittest
from scripture_phaser.agents import BaseAgent
from scripture_phaser.agents import ESVAPIAgent

class AgentsTests(unittest.TestCase):
    def test_esv_api(self):
       self.agent = ESVAPIAgent()

       raw_text = "“—”"
       cleaned_text = "\"-\""

       self.assertEqual(self.agent._clean(raw_text), cleaned_text)

    def test_validate_reference(self):
        self.assertTrue(BaseAgent.validate_reference(("Job", "1", "1")))
        self.assertFalse(BaseAgent.validate_reference(("Steven", "12", "13")))
        self.assertFalse(BaseAgent.validate_reference(("Psalm", "151", "1")))
        self.assertFalse(BaseAgent.validate_reference(("One_Samuel", "1", "200")))
        self.assertTrue(BaseAgent.validate_reference(("Three_John", "1", "5")))

    def test_split_reference(self):
        ref_string1 = "1 John 3:5"
        expected_start_ref1 = ("One_John", "3", "5")
        expected_end_ref1 = ("One_John", "3", "5")
        actual_start_ref1, actual_end_ref1 = BaseAgent.split_reference(ref_string1)
        self.assertTupleEqual(expected_start_ref1, actual_start_ref1)
        self.assertTupleEqual(expected_end_ref1, actual_end_ref1)

        ref_string2 = "genesis 49:2 - 49:8"
        expected_start_ref2 = ("Genesis", "49", "2")
        expected_end_ref2 = ("Genesis", "49", "8")
        actual_start_ref2, actual_end_ref2 = BaseAgent.split_reference(ref_string2)
        self.assertTupleEqual(expected_start_ref2, actual_start_ref2)
        self.assertTupleEqual(expected_end_ref2, actual_end_ref2)

        ref_string3 = "Esther 3:7 - 4"
        expected_start_ref3 = ("Esther", "3", "7")
        expected_end_ref3 = ("Esther", "4", "17")
        actual_start_ref3, actual_end_ref3 = BaseAgent.split_reference(ref_string3)
        self.assertTupleEqual(expected_start_ref3, actual_start_ref3)
        self.assertTupleEqual(expected_end_ref3, actual_end_ref3)

        ref_string4 = "First Kings 4"
        expected_start_ref4 = ("One_Kings", "4", "1")
        expected_end_ref4 = ("One_Kings", "4", "34")
        actual_start_ref4, actual_end_ref4 = BaseAgent.split_reference(ref_string4)
        self.assertTupleEqual(expected_start_ref4, actual_start_ref4)
        self.assertTupleEqual(expected_end_ref4, actual_end_ref4)

        ref_string5 = "exodus 3-4:3"
        expected_start_ref5 = ("Exodus", "3", "1")
        expected_end_ref5 = ("Exodus", "4", "3")
        actual_start_ref5, actual_end_ref5 = BaseAgent.split_reference(ref_string5)
        self.assertTupleEqual(expected_start_ref5, actual_start_ref5)
        self.assertTupleEqual(expected_end_ref5, actual_end_ref5)

    def test_validate_reference_pair(self):
        ref1 = ("Job", "1", "11")
        ref2 = ("Job", "1", "12")
        ref3 = ("Job", "1", "13")
        ref4 = ("Proverbs", "30", "5")

        self.assertTrue(BaseAgent.validate_reference_pair(ref1, ref1))
        self.assertTrue(BaseAgent.validate_reference_pair(ref1, ref2))
        self.assertTrue(BaseAgent.validate_reference_pair(ref1, ref3))
        self.assertFalse(BaseAgent.validate_reference_pair(ref1, ref4))
        self.assertFalse(BaseAgent.validate_reference_pair(ref2, ref1))
        self.assertTrue(BaseAgent.validate_reference_pair(ref2, ref2))
        self.assertTrue(BaseAgent.validate_reference_pair(ref2, ref3))
        self.assertFalse(BaseAgent.validate_reference_pair(ref2, ref4))
        self.assertFalse(BaseAgent.validate_reference_pair(ref3, ref1))
        self.assertFalse(BaseAgent.validate_reference_pair(ref3, ref2))
        self.assertTrue(BaseAgent.validate_reference_pair(ref3, ref3))
        self.assertFalse(BaseAgent.validate_reference_pair(ref3, ref4))
        self.assertFalse(BaseAgent.validate_reference_pair(ref4, ref1))
        self.assertFalse(BaseAgent.validate_reference_pair(ref4, ref2))
        self.assertFalse(BaseAgent.validate_reference_pair(ref4, ref3))
        self.assertTrue(BaseAgent.validate_reference_pair(ref4, ref4))
