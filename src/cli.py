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
from src.enums import TermColours as TC
from src.exceptions import InvalidTranslation


class CLISTR:
    def __init__(self, api):
        self.api = api

    @staticmethod
    def CLI_PROMPT():
        return "> "

    @staticmethod
    def DESCRIPTION():
        return "scripture_phaser helps you to memorize the Word of Truth."

    @staticmethod
    def LiCENSE():
        return App.license.value

    @staticmethod
    def VERSION():
        return f"{App.Name.value} version {App.version.value}, Release Date: {App.release_date.value}"

    @staticmethod
    def VERSION_HELP():
        return "show the version number and release date"

    @staticmethod
    def LICENSE_HELP():
        return "show the license"

    @staticmethod
    def WELCOME():
        return (
            f"{TC.PINK}scripture_phaser helps you to memorize the Word of Truth.{TC.WHITE}\n"
            f"{TC.PINK}Copyright (C) 2023 Nolan McMahon{TC.WHITE}"
        )

    @staticmethod
    def CONFIG_LOADED():
        return f"{TC.PINK}Configuration loaded!{TC.WHITE}"

    @staticmethod
    def CONFIG_SAVED():
        return f"{TC.PINK}Current configuration saved!{TC.WHITE}"

    @staticmethod
    def NO_REFERENCE():
        return f"{TC.PINK}Reference:{TC.RED} No reference set{TC.WHITE}"

    @staticmethod
    def STATS_RESET_WARNING():
        return (
            f"Are you sure that you want to reset your statistics? [{TC.RED}y{TC.WHITE}/{TC.GREEN}N{TC.WHITE}] "
        )

    @staticmethod
    def STATS_RESET():
        return f"{TC.PINK}Statistics reset{TC.WHITE}"

    @staticmethod
    def HELP():
        return (
            f"{TC.PINK}scripture_phaser can be controlled from the command line with the following commands:{TC.WHITE}\n"
            f"\t{TC.BLUE}G{TC.WHITE} - {TC.YELLOW}Reload the configuration file{TC.WHITE}\n"
            f"\t{TC.BLUE}H{TC.WHITE} - {TC.YELLOW}Prints this help message{TC.WHITE}\n"
            f"\t{TC.BLUE}I{TC.WHITE} - {TC.YELLOW}List available translations{TC.WHITE}\n"
            f"\t{TC.BLUE}L{TC.WHITE} - {TC.YELLOW}Lists selected reference, mode and translation{TC.WHITE}\n"
            f"\t{TC.BLUE}M{TC.WHITE} - {TC.YELLOW}Toggles the mode{TC.WHITE}\n"
            f"\t{TC.BLUE}P{TC.WHITE} - {TC.YELLOW}Practice the current reference{TC.WHITE}\n"
            f"\t{TC.BLUE}R{TC.WHITE} - {TC.YELLOW}Sets the reference{TC.WHITE}\n"
            f"\t{TC.BLUE}S{TC.WHITE} - {TC.YELLOW}View your statistics{TC.WHITE}\n"
            f"\t{TC.BLUE}T{TC.WHITE} - {TC.YELLOW}Set the translation{TC.WHITE}\n"
            f"\t{TC.BLUE}V{TC.WHITE} - {TC.YELLOW}Preview current reference{TC.WHITE}\n"
            f"\t{TC.BLUE}W{TC.WHITE} - {TC.YELLOW}Save the current configuration{TC.WHITE}\n"
            f"\t{TC.BLUE}Z{TC.WHITE} - {TC.YELLOW}Reset statistics{TC.WHITE}\n"
            f"\t{TC.BLUE}Q{TC.WHITE} - {TC.YELLOW}Quits{TC.WHITE}"
        )

    @staticmethod
    def REFERENCE_PROMPT():
        return f"{TC.PINK}Reference: {TC.WHITE}"

    @staticmethod
    def TRANSLATION_PROMPT():
        return f"{TC.PINK}Translation: {TC.WHITE}"

    def REFERENCE(self):
        return f"{TC.PINK}Reference:{TC.YELLOW} {self.api.passage.reference}{TC.WHITE}"

    def TRANSLATION(self):
        return f"{TC.PINK}Translation:{TC.YELLOW} {self.api.translation.name}{TC.WHITE}"

    def RANDOM_MODE(self):
        return f"{TC.PINK}Random Mode:{TC.YELLOW} {self.api.mode}{TC.WHITE}"

    def TOGGLE_RANDOM_MODE(self):
        return f"{TC.PINK}Toggled random mode to {TC.YELLOW}{self.api.mode}{TC.WHITE}"

    def INVALID_TRANSLATION(self):
        return f"{TC.RED}Invalid Translation\n{TC.PINK}Choose one of:\n{TC.BLUE}" + "\n".join(self.api.list_translations()) + f"{TC.WHITE}"

    def AVAILABLE_TRANSLATIONS(self):
        return f"{TC.PINK}Available Translations:{TC.WHITE}\n{TC.BLUE}" + "\n".join(self.api.list_translations()) + f"{TC.WHITE}"

    def PASSAGE(self):
        return f"{TC.CYAN}{self.api.view_passage()}{TC.WHITE}"

    def SCORE(self, score, diff):
        if score == 1.0:
            return f"{TC.GREEN}Perfect!{TC.WHITE}"
        elif score > 0.75:
            return f"{TC.PINK}Not bad: {TC.GREEN}{round(score * 100, 0)}%{TC.WHITE}\n{TC.CYAN}{diff}{TC.WHITE}"
        else:
            return f"{TC.RED}Not quite...{TC.WHITE}\n{TC.CYAN}{diff}{TC.WHITE}"


