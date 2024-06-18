# scripture_phaser helps you to memorize the Bible.
# Copyright (C) 2023-2024 Nolan McMahon
#
# This file is part of scripture_phaser.
#
# scripture_phaser is licensed under the terms of the BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
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

from unittest.mock import MagicMock
from src.passage import Passage
from src.reference import Reference
from test.test_base import BaseTest


class PassageTests(BaseTest):
    """
    Test the Passage Object
    """
    def test_show(self) -> None:
        """
        Do passages display their content properly?
        """
        reference = Reference("1 Peter 1:2 - 1:3")
        translation = "ESV"
        passage = Passage(reference, translation)

        mock_api_return = [
        'according to the foreknowledge of God the Father, in the sanctification of '
        'the Spirit, for obedience to Jesus Christ and for sprinkling with his blood:'
        '\nMay grace and peace be multiplied to you. \n', 'Blessed be the God and Father '
        'of our Lord Jesus Christ! According to his great mercy, he has caused us to be '
        'born again to a living hope through the resurrection of Jesus Christ from the dead,'
        ]

        passage.agent.fetch = MagicMock(return_value=mock_api_return)

        expected_clean = 'according to the foreknowledge of God the Father, ' + \
        'in the sanctification of the Spirit, for obedience to Jesus Christ and ' + \
        'for sprinkling with his blood:\nMay grace and peace be multiplied to ' + \
        'you. \nBlessed be the God and Father of our Lord Jesus Christ! ' + \
        'According to his great mercy, he has caused us to be born again to a ' + \
        'living hope through the resurrection of Jesus Christ from the dead,'

        expected_verse = '[2] according to the foreknowledge of God the Father, ' + \
        'in the sanctification of the Spirit, for obedience to Jesus Christ and ' + \
        'for sprinkling with his blood:\nMay grace and peace be multiplied to ' + \
        'you. \n[3] Blessed be the God and Father of our Lord Jesus Christ! ' + \
        'According to his great mercy, he has caused us to be born again to a ' + \
        'living hope through the resurrection of Jesus Christ from the dead,'

        expected_ref = 'according to the foreknowledge of God the Father, ' + \
        'in the sanctification of the Spirit, for obedience to Jesus Christ and ' + \
        'for sprinkling with his blood:\nMay grace and peace be multiplied to ' + \
        'you. \nBlessed be the God and Father of our Lord Jesus Christ! ' + \
        'According to his great mercy, he has caused us to be born again to a ' + \
        'living hope through the resurrection of Jesus Christ from the dead, ' + \
        '- 1 Peter 1:2-3'

        expected_full = '[2] according to the foreknowledge of God the Father, ' + \
        'in the sanctification of the Spirit, for obedience to Jesus Christ and ' + \
        'for sprinkling with his blood:\nMay grace and peace be multiplied to ' + \
        'you. \n[3] Blessed be the God and Father of our Lord Jesus Christ! ' + \
        'According to his great mercy, he has caused us to be born again to a ' + \
        'living hope through the resurrection of Jesus Christ from the dead, ' + \
        '- 1 Peter 1:2-3'

        passage.populate()

        self.assertEqual(passage.show(), expected_clean)
        self.assertEqual(passage.show(with_verse=True), expected_verse)
        self.assertEqual(passage.show(with_ref=True), expected_ref)
        self.assertEqual(passage.show(with_verse=True, with_ref=True), expected_full)
