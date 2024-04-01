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
import readchar
import argparse
import subprocess
from shutil import which
from src.api import API
from src.enums import App
from difflib import SequenceMatcher
from src.enums import TermColours as TC
from src.exceptions import EditorNotFound
from src.exceptions import InvalidTranslation

NUM_DAYS_FOR_GOOD_STREAK = 7
GOOD_YEARLY_ATTEMPT_COUNT = 180


class CLISTR:
    def __init__(self, api):
        self.api = api

    @staticmethod
    def CLI_PROMPT():
        return "> "

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
            "scripture_phaser helps you to memorize the Bible.\n"
            "Copyright (C) 2023-2024 Nolan McMahon"
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
            f"This is the {TC.CYAN}Normal Mode{TC.WHITE}.\n\n"
            "Here you configure scripture_phaser, view the passage "
            "or start a recitation.\n\n"
            f"{TC.CYAN}Normal Mode{TC.WHITE} can be controlled using:\n"
            f"\t{TC.BLUE}H{TC.WHITE} - Prints this help message\n"
            f"\t{TC.BLUE}I{TC.WHITE} - List available translations\n"
            f"\t{TC.BLUE}L{TC.WHITE} - Lists selected reference, random single verse recitations and translation\n"
            f"\t{TC.BLUE}M{TC.WHITE} - Toggles whether or not to practice random single verses\n"
            f"\t{TC.BLUE}N{TC.WHITE} - Toggles whether or not to include the passage numbers\n"
            f"\t{TC.BLUE}P{TC.WHITE} - Practice the current reference\n"
            f"\t{TC.BLUE}R{TC.WHITE} - Sets the reference\n"
            f"\t{TC.BLUE}S{TC.WHITE} - View recitation statistics\n"
            f"\t{TC.BLUE}D{TC.WHITE} - Deletes all past statistics\n"
            f"\t{TC.BLUE}T{TC.WHITE} - Set the translation\n"
            f"\t{TC.BLUE}V{TC.WHITE} - Preview current reference\n"
            f"\t{TC.BLUE}Q{TC.WHITE} - Quits"
        )

    @staticmethod
    def FAST_HELP():
        return (
            f"This is the {TC.CYAN}Fast Recitation Mode{TC.WHITE}.\n\n"
            f"Type the first letter of the next word in the passage "
            f"(it is case sensitive) to advance the recitation by one word. "
            f"If you type the wrong letter twice, the reciation will "
            f"advance by one word and will reveal the correct word in red.\n\n"
            f"The {TC.CYAN}Fast Recitation Mode{TC.WHITE} "
            "can be controlled using:\n"
            f"\t{TC.BLUE}?{TC.WHITE}        - Print this help message\n"
            f"\t{TC.BLUE}Ctrl + c{TC.WHITE} - Stop the recitation\n"
        )

    @staticmethod
    def REFERENCE_PROMPT():
        return "Reference: "

    @staticmethod
    def TRANSLATION_PROMPT():
        return "Translation: "

    @staticmethod
    def NO_EDITOR():
        return (
            f"{TC.RED}No editor found! {TC.WHITE}"
            "Try setting your 'EDITOR' environmental variable and "
            "restarting scripture_phaser or reciting with "
            f"{TC.CYAN}Fast Recitation Mode{TC.WHITE}."
        )

    @staticmethod
    def EXIT_TO_NORMAL_MODE():
        return "Exiting to Normal Mode!"

    def ALL_VERSES_RANKED(self):
        verse_scores, verse_counts = self.api.stats.all_verses_ranked()

        # Used to Make Output Columnar
        max_attempt_width = len(str(max(verse_counts.values())))

        if len(verse_counts) == 0:
            string = "You haven't recorded any attempts yet!"
        else:
            string = ""
            sorted_verses = sorted(verse_scores.items(), key=lambda item: item[1], reverse=True)
            for ref, score in sorted_verses:
                attempt_count = verse_counts[ref]
                if attempt_count == 1:
                    string += "[1 Attempt] "
                    string += " " * max_attempt_width
                else:
                    string += f"[{attempt_count} Attempts] "
                    string += " " * (max_attempt_width - 1)

                score = round(score * 100, 1)
                if score == 100:
                    string += f"({TC.GREEN}{score}%{TC.WHITE}) {ref}\n"
                elif score > 75:
                    string += f"({TC.GREEN}{score}%{TC.WHITE})  {ref}\n"
                elif score >= 10:
                    string += f"({TC.RED}{score}%{TC.WHITE})  {ref}\n"
                else:
                    string += f"({TC.RED}{score}%{TC.WHITE})   {ref}\n"

            string = string[:-1]
        return string

    def STATS_GAMIFICATION(self):
        streak = self.api.stats.get_streak()
        if streak < NUM_DAYS_FOR_GOOD_STREAK:
            streak_str = f"Current Recititation Streak is {TC.RED}{streak}{TC.WHITE}."
        else:
            streak_str = f"Current Recitation Streak is {TC.GREEN}{streak}{TC.WHITE}!"

        past_year_attempt_count = self.api.stats.get_num_attempts_past_year()
        if past_year_attempt_count < GOOD_YEARLY_ATTEMPT_COUNT:
            past_year_attempt_count_str = f"{TC.RED}{past_year_attempt_count}{TC.WHITE} recitations in the past year."
        else:
            past_year_attempt_count_str = f"{TC.GREEN}{past_year_attempt_count}{TC.WHITE} recitations in the past year!"

        attempts_by_day = self.api.stats.get_num_attempts_past_year_by_day()

        max_attempts = max(attempts_by_day)
        few_threshold = 0
        some_threshold = max_attempts / 3
        many_threshold = 2 * max_attempts / 3

        blank, few, some, many = ".", "\u2591", "\u2592", "\u2593"
        for i, day in enumerate(attempts_by_day):
            if day > many_threshold:
                attempts_by_day[i] = many
            elif day > some_threshold:
                attempts_by_day[i] = some
            elif day > few_threshold:
                attempts_by_day[i] = few
            else:
                attempts_by_day[i] = blank

        mon, tue, wed, thr, fri, sat, sun = "MON ", "TUE ", "WED ", "THR ", "FRI ", "SAT ", "SUN "
        mon += "".join(attempts_by_day[::7])
        tue += "".join(attempts_by_day[1::7])
        wed += "".join(attempts_by_day[2::7])
        thr += "".join(attempts_by_day[3::7])
        fri += "".join(attempts_by_day[4::7])
        sat += "".join(attempts_by_day[5::7])
        sun += "".join(attempts_by_day[6::7])

        return (
            f"{streak_str}\n"
            f"{past_year_attempt_count_str}\n\n"
            f"{mon}\n{tue}\n{wed}\n{thr}\n{fri}\n{sat}\n{sun}\n\n"
            f"{many} = >{int(many_threshold)} Attempt" + \
                    ("s" if int(many_threshold) != 1 else "") + "   "
            f"{some} = >{int(some_threshold)} Attempt" + \
                    ("s" if int(some_threshold) != 1 else "") + "   "
            f"{few} = >0 Attempts   "
            ". = 0 Attempts\n"
        )

    def REFERENCE(self):
        return f"Reference:{TC.YELLOW} {self.api.passage.reference.ref_str}{TC.WHITE}"

    def TRANSLATION(self):
        return f"Translation:{TC.YELLOW} {self.api.translation}{TC.WHITE}"

    def RANDOM_SINGLE_VERSE(self):
        return f"Random Single Verse Recitations:{TC.YELLOW} {self.api.random_single_verse}{TC.WHITE}"

    def REQUIRE_PASSAGE_NUMBERS(self):
        return f"Require Passage Numbers:{TC.YELLOW} {self.api.require_passage_numbers}{TC.WHITE}"

    def FAST_RECITATIONS(self):
        return f"Fast Recitations:{TC.YELLOW} {self.api.fast_recitations}{TC.WHITE}"

    def SET_RANDOM_SINGLE_VERSE(self):
        return f"Toggled random single verse recitations to {TC.YELLOW}{self.api.random_single_verse}{TC.WHITE}"

    def SET_PASSAGE_NUMBERS(self):
        return f"Toggled require passage numbers to {TC.YELLOW}{self.api.require_passage_numbers}{TC.WHITE}"

    def SET_FAST_RECITATIONS(self):
        return f"Toggled fast recitations to {TC.YELLOW}{self.api.fast_recitations}{TC.WHITE}"

    def INVALID_TRANSLATION(self):
        return f"{TC.RED}Invalid Translation\n{TC.WHITE}Choose one of:\n{TC.YELLOW}" + "\n".join(self.api.view_translation()) + f"{TC.WHITE}"

    def AVAILABLE_TRANSLATIONS(self):
        return f"Available Translations:\n{TC.YELLOW}" + "\n".join(self.api.view_translation()) + f"{TC.WHITE}"

    def PASSAGE(self):
        return f"{TC.CYAN}{self.api.view_passage()}{TC.WHITE}"

    def TEXT_SCORE(self, score, diff):
        if score == 1.0:
            return f"{TC.GREEN}Perfect!{TC.WHITE}"
        elif score > 0.75:
            return f"{TC.PINK}Not bad: {TC.GREEN}{round(score * 100, 0)}%{TC.WHITE}\n{TC.CYAN}{diff}{TC.WHITE}"
        else:
            return f"{TC.RED}Not quite...{TC.WHITE}\n{TC.CYAN}{diff}{TC.WHITE}"

    def FAST_SCORE(self, score):
        if score == 1.0:
            return f"{TC.GREEN}Perfect!{TC.WHITE}"
        elif score > 0.75:
            return f"{TC.PINK}Not bad: {round(score * 100, 0)}%{TC.WHITE}"
        else:
            return f"{TC.RED}Not quite...{TC.WHITE}"