class CLI:
    def __init__(self):
        self.api = API()
        self.config = self.api.load_config()
        self.messages = CLISTR(self.api)

        parser = argparse.ArgumentParser(
            description=self.messages.DESCRIPTION()
        )
        parser.add_argument(
            "--version",
            action="store_true",
            required=False,
            default=False,
            help=self.messages.VERSION_HELP(),
            dest="version"
        )
        parser.add_argument(
            "--license",
            action="store_true",
            required=False,
            default=False,
            help=self.messages.LICENSE_HELP(),
            dest="license"
        )
        args = parser.parse_args()

        if getattr(args, "version"):
            print(self.messages.VERSION())

        if getattr(args, "license"):
            print(self.messages.LICENSE())

        if not getattr(args, "version") and not getattr(args, "license"):
            self.mainloop()

    def mainloop(self):
        print(self.messages.WELCOME())

        while True:
            user_input = input(self.messages.CLI_PROMPT()).strip().lower()

            # Exit
            if user_input == "q" or user_input == "quit":
                break

            # Get Config
            elif user_input == "g" or user_input == "get":
                self.api.load_config()
                print(self.messages.CONFIG_LOADED())

            # Write Config
            elif user_input == "w" or user_input == "write":
                self.api.save_config(self.api.config)
                print(self.messages.CONFIG_SAVED())

            # Current State
            elif user_input == "l" or user_input == "list":
                if self.api.passage is not None:
                    print(self.messages.REFERENCE())
                else:
                    print(self.messages.NO_REFERENCE())
                print(self.messages.TRANSLATION())
                print(self.messages.RANDOM_MODE())

            # Toggle Mode
            elif user_input == "m" or user_input == "mode":
                self.api.mode = not self.api.mode
                print(self.messages.TOGGLE_RANDOM_MODE())

            # Set Reference
            elif user_input == "r" or user_input == "reference":
                ref_str = input(self.messages.REFERENCE_PROMPT())
                self.api.passage = ref_str

            # View Passage
            elif user_input == "v" or user_input == "view":
                if self.api.passage is not None:
                    print(self.messages.PASSAGE())
                else:
                    print(self.messages.NO_REFERENCE())

            # Set Translation
            elif user_input == "t" or user_input == "translation":
                trn_str = input(self.messages.TRANSLATION_PROMPT()).upper()
                try:
                    self.api.translation = trn_str
                except InvalidTranslation:
                    print(self.messages.INVALID_TRANSLATION())

            # View Translations
            elif user_input == "i" or user_input == "inquire":
                print(self.messages.AVAILABLE_TRANSLATIONS())

            # Practice Passage
            elif user_input == "p" or user_input == "practice":
                if self.api.passage is None:
                    print(self.messages.NO_REFERENCE())
                else:
                    score, diff = self.api.recitation()
                    print(self.messages.SCORE(score, diff))

            # Show Stats
            elif user_input == "s" or user_input == "stats":
                if self.api.passage is None:
                    print(self.messages.NO_REFERENCE)
                else:
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
                confirmation = input(self.messages.STATS_RESET_WARNING()).strip().lower()
                if confirmation == "y" or confirmation == "yes":
                    self.api.reset_db()
                    print(self.messages.STATS_RESET())

            # Print Help
            else:
                print(self.messages.HELP())
