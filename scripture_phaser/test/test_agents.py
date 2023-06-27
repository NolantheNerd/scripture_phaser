import unittest
from dotenv import dotenv_values
from unittest.mock import MagicMock
from scripture_phaser.enums import App
from scripture_phaser.verse import Verse
from scripture_phaser.agents import BaseAgent
from scripture_phaser.agents import ESVAPIAgent
from scripture_phaser.agents import KJVAPIAgent
from scripture_phaser.agents import WEBAPIAgent
from xdg.BaseDirectory import load_first_config

class AgentsTests(unittest.TestCase):
    def test_esvapi_agent(self):
        esv_api_key = dotenv_values(
            load_first_config(App.Name.value) + "/config"
        ).get("ESV_API_KEY", None)
        agent = ESVAPIAgent(esv_api_key)

        # All ESV API responses end with "\n\n"
        raw_text = "“—”\n\n"
        cleaned_text = "\"-\""

        self.assertEqual(agent._clean(raw_text), cleaned_text)

        ref = "John 1:1-5"
        raw_return ='[1] In the beginning was the Word, and the Word was with ' + \
        'God, and the Word was God. [2] He was in the beginning with God. [3] ' + \
        'All things were made through him, and without him was not any thing ' + \
        'made that was made. [4] In him was life, and the life was the light of ' + \
        'men. [5] The light shines in the darkness, and the darkness has not ' + \
        'overcome it.\n\n'

        agent._fetch = MagicMock(return_value=raw_return)

        expected_output = [
        'In the beginning was the Word, and the Word was with God, and the ' +
        'Word was God.',
        'He was in the beginning with God.',
        'All things were made through him, and without him was not any ' +
        'thing made that was made.',
        'In him was life, and the life was the light of men.',
        'The light shines in the darkness, and the darkness has not overcome it.'
        ]

        self.assertEqual(agent.get(ref), expected_output)

    def test_kjv_agent(self):
        agent = KJVAPIAgent()
        ref = "1 Peter 1:1-5"

        raw_return = '(1) Peter, an apostle of Jesus Christ, to the strangers ' + \
        'scattered throughout Pontus, Galatia, Cappadocia, Asia, and ' + \
        'Bithynia,\n(2) Elect according to the foreknowledge of God the Father, ' + \
        'through sanctification of the Spirit, unto obedience and sprinkling of ' + \
        'the blood of Jesus Christ: Grace unto you, and peace, be ' + \
        'multiplied.\n(3) Blessed\nbe the God and Father of our Lord Jesus ' + \
        'Christ, which according to his abundant mercy hath begotten us again ' + \
        'unto a lively hope by the resurrection of Jesus Christ from the ' + \
        'dead,\n(4) To an inheritance incorruptible, and undefiled, and that ' + \
        'fadeth not away, reserved in heaven for you,\n(5) Who are kept by the ' + \
        'power of God through faith unto salvation ready to be revealed in the ' + \
        'last time.\n'

        agent._fetch = MagicMock(return_value=raw_return)

        expected_clean = '(1) Peter, an apostle of Jesus Christ, to the strangers ' + \
        'scattered throughout Pontus, Galatia, Cappadocia, Asia, and ' + \
        'Bithynia,\n(2) Elect according to the foreknowledge of God the Father, ' + \
        'through sanctification of the Spirit, unto obedience and sprinkling of ' + \
        'the blood of Jesus Christ: Grace unto you, and peace, be ' + \
        'multiplied.\n(3) Blessed\nbe the God and Father of our Lord Jesus ' + \
        'Christ, which according to his abundant mercy hath begotten us again ' + \
        'unto a lively hope by the resurrection of Jesus Christ from the ' + \
        'dead,\n(4) To an inheritance incorruptible, and undefiled, and that ' + \
        'fadeth not away, reserved in heaven for you,\n(5) Who are kept by the ' + \
        'power of God through faith unto salvation ready to be revealed in the ' + \
        'last time.'

        self.assertEqual(agent._clean(raw_return), expected_clean)

        expected_split = [
            'Peter, an apostle of Jesus Christ, to the strangers ' + \
        'scattered throughout Pontus, Galatia, Cappadocia, Asia, and ' + \
        'Bithynia,\n',
            'Elect according to the foreknowledge of God the Father, ' + \
        'through sanctification of the Spirit, unto obedience and sprinkling of ' + \
        'the blood of Jesus Christ: Grace unto you, and peace, be ' + \
        'multiplied.\n',
            'Blessed\nbe the God and Father of our Lord Jesus ' + \
        'Christ, which according to his abundant mercy hath begotten us again ' + \
        'unto a lively hope by the resurrection of Jesus Christ from the ' + \
        'dead,\n',
            'To an inheritance incorruptible, and undefiled, and that ' + \
        'fadeth not away, reserved in heaven for you,\n',
            'Who are kept by the ' + \
        'power of God through faith unto salvation ready to be revealed in the ' + \
        'last time.'
        ]
        self.assertEqual(agent.get(ref), expected_split)

    def test_web_agent(self):
        agent = WEBAPIAgent()
        ref = "1 Peter 1:1-5"

        raw_return = "(1) Peter, an apostle of Jesus Christ, to the chosen ones " + \
        "who are living as foreigners in the Dispersion in Pontus, Galatia, " + \
        "Cappadocia, Asia, and Bithynia,\n(2) according to the foreknowledge of " + \
        "God the Father, in sanctification of the Spirit, that you may obey " + \
        "Jesus Christ and be sprinkled with his blood: Grace to you and peace be " + \
        "multiplied.\n(3) Blessed be the God and Father of our Lord Jesus " + \
        "Christ, who according to his great mercy caused us to be born again to " + \
        "a living hope through the resurrection of Jesus Christ from the " + \
        "dead,\n(4) to an incorruptible and undefiled inheritance that doesn’t " + \
        "fade away, reserved in Heaven for you,\n(5) who by the power of God are " + \
        "guarded through faith for a salvation ready to be revealed in the last " + \
        "time.\n"

        agent._fetch = MagicMock(return_value=raw_return)

        expected_clean = "(1) Peter, an apostle of Jesus Christ, to the chosen ones " + \
        "who are living as foreigners in the Dispersion in Pontus, Galatia, " + \
        "Cappadocia, Asia, and Bithynia,\n(2) according to the foreknowledge of " + \
        "God the Father, in sanctification of the Spirit, that you may obey " + \
        "Jesus Christ and be sprinkled with his blood: Grace to you and peace be " + \
        "multiplied.\n(3) Blessed be the God and Father of our Lord Jesus " + \
        "Christ, who according to his great mercy caused us to be born again to " + \
        "a living hope through the resurrection of Jesus Christ from the " + \
        "dead,\n(4) to an incorruptible and undefiled inheritance that doesn’t " + \
        "fade away, reserved in Heaven for you,\n(5) who by the power of God are " + \
        "guarded through faith for a salvation ready to be revealed in the last " + \
        "time."

        self.assertEqual(agent._clean(raw_return), expected_clean)

        expected_split = [
            "Peter, an apostle of Jesus Christ, to the chosen ones who are living as foreigners in the Dispersion in Pontus, Galatia, Cappadocia, Asia, and Bithynia,\n",
            "according to the foreknowledge of God the Father, in sanctification of the Spirit, that you may obey Jesus Christ and be sprinkled with his blood: Grace to you and peace be multiplied.\n",
            "Blessed be the God and Father of our Lord Jesus Christ, who according to his great mercy caused us to be born again to a living hope through the resurrection of Jesus Christ from the dead,\n",
            "to an incorruptible and undefiled inheritance that doesn’t fade away, reserved in Heaven for you,\n",
        "who by the power of God are guarded through faith for a salvation ready to be revealed in the last time."
        ]

        self.assertEqual(agent.get(ref), expected_split)
