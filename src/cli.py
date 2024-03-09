# scripture_phaser helps you to memorize the Bible.
# Copyright (C) 2023-2024 Nolan McMahon
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
import platform
import argparse
import datetime
import subprocess
from sys import exit
from shutil import which
from src.api import API
from src.enums import App
from src.enums import TermColours as TC
from src.exceptions import EditorNotFound
from src.exceptions import InvalidTranslation


class CLISTR:
    def __init__(self, api):
        self.api = api

    @staticmethod
    def CLI_PROMPT():
        return "> "

    @staticmethod
    def STATS_CLI_PROMPT():
        return f"{TC.WHITE}[{TC.GREEN}STATS{TC.WHITE}] > "

    @staticmethod
    def DESCRIPTION():
        return "scripture_phaser helps you to memorize the Bible."

    @staticmethod
    def LICENSE():
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
            f"scripture_phaser helps you to memorize the Bible.\n"
            f"Copyright (C) 2023-2024 Nolan McMahon"
        )

    @staticmethod
    def WELCOME_STATS():
        return (
            f"You are now in the statistics viewer!\n"
            f"To exit back to the main prompt, press 'q'."
        )

    @staticmethod
    def NO_REFERENCE():
        return f"Reference:{TC.RED} No reference set{TC.WHITE}"

    @staticmethod
    def STATS_RESET_WARNING():
        return (
            f"Are you sure that you want to reset your statistics? [{TC.RED}y{TC.WHITE}/{TC.GREEN}N{TC.WHITE}] "
        )

    @staticmethod
    def STATS_RESET():
        return f"Statistics reset{TC.WHITE}"

    @staticmethod
    def HELP():
        return (
            f"scripture_phaser can be controlled from the command line with the following commands:\n"
            f"\t{TC.BLUE}H{TC.WHITE} - Prints this help message\n"
            f"\t{TC.BLUE}I{TC.WHITE} - List available translations\n"
            f"\t{TC.BLUE}L{TC.WHITE} - Lists selected reference, random mode and translation\n"
            f"\t{TC.BLUE}M{TC.WHITE} - Toggles the random_mode\n"
            f"\t{TC.BLUE}N{TC.WHITE} - Toggles whether or not to include the passage numbers\n"
            f"\t{TC.BLUE}P{TC.WHITE} - Practice the current reference\n"
            f"\t{TC.BLUE}R{TC.WHITE} - Sets the reference\n"
            f"\t{TC.BLUE}S{TC.WHITE} - View your statistics\n"
            f"\t{TC.BLUE}T{TC.WHITE} - Set the translation\n"
            f"\t{TC.BLUE}V{TC.WHITE} - Preview current reference\n"
            f"\t{TC.BLUE}Q{TC.WHITE} - Quits"
        )

    @staticmethod
    def STATS_HELP():
        return (
            f"The statistics mode can be controlled from the command line with the following commands:\n"
            f"\t{TC.BLUE}SD{TC.WHITE} - Set the start date used to filter your statistics\n"
            f"\t{TC.BLUE}ED{TC.WHITE} - Set the end date used to filter your statistics\n"
            f"\t{TC.BLUE}A{TC.WHITE}  - List all verses attempted\n"
            f"\t{TC.BLUE}R{TC.WHITE}  - Rank all attempted passages by average score\n"
            f"\t{TC.BLUE}D{TC.WHITE}  - Reset statistics\n"
        )

    @staticmethod
    def REFERENCE_PROMPT():
        return f"{TC.PINK}Reference: {TC.WHITE}"

    @staticmethod
    def TRANSLATION_PROMPT():
        return f"{TC.PINK}Translation: {TC.WHITE}"

    @staticmethod
    def SET_START_DATE():
        return f"{TC.PINK}Set Start Date to Filter by: (Leave Blank to Unset){TC.WHITE}"

    @staticmethod
    def SET_END_DATE():
        return f"{TC.PINK}Set End Date to Filter by: (Leave Blank to Unset):{TC.WHITE}"

    @staticmethod
    def YEAR_PROMPT():
        return f"{TC.PINK}Year (yyyy): {TC.WHITE}"

    @staticmethod
    def MONTH_PROMPT():
        return f"{TC.PINK}Month (mm): {TC.WHITE}"

    @staticmethod
    def DAY_PROMPT():
        return f"{TC.PINK}Day (dd): {TC.WHITE}"

    def START_DATE(self):
        return f"{TC.PINK}Start Date (yyyy-mm-dd):{TC.YELLOW} {self.api.stats.start_date}{TC.WHITE}"

    def END_DATE(self):
        return f"{TC.PINK}End Date (yyyy-mm-dd):{TC.YELLOW} {self.api.stats.end_date}{TC.WHITE}"

    def ALL_ATTEMPTED_VERSES(self):
        start = self.api.stats.start_date
        if isinstance(start, datetime.date):
            start = start.strftime("%B %d, %Y")

        end = self.api.stats.end_date
        if isinstance(end, datetime.date):
            end = end.strftime("%B %d, %Y")

        refs = self.api.stats.all_attempted_verses()
        if len(refs) == 0:
            string = "You haven't recorded any attempts yet!"
        else:
            last_ref = refs.pop()
            if len(refs) == 0:
                ref_str = last_ref
            else:
                ref_str = ", ".join(refs) + f" and {last_ref}"

            if start is not None and end is not None:
                string = f"Between {start} and {end}, you've attempted {ref_str}."
            elif start is not None:
                string = f"Since {start}, you've attempted {ref_str}."
            elif end is not None:
                string = f"Prior to {end}, you've attempted {ref_str}."
            else:
                string = f"You've attempted {ref_str} before."
        return string

    def ALL_VERSES_RANKED(self):
        start = self.api.stats.start_date
        if isinstance(start, datetime.date):
            start = start.strftime("%B %d, %Y")

        end = self.api.stats.end_date
        if isinstance(end, datetime.date):
            end = end.strftime("%B %d, %Y")

        verses = self.api.stats.all_verses_ranked()
        if len(verses) == 0:
            string = "You haven't recorded any attempts yet!"
        else:
            string = ""
            sorted_verses = sorted(verses.items(), key=lambda item: item[1], reverse=True)
            for ref, score in sorted_verses:
                score = round(score * 100, 1)
                if score > 75:
                    string += f"({TC.GREEN}{score}%{TC.WHITE}) {ref}\n"
                else:
                    string += f"({TC.RED}{score}%{TC.WHITE}) {ref}\n"
            string = string[:-1]
        return string

    def REFERENCE(self):
        return f"Reference:{TC.YELLOW} {self.api.passage.reference.ref_str}{TC.WHITE}"

    def TRANSLATION(self):
        return f"Translation:{TC.YELLOW} {self.api.translation}{TC.WHITE}"

    def RANDOM_MODE(self):
        return f"Random Mode:{TC.YELLOW} {self.api.random_mode}{TC.WHITE}"

    def SHOW_PASSAGE_NUMBERS(self):
        return f"Show Passage Numbers:{TC.YELLOW} {self.api.show_passage_numbers}{TC.WHITE}"

    def FAST_RECITATIONS(self):
        return f"Fast Recitations:{TC.YELLOW} {self.api.fast_recitations}{TC.WHITE}"

    def SET_RANDOM_MODE(self):
        return f"Toggled random mode to {TC.YELLOW}{self.api.random_mode}{TC.WHITE}"

    def SET_PASSAGE_NUMBERS(self):
        return f"Toggled show passage numbers to {TC.YELLOW}{self.api.show_passage_numbers}{TC.WHITE}"

    def SET_FAST_RECITATIONS(self):
        return f"Toggled single letter mode to {TC.YELLOW}{self.api.fast_recitations}{TC.WHITE}"

    def INVALID_TRANSLATION(self):
        return f"{TC.RED}Invalid Translation\n{TC.WHITE}Choose one of:\n{TC.BLUE}" + "\n".join(self.api.view_translation()) + f"{TC.WHITE}"

    def AVAILABLE_TRANSLATIONS(self):
        return f"Available Translations:\n{TC.BLUE}" + "\n".join(self.api.view_translation()) + f"{TC.WHITE}"

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

        try:
            self.editor = os.environ["EDITOR"]
        except KeyError:
            try:
                if which("gedit") is not None:
                    self.editor = "gedit"
                elif which("nano") is not None:
                    self.editor = "nano"
                elif which("nvim") is not None:
                    self.editor = "nvim"
                elif which("vim") is not None:
                    self.editor = "vim"
                elif which("notepad") is not None:
                    self.editor = "notepad"
                else:
                    raise EditorNotFound()
            except EditorNotFound as e:
                print(e.__str__())
                exit()

        self.is_windows = platform.system() == "Windows"

        if not getattr(args, "version") and not getattr(args, "license"):
            self.mainloop()

    def mainloop(self):
        print(self.messages.WELCOME())

        while True:
            user_input = input(self.messages.CLI_PROMPT()).strip().lower()

            # Exit
            if user_input == "q" or user_input == "quit":
                break

            # Current State
            elif user_input == "l" or user_input == "list":
                if self.api.passage is not None:
                    print(self.messages.REFERENCE())
                else:
                    print(self.messages.NO_REFERENCE())
                print(self.messages.TRANSLATION())
                print(self.messages.RANDOM_MODE())
                print(self.messages.SHOW_PASSAGE_NUMBERS())
                print(self.messages.FAST_RECITATIONS())

            # Set (Toggle) Mode
            elif user_input == "m" or user_input == "random_mode":
                self.api.set_random_mode()
                print(self.messages.SET_RANDOM_MODE())

            # Set (Toggle) the Passage Numbers
            elif user_input == "n" or user_input == "numbers":
                self.api.set_show_passage_numbers()
                print(self.messages.SET_PASSAGE_NUMBERS())

            # Set (Toggle) Fast Recitations
            elif user_input == "f" or user_input == "fast":
                self.api.set_fast_recitations()
                print(self.messages.SET_FAST_RECITATIONS())

            # Set Reference
            elif user_input == "r" or user_input == "reference":
                ref_str = input(self.messages.REFERENCE_PROMPT())
                self.api.set_passage(ref_str)

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
                    self.api.set_translation(trn_str)
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
                    reference = self.api.new_recitation()
                    if self.is_windows:
                        windows_filename = f"{reference.ref_str}".replace(":", ";")
                        filename = self.api.cache_path / windows_filename
                    else:
                        filename = self.api.cache_path / f"{reference.ref_str}"

                    filename.touch(exist_ok=True)
                    subprocess.run([self.editor, filename])

                    if not filename.exists():
                        text = ""
                    else:
                        with open(filename, "r") as file:
                            text = file.readlines()
                            text = "".join(text)

                        # Editors Sometimes add \n at the end of a file, if
                        # one doesn't already exist @@@ TODO (Nolan): Think
                        # about the case where the correct recitation ends
                        # with a \n and the user has set these options...
                        if len(text) > 0 and text[-1] == "\n":
                            text = text[:-1]

                        if filename.exists():
                            os.remove(filename)

                    score, diff = self.api.finish_recitation(reference, text)
                    print(self.messages.SCORE(score, diff))

            # Show Stats
            elif user_input == "s" or user_input == "stats":
                self.stats_mainloop()

            # Print Help
            else:
                print(self.messages.HELP())

    def stats_mainloop(self):
        print(self.messages.WELCOME_STATS())

        while True:
            user_input = input(self.messages.STATS_CLI_PROMPT()).strip().lower()

            # Current State
            if user_input == "l" or user_input == "list":
                print(self.messages.START_DATE())
                print(self.messages.END_DATE())

            # Set Start Date
            elif user_input == "sd" or user_input == "start date":
                print(self.messages.SET_START_DATE())
                year = input(self.messages.YEAR_PROMPT())
                month = input(self.messages.MONTH_PROMPT())
                day = input(self.messages.DAY_PROMPT())

                if not (year.isdecimal() and month.isdecimal() and day.isdecimal()):
                    self.api.stats.start_date = None
                else:
                    try:
                        self.api.stats.start_date = datetime.date(int(year), int(month), int(day))
                    except ValueError as e:
                        print(e.__str__().capitalize())

            # Set End Date
            elif user_input == "ed" or user_input == "end date":
                print(self.messages.SET_END_DATE())
                year = input(self.messages.YEAR_PROMPT())
                month = input(self.messages.MONTH_PROMPT())
                day = input(self.messages.DAY_PROMPT())

                if not (year.isdecimal() and month.isdecimal() and day.isdecimal()):
                    self.api.stats.start_date = None
                else:
                    try:
                        self.api.stats.end_date = datetime.date(int(year), int(month), int(day))

                    except ValueError as e:
                        print(e.__str__().capitalize())

            # See All Attempted Verses
            elif user_input == "a" or user_input == "all":
                print(self.messages.ALL_ATTEMPTED_VERSES())

            # See All Verses Ranked By Score
            elif user_input == "r" or user_input == "rank":
                print(self.messages.ALL_VERSES_RANKED())

            # Reset Statistics
            elif user_input == "d" or user_input == "reset":
                confirmation = input(self.messages.STATS_RESET_WARNING()).strip().lower()
                if confirmation == "y" or confirmation == "yes":
                    self.api.stats.reset_db()
                    print(self.messages.STATS_RESET())

            # Exit Stats
            elif user_input == "q" or user_input == "quit":
                break

            # Print Stats Help
            else:
                print(self.messages.STATS_HELP())
