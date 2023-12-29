# scripture_phaser helps you to memorize the Word of Truth.
# Copyright (C) 2023 Nolan McMahon
#
# This file is part of scripture_phaser.
#
# scripture_phaser is licensed under the terms of the BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import unittest
from dotenv import dotenv_values
from unittest.mock import MagicMock
from src.enums import App
from src.agents import ESVAPIAgent
from src.agents import KJVAPIAgent
from src.agents import WEBAPIAgent
from src.agents import BBEAPIAgent
from xdg.BaseDirectory import load_first_config


class AgentsTests(unittest.TestCase):
    """
    Test the Agent Object
    """
    def test_esvapi_agent(self):
        """
        Can api.esv.org responses be versified?
        """
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

    def test_kjvapi_agent(self):
        """
        Can bible-api.com responses be versified (KJV)?
        """
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

    def test_webapi_agent(self):
        """
        Can bible-api.com responses be versified (WEB)?
        """
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

    def test_bbeapi_agent(self):
        """
        Can bible-api.com responses be versified (BBE)?
        """
        agent = BBEAPIAgent()
        ref = "1 Peter 1:1-5"

        raw_return = "(1) Peter, an Apostle of Jesus Christ, to the saints who " + \
        "are living in Pontus, Galatia, Cappadocia, Asia, and Bithynia,(2) Who, " + \
        "through the purpose of God, have been made holy by the Spirit, " + \
        "disciples of Jesus, made clean by his blood: May you have grace and " + \
        "peace in full measure.(3) Praise be to the God and Father of our Lord " + \
        "Jesus Christ, who through his great mercy has given us a new birth and " + \
        "a living hope by the coming again of Jesus Christ from the dead,(4) And " + \
        "a heritage fair, holy and for ever new, waiting in heaven for you,(5) " + \
        "Who, by the power of God are kept, through faith, for that salvation, " + \
        "which will be seen at the last day. "

        agent._fetch = MagicMock(return_value=raw_return)
        expected_clean = raw_return
        self.assertEqual(agent._clean(raw_return), expected_clean)

        expected_split = [
            "Peter, an Apostle of Jesus Christ, to the saints who are living in Pontus, Galatia, Cappadocia, Asia, and Bithynia,",
            "Who, through the purpose of God, have been made holy by the Spirit, disciples of Jesus, made clean by his blood: May you have grace and peace in full measure.",
            "Praise be to the God and Father of our Lord Jesus Christ, who through his great mercy has given us a new birth and a living hope by the coming again of Jesus Christ from the dead,",
            "And a heritage fair, holy and for ever new, waiting in heaven for you,",
            "Who, by the power of God are kept, through faith, for that salvation, which will be seen at the last day. "
        ]

        self.assertEqual(agent.get(ref), expected_split)
