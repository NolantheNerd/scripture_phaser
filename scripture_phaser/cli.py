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

import argparse
from scripture_phaser.api import API
from scripture_phaser.enums import App
from scripture_phaser.models import Attempt
from scripture_phaser.exceptions import InvalidTranslation

class CLI:
    def __init__(self):
        self.api = API()
        self.config = self.api.load_config()

        self.parser = argparse.ArgumentParser(
            description="scripture_phaser helps you to memorize the Word of Truth.",
        )
        self.parser.add_argument(
            "--reference",
            required=False,
            help="The reference that you want to have scripture_phaser help you to commit to memory",
            dest="reference"
        )
        self.parser.add_argument(
            "--random-mode",
            action="store_true",
            required=False,
            default=False,
            help="Use to have scripture_phaser randomly prompt you with single verse from your passage",
            dest="mode"
        )
        self.parser.add_argument(
            "--translation",
            required=False,
            default=None,
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

        self.mainloop()

    def mainloop(self):
        print("scripture_phaser helps you to memorize the Word of Truth.")
        print("Copyright (C) 2023 Nolan McMahon")

        while True:
            user_input = input("> ").strip().lower()

            # Exit
            if user_input == "q" or user_input == "quit":
                break

            # Get Config
            elif user_input == "g" or user_input == "get":
                self.api.load_config()
                print("Configuration loaded!")

            # Write Config
            elif user_input == "w" or user_input == "write":
                self.api.save_config()
                print("Current configuration saved!")

            # Current State
            elif user_input == "l" or user_input == "list":
                if self.api.passage is not None:
                    print(f"Reference: {self.api.passage.reference}")
                else:
                    print("Reference: No reference set")
                print(f"Translation: {self.api.translation.name}")
                print(f"Random Mode: {self.api.mode}")
                if App.esv_api_key.name in self.api.config and \
                        self.api.config[App.esv_api_key.name] != "None":
                    print(f"API Key for ESV.org Found")

            # Toggle Mode
            elif user_input == "m" or user_input == "mode":
                self.api.mode = not self.api.mode
                print(f"Toggled random mode to {self.api.mode}")

            # Set Reference
            elif user_input == "r" or user_input == "reference":
                ref_str = input("Reference: ")
                self.api.passage = ref_str

            # View Passage
            elif user_input == "v" or user_input == "view":
                self.api.view_passage()

            # Set Translation
            elif user_input == "t" or user_input == "translation":
                trn_str = input("Translation: ")
                try:
                    self.api.translation = trn_str
                except InvalidTranslation:
                    print("Invalid Translation\nChoose one of:\n" + "\n".join(self.api.list_translations()))

            # View Translations
            elif user_input == "i" or user_input == "inquire":
                print("\n".join(self.api.list_translations()))

            # Practice Passage
            elif user_input == "p" or user_input == "practice":
                if self.api.passage is None:
                    print("Reference: No reference set")
                else:
                    self.api.new_recitation()
                    self.api.launch_recitation()
                    self.api.complete_recitation()

            # Show Stats
            elif user_input == "s" or user_input == "stats":
                pass

            # Show scripture_phaser about
            elif user_input == "z" or user_input == "about":
                pass

            # Print Help
            else:
                print("scripture_phaser can be controlled from the command line with the following commands:")
                print("\tg - Reload the configuration file")
                print("\tw - Save the current configuration")
                print("\tl - Lists selected reference, mode and translation")
                print("\tm - Toggles the mode")
                print("\tr - Sets the reference")
                print("\tt - Set the translation")
                print("\ti - List available translations")
                print("\tp - Practice the current reference")
                print("\tv - Preview current reference")
                print("\ts - View your statistics")
                print("\th - Prints this help message")
                print("\tz - Prints information about scripture_phaser")
                print("\tq - Quits scripture_phaser")

if __name__ == "__main__":
    obj = CLI()
