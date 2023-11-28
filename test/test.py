#!/usr/share/python

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

import os
import unittest
from pathlib import Path
from xdg.BaseDirectory import save_config_path
from colour_runner.runner import ColourTextTestRunner
from src.enums import App
from test_agents import AgentsTests
from test_passage import PassageTests
from test_verse import VerseTests
from test_api import APITests
from test_attempt import AttemptTests

suite = unittest.TestSuite()

suite.addTest(AgentsTests("test_esvapi_agent"))
suite.addTest(AgentsTests("test_kjvapi_agent"))
suite.addTest(AgentsTests("test_webapi_agent"))
suite.addTest(AgentsTests("test_bbeapi_agent"))

suite.addTest(VerseTests("test_validate"))
suite.addTest(VerseTests("test_show"))

suite.addTest(PassageTests("test_validate_verse_pair"))
suite.addTest(PassageTests("test_clean_reference"))
suite.addTest(PassageTests("test_interpret_reference"))
suite.addTest(PassageTests("test_reference_to_verses"))
suite.addTest(PassageTests("test_populate"))
suite.addTest(PassageTests("test_show"))

suite.addTest(APITests("test_translation_setter"))
suite.addTest(APITests("test_get_random_verse"))

suite.addTest(AttemptTests("test_grade"))

if __name__ == "__main__":
    try:
        config_path = Path(save_config_path(App.Name.value))
        config_file = config_path / "config"
        temp_config_file = config_path / "config_TEST"
        if config_file.exists():
            os.rename(config_file, temp_config_file)

        ColourTextTestRunner(verbosity=2).run(suite)

    finally:
        if temp_config_file.exists():
            os.rename(temp_config_file, config_file)
