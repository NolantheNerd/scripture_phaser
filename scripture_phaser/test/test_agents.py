import unittest
from scripture_phaser.verse import Verse
from scripture_phaser.agents import BaseAgent
from scripture_phaser.agents import ESVAPIAgent

class AgentsTests(unittest.TestCase):
    @unittest.skip("")
    def test_esv_api(self):
       self.agent = ESVAPIAgent()

       raw_text = "“—”"
       cleaned_text = "\"-\""

       self.assertEqual(self.agent._clean(raw_text), cleaned_text)