class CLI:
    def __init__(self):
        self.api = API()
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
                self.editor = None

        self.is_windows = platform.system() == "Windows"

        if not getattr(args, "version") and not getattr(args, "license"):
            self.mainloop()

    def clear(self):
        if self.is_windows:
            os.system("cls")
        else:
            os.system("clear")

    def fast_recitation(self, ref):
        ans = self.api.get_fast_recitation_ans(ref)
        if self.api.random_single_verse:
            # @@@ TODO: The API should be able to pull a verse by reference
            for verse in self.api.passage.verses:
                if verse.reference.ref_str == ref.ref_str:
                    passage_words = verse.text.split()
                    break
        else:
            passage_words = self.api.passage.show().split()

        self.clear()
        print(f"[{TC.CYAN}{ref.ref_str}{TC.WHITE}]")

        i = 0
        n_wrong, n_right = 0, 0
        recitation = []
        try_again = True
        passage_so_far = ""
        while True:
            try:
                key = readchar.readkey()
            except KeyboardInterrupt:
                print(self.messages.EXIT_TO_NORMAL_MODE())
                break

            if key == "?":
                print(self.messages.FAST_HELP())
                continue
            elif key == ans[i]:
                n_right += 1
                try_again = True
                passage_so_far += f"{TC.GREEN}{passage_words[i]}{TC.WHITE} "
                i += 1
                recitation.append(key)
                key_press = f"{TC.GREEN}{key}{TC.WHITE}"
            elif try_again:
                try_again = False
                key_press = f"{TC.RED}{key}{TC.WHITE}"
            else:
                n_wrong += 1
                try_again = True
                passage_so_far += f"{TC.RED}{passage_words[i]}{TC.WHITE} "
                i += 1
                recitation.append(key)
                key_press = f"{TC.RED}{key}{TC.WHITE}"

            self.clear()
            if len(passage_so_far) > 0:
                print(passage_so_far)
            print(f"[{TC.CYAN}{ref.ref_str}{TC.WHITE}]")
            print("Last Key:", key_press)

            if i == len(passage_words):
                score = self.api.finish_recitation(ref, recitation)
                print(self.messages.FAST_SCORE(score))
                break

    def text_recitation(self, ref):
        if self.editor is None:
            print(self.messages.NO_EDITOR())
        else:
            if self.is_windows:
                windows_filename = f"{ref.ref_str}".replace(":", ";")
                filename = self.api.cache_path / windows_filename
            else:
                filename = self.api.cache_path / f"{ref.ref_str}"

            filename.touch(exist_ok=True)
            subprocess.run([self.editor, filename])

            if not filename.exists():
                text = ""
            else:
                with open(filename, "r") as file:
                    text = file.readlines()
                    text = "".join(text).strip()

                if filename.exists():
                    os.remove(filename)

            score = self.api.finish_recitation(ref, text)
            ans = self.api.get_recitation_ans(ref)

            diff = ""
            result = SequenceMatcher(a=text, b=ans).get_opcodes()
            for tag, i1, i2, j1, j2 in result:
                if tag == "replace":
                    segment = f"{TC.RED}{text[i1:i2]}{TC.GREEN}{ans[j1:j2]}{TC.WHITE}"
                    segment = segment.replace(" ", "_")
                    segment = segment.replace("\n", "\\n")
                    diff += segment
                elif tag == "delete":
                    segment = f"{TC.RED}{text[i1:i2]}{TC.WHITE}"
                    segment = segment.replace(" ", "_")
                    segment = segment.replace("\n", "\\n")
                    diff += segment
                elif tag == "insert":
                    segment = f"{TC.GREEN}{ans[j1:j2]}{TC.WHITE}"
                    segment = segment.replace(" ", "_")
                    segment = segment.replace("\n", "\\n")
                    diff += segment
                elif tag == "equal":
                    diff += f"{TC.CYAN}{text[i1:i2]}{TC.WHITE}"

            print(self.messages.TEXT_SCORE(score, diff))

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
                print(self.messages.RANDOM_SINGLE_VERSE())
                print(self.messages.REQUIRE_PASSAGE_NUMBERS())
                print(self.messages.FAST_RECITATIONS())

            # Set (Toggle) Random Single Verse
            elif user_input == "m" or user_input == "single":
                self.api.set_random_single_verse()
                print(self.messages.SET_RANDOM_SINGLE_VERSE())

            # Set (Toggle) the Passage Numbers
            elif user_input == "n" or user_input == "numbers":
                self.api.set_require_passage_numbers()
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
                    if self.api.fast_recitations:
                        self.fast_recitation(reference)
                    else:
                        self.text_recitation(reference)

            # Show Stats
            elif user_input == "s" or user_input == "stats":
                print(self.messages.STATS_GAMIFICATION())
                print(self.messages.ALL_VERSES_RANKED())

            # Reset Statistics
            elif user_input == "d" or user_input == "delete":
                confirmation = input(self.messages.STATS_RESET_WARNING()).strip().lower()
                if confirmation == "y" or confirmation == "yes":
                    self.api.stats.reset_db()
                    print(self.messages.STATS_RESET())

            # Print Help
            else:
                print(self.messages.HELP())
