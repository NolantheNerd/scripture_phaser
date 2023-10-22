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
import argparse
from pathlib import Path
from dotenv import dotenv_values
from scripture_phaser.api import API
from scripture_phaser.enums import App
from xdg.BaseDirectory import xdg_config_home
from xdg.BaseDirectory import save_config_path
from xdg.BaseDirectory import load_first_config

class CLI:
    def __init__(self):
        self.config = self.load_config()

        self.parser = argparse.ArgumentParser(
            description="scripture_phaser helps you to memorize the Word of Truth.",
        )
        self.parser.add_argument(
            "--tui",
            action="store_true",
            required=False,
            default=self.config["tui"],
            help="Interact with scripture_phaser through a TUI instead of the CLI",
            dest="tui"
        )
        self.parser.add_argument(
            "--reference",
            required=False, # @@@ TODO: Make optional if --tui
            help="The reference that you want to have scripture_phaser help you to commit to memory",
            dest="reference"
        )
        self.parser.add_argument(
            "--random-mode",
            action="store_true",
            required=False,
            default=self.config["random_mode"],
            help="Use to have scripture_phaser randomly prompt you with single verse from your passage",
            dest="mode"
        )
        self.parser.add_argument(
            "--translation",
            required=False,
            default=self.config["translation"],
            help="The translation to use when evaluating your submissions",
            dest="translation"
        )
        self.parser.add_argument(
            "--list-translations",
            action="store_true",
            required=False,
            default=False,
            help="List available translations",
            dest="list_translations"
        )
        args = self.parser.parse_args()

    def load_config(self):
        config_path = Path(save_config_path(App.Name.value))
        config_path /= "config"
        if not config_path.exists():
            with open(config_path, "w") as config_file:
                for default in App.Defaults.value:
                    config_file.write(f"{default.name}=\"{default.value}\"\n")

        config = dotenv_values(config_path)

        missing_keys = []
        for default in App.Defaults.value:
            key = default.name
            if key not in config:
                missing_keys.append(key)
        if len(missing_keys) > 0:
            with open(config_path, "a") as config_file:
                for key in missing_keys:
                    config_file.write(f"{key}=\"{App.Defaults.value[key].value}\"\n")
                    config[key] = App.Defaults.value[key].value

        return config

if __name__ == "__main__":
    obj = CLI()
