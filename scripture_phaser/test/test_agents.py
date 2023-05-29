import unittest
from scripture_phaser.agents import ESVAPIAgent

class AgentsTests(unittest.TestCase):
    def test_esv_api(self):
       self.agent = ESVAPIAgent()
       ref = "1 Peter 2:6"

       raw_text = "“—”"

       cleaned_text = "\"-\""

       self.assertEqual(self.agent._clean(raw_text), cleaned_text)
