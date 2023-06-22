import unittest
from dotenv import dotenv_values
from scripture_phaser.enums import App
from scripture_phaser.verse import Verse
from scripture_phaser.agents import BaseAgent
from scripture_phaser.agents import ESVAPIAgent
from xdg.BaseDirectory import load_first_config

class AgentsTests(unittest.TestCase):
    def setUp(self):
        self.esv_api_key = dotenv_values(
            load_first_config(App.Name.value) + "/config"
        ).get("ESV_API_KEY", None)

    def test_esv_api_clean(self):
        agent = ESVAPIAgent(self.esv_api_key)

        # All ESV API responses end with "\n\n"
        raw_text = "“—”\n\n"
        cleaned_text = "\"-\""

        self.assertEqual(agent._clean(raw_text), cleaned_text)

    def test_esv_api_split(self):
        agent = ESVAPIAgent(self.esv_api_key)

        raw_input ='[1] In the beginning was the Word, and the Word was with ' + \
        'God, and the Word was God. [2] He was in the beginning with God. [3] ' + \
        'All things were made through him, and without him was not any thing ' + \
        'made that was made. [4] In him was life, and the life was the light of ' + \
        'men. [5] The light shines in the darkness, and the darkness has not ' + \
        'overcome it.'

        expected_output = [
        'In the beginning was the Word, and the Word was with God, and the ' +
        'Word was God.',
        'He was in the beginning with God.',
        'All things were made through him, and without him was not any ' +
        'thing made that was made.',
        'In him was life, and the life was the light of men.',
        'The light shines in the darkness, and the darkness has not overcome it.'
        ]

        self.assertEqual(agent._split(raw_input), expected_output)
