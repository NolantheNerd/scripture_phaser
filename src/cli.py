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
from src.api import API
from src.enums import App
from src.models import Attempt
from src.enums import TermColours as TC
from src.exceptions import InvalidTranslation

class CLI:
    def __init__(self):
        self.api = API()
        self.config = self.api.load_config()

        parser = argparse.ArgumentParser(
            description="scripture_phaser helps you to memorize the Word of Truth."
        )
        parser.add_argument(
            "--version",
            action="store_true",
            required=False,
            default=False,
            help="show the version number and release date",
            dest="version"
        )
        parser.add_argument(
            "--license",
            action="store_true",
            required=False,
            default=False,
            help="show the license",
            dest="license"
        )
        args = parser.parse_args()

        if getattr(args, "version"):
            print(f"{App.Name.value} version {App.version.value}, Release Date: {App.release_date.value}")

        if getattr(args, "license"):
            print(App.license.value)

        if not getattr(args, "version") and not getattr(args, "license"):
            self.mainloop()

    def mainloop(self):
        print(f"{TC.PINK helps you to memorize the Word of Truth.{TC.WHITE}")
        print(f"{TC.PINK}Copyright (C) 2023 Nolan McMahon{TC.WHITE}")

        while True:
            user_input = input("> ").strip().lower()

            # Exit
            if user_input == "q" or user_input == "quit":
                break

            # Get Config
            elif user_input == "g" or user_input == "get":
                self.api.load_config()
                print(f"{TC.PINK}Configuration loaded!{TC.WHITE}")

            # Write Config
            elif user_input == "w" or user_input == "write":
                self.api.save_config(self.api.config)
                print(f"{TC.PINK}Current configuration saved!{TC.WHITE}")

            # Current State
            elif user_input == "l" or user_input == "list":
                if self.api.passage is not None:
                    print(f"{TC.PINK}Reference:{TC.YELLOW} {self.api.passage.reference}{TC.WHITE}")
                else:
                    print(f"{TC.PINK}Reference:{TC.RED} No reference set{TC.WHITE}")
                print(f"{TC.PINK}Translation:{TC.YELLOW} {self.api.translation.name}{TC.WHITE}")
                print(f"{TC.PINK}Random Mode:{TC.YELLOW} {self.api.mode}{TC.WHITE}")
                if App.esv_api_key.name in self.api.config and \
                        self.api.config[App.esv_api_key.name] != "None":
                    print(f"{TC.PINK}API Key for ESV.org Found{TC.WHITE}")

            # Toggle Mode
            elif user_input == "m" or user_input == "mode":
                self.api.mode = not self.api.mode
                print(f"{TC.PINK}Toggled random mode to {TC.YELLOW}{self.api.mode}{TC.WHITE}")

            # Set Reference
            elif user_input == "r" or user_input == "reference":
                ref_str = input(f"{TC.PINK}Reference: {TC.WHITE}")
                self.api.passage = ref_str

            # View Passage
            elif user_input == "v" or user_input == "view":
                text = self.api.view_passage()
                if len(text) > 0:
                    print(f"{TC.CYAN}{text}{TC.WHITE}")
                else:
                    print(f"{TC.PINK}Reference:{TC.RED} No reference set{TC.WHITE}")

            # Set Translation
            elif user_input == "t" or user_input == "translation":
                trn_str = input(f"{TC.PINK}Translation: {TC.WHITE}")
                try:
                    self.api.translation = trn_str
                except InvalidTranslation:
                    print(f"{TC.RED}Invalid Translation\n{TC.PINK}Choose one of:\n{TC.BLUE}" + "\n".join(self.api.list_translations()) + f"{TC.WHITE}")

            # View Translations
            elif user_input == "i" or user_input == "inquire":
                print(f"{TC.PINK}Available Translations:{TC.WHITE}")
                print(f"{TC.BLUE}" + "\n".join(self.api.list_translations()) + f"{TC.WHITE}")

            # Practice Passage
            elif user_input == "p" or user_input == "practice":
                if self.api.passage is None:
                    print(f"{TC.PINK}Reference:{TC.RED} No reference set{TC.WHITE}")
                else:
                    score, diff = self.api.recitation()

                    if score == 1.0:
                        print(f"{TC.GREEN}Perfect!{TC.WHITE}")
                    elif score > 0.75:
                        print(f"{TC.PINK}Not bad: {TC.GREEN}{round(score * 100, 0)}%{TC.WHITE}")
                        print(f"{TC.CYAN}{diff}{TC.WHITE}")
                    else:
                        print(f"{TC.RED}Not quite...{TC.WHITE}")
                        print(f"{TC.CYAN}{diff}{TC.WHITE}")

            # Show Stats
            elif user_input == "s" or user_input == "stats":
                total_attempts = self.api.stats.total_attempts()
                total_target_attempts = self.api.stats.total_target_attempts(
                    self.api.passage.reference
                )
                average_target_score = round(
                    self.api.stats.average_target_score(
                        self.api.passage.reference
                    ) * 100, 2
                )

                print(f"{TC.PINK}You've made {TC.GREEN}{total_attempts}{TC.PINK} practice attempts!{TC.WHITE}")
                print(f"{TC.PINK}That includes {TC.GREEN}{total_target_attempts}{TC.PINK} practice attempts of {TC.CYAN}{self.api.passage.reference}{TC.PINK}!{TC.WHITE}")
                print(f"{TC.PINK}Your average score on {TC.CYAN}{self.api.passage.reference}{TC.PINK} is {TC.GREEN}{average_target_score}%{TC.PINK}!{TC.WHITE}")

            # Reset Statistics
            elif user_input == "z" or user_input == "reset":
                confirmation = input(
                    f"Are you sure that you want to reset your statistics? [{TC.RED}y{TC.WHITE}/{TC.GREEN}N{TC.WHITE}] "
                ).strip().lower()
                if confirmation == "y" or confirmation == "yes":
                    self.api.reset_db()
                    print(f"{TC.PINK}Statistics reset{TC.WHITE}")

            # Print Help
            else:
                print(f"{TC.PINK can be controlled from the command line with the following commands:{TC.WHITE}")
                print(f"\t{TC.BLUE}g{TC.WHITE} - {TC.YELLOW}Reload the configuration file{TC.WHITE}")
                print(f"\t{TC.BLUE}w{TC.WHITE} - {TC.YELLOW}Save the current configuration{TC.WHITE}")
                print(f"\t{TC.BLUE}l{TC.WHITE} - {TC.YELLOW}Lists selected reference, mode and translation{TC.WHITE}")
                print(f"\t{TC.BLUE}m{TC.WHITE} - {TC.YELLOW}Toggles the mode{TC.WHITE}")
                print(f"\t{TC.BLUE}r{TC.WHITE} - {TC.YELLOW}Sets the reference{TC.WHITE}")
                print(f"\t{TC.BLUE}t{TC.WHITE} - {TC.YELLOW}Set the translation{TC.WHITE}")
                print(f"\t{TC.BLUE}i{TC.WHITE} - {TC.YELLOW}List available translations{TC.WHITE}")
                print(f"\t{TC.BLUE}p{TC.WHITE} - {TC.YELLOW}Practice the current reference{TC.WHITE}")
                print(f"\t{TC.BLUE}v{TC.WHITE} - {TC.YELLOW}Preview current reference")
                print(f"\t{TC.BLUE}s{TC.WHITE} - {TC.YELLOW}View your statistics")
                print(f"\t{TC.BLUE}h{TC.WHITE} - {TC.YELLOW}Prints this help message")
                print(f"\t{TC.BLUE}z{TC.WHITE} - {TC.YELLOW}Reset statistics")
                print(f"\t{TC.BLUE}q{TC.WHITE} - {TC.YELLOW}Quits{TC.WHITE}")

if __name__ == "__main__":
    obj = CLI()
