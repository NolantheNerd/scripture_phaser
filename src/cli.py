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
from src.enums import VERSION
from src.enums import RELEASE_DATE
from src.enums import license_text
from difflib import SequenceMatcher
from src.enums import TermColours as TC
from src.exceptions import NoReferences
from src.exceptions import EditorNotFound
from src.exceptions import InvalidTranslation
from src.reference import Reference

NUM_DAYS_FOR_GOOD_STREAK: int = 7
GOOD_YEARLY_ATTEMPT_COUNT: int = 180
GOOD_SCORE: float = 0.75


class CLISTR:
    def __init__(self, api: API) -> None:
        self.api = api

    @staticmethod
    def CLI_PROMPT() -> str:
        return "> "

    @staticmethod
    def DESCRIPTION() -> str:
        return "scripture_phaser helps you to memorize the Bible."

    @staticmethod
    def LICENSE() -> str:
        return license_text

    @staticmethod
    def VERSION() -> str:
        return f"scripture_phaser version {VERSION}, Release Date: {RELEASE_DATE}"

    @staticmethod
    def VERSION_HELP() -> str:
        return "show the version number and release date"

    @staticmethod
    def LICENSE_HELP() -> str:
        return "show the license"

    @staticmethod
    def WELCOME() -> str:
        return (
            "scripture_phaser helps you to memorize the Bible.\n"
            "Copyright (C) 2023-2024 Nolan McMahon"
        )

    @staticmethod
    def NO_REFERENCE() -> str:
        return f"Reference:{TC.RED} No reference set{TC.WHITE}"

    @staticmethod
    def STATS_RESET_WARNING() -> str:
        return (
            f"Are you sure that you want to reset your statistics? [{TC.RED}y{TC.WHITE}/{TC.GREEN}N{TC.WHITE}] "
        )

    @staticmethod
    def STATS_RESET() -> str:
        return f"Statistics reset{TC.WHITE}"

    @staticmethod
    def HELP() -> str:
        return (
            f"This is the {TC.CYAN}Normal Mode{TC.WHITE}.\n\n"
            "Here you configure scripture_phaser, view the passage "
            "or start a recitation.\n\n"
            f"{TC.CYAN}Normal Mode{TC.WHITE} can be controlled using:\n"
            f"\t{TC.BLUE}H{TC.WHITE} - Prints this help message\n"
            f"\t{TC.BLUE}I{TC.WHITE} - List available translations\n"
            f"\t{TC.BLUE}L{TC.WHITE} - Lists selected reference, random single verse recitations and translation\n"
            f"\t{TC.BLUE}M{TC.WHITE} - Toggles whether or not to practice random single verses\n"
            f"\t{TC.BLUE}N{TC.WHITE} - Toggles whether or not to include the reference numbers\n"
            f"\t{TC.BLUE}P{TC.WHITE} - Practice the current reference\n"
            f"\t{TC.BLUE}R{TC.WHITE} - Sets the reference\n"
            f"\t{TC.BLUE}S{TC.WHITE} - View recitation statistics\n"
            f"\t{TC.BLUE}D{TC.WHITE} - Deletes all past statistics\n"
            f"\t{TC.BLUE}T{TC.WHITE} - Set the translation\n"
            f"\t{TC.BLUE}V{TC.WHITE} - Preview current reference\n"
            f"\t{TC.BLUE}Q{TC.WHITE} - Quits"
        )

    @staticmethod
    def FAST_HELP() -> str:
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
    def REFERENCE_PROMPT() -> str:
        return "Reference: "

    @staticmethod
    def TRANSLATION_PROMPT() -> str:
        return "Translation: "

    @staticmethod
    def NO_EDITOR() -> str:
        return (
            f"{TC.RED}No editor found! {TC.WHITE}"
            "Try setting your 'EDITOR' environmental variable and "
            "restarting scripture_phaser or reciting with "
            f"{TC.CYAN}Fast Recitation Mode{TC.WHITE}."
        )

    @staticmethod
    def EXIT_TO_NORMAL_MODE() -> str:
        return "Exiting to Normal Mode!"

    @staticmethod
    def CONFIRM_REFERENCE_DELETION() -> str:
        return "Are you sure that you want to delete the selected references? [y/N] "

    def ALL_VERSES_RANKED(self) -> str:
        verse_scores, verse_counts = self.api.stats.all_verses_ranked()

        if len(verse_counts) == 0:
            string = "You haven't recorded any attempts yet!"
        else:
            # Used to Make Output Columnar
            max_attempt_width = len(str(max(verse_counts.values())))

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

    def STATS_GAMIFICATION(self) -> str:
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

    def REFERENCE(self) -> str:
        try:
            return f"References:{TC.YELLOW} {"\t, ".join(self.api.list_references())}{TC.WHITE}"
        except NoReferences:
            return f"Reference:{TC.RED} No references set{TC.WHITE}"

    def TRANSLATION(self) -> str:
        return f"Translation:{TC.YELLOW} {self.api.translation}{TC.WHITE}"

    def SINGLE_VERSE_RECITATIONS(self) -> str:
        return f"Single Verse Recitations:{TC.YELLOW} {self.api.one_verse_recitation}{TC.WHITE}"

    def INLCUDE_VERSE_NUMBERS(self) -> str:
        return f"Include Verse Numbers:{TC.YELLOW} {self.api.include_verse_numbers}{TC.WHITE}"

    def FAST_RECITATIONS(self) -> str:
        return f"Fast Recitations:{TC.YELLOW} {self.api.fast_recitations}{TC.WHITE}"

    def SET_ONE_VERSE_RECITATION(self) -> str:
        return f"Toggled recitations to {TC.YELLOW}{self.api.random_single_verse}{TC.WHITE}"

    def SET_VERSE_NUMBERS(self) -> str:
        return f"Toggled include verse numbers to {TC.YELLOW}{self.api.include_verse_numbers}{TC.WHITE}"

    def SET_FAST_RECITATIONS(self) -> str:
        return f"Toggled fast recitations to {TC.YELLOW}{self.api.fast_recitations}{TC.WHITE}"

    def INVALID_TRANSLATION(self) -> str:
        return f"{TC.RED}Invalid Translation\n{TC.WHITE}Choose one of:\n{TC.YELLOW}" + "\n".join(self.api.view_translation()) + f"{TC.WHITE}"

    def AVAILABLE_TRANSLATIONS(self) -> str:
        return f"Available Translations:\n{TC.YELLOW}" + "\n".join(self.api.view_translations()) + f"{TC.WHITE}"

    def PASSAGE(self) -> str:
        try:
            return f"{TC.CYAN}{self.api.view_passage()}{TC.WHITE}"
        except NoReferences:
            return f"Reference:{TC.RED} No references set{TC.WHITE}"

    def TEXT_SCORE(self, score: float, diff: str) -> str:
        if score == 1.0:
            return f"({TC.GREEN}100%{TC.WHITE})"
        elif score > GOOD_SCORE:
            return f"({TC.GREEN}{round(score * 100, 0)}%{TC.WHITE})\n{TC.CYAN}{diff}{TC.WHITE}"
        else:
            return f"({TC.RED}{round(score * 100, 0)}%{TC.WHITE})\n{TC.CYAN}{diff}{TC.WHITE}"

    def FAST_SCORE(self, score: float) -> str:
        if score == 1.0:
            return f"({TC.GREEN}100%{TC.WHITE})"
        elif score > 0.75:
            return f"({TC.GREEN}{round(score * 100, 0)}%{TC.WHITE})"
        else:
            return f"({TC.RED}{round(score * 100, 0)}%{TC.WHITE})"


class CLI:
    def __init__(self) -> None:
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

    def clear(self) -> None:
        if self.is_windows:
            os.system("cls")
        else:
            os.system("clear")

    def fast_recitation(self, ref: Reference) -> None:
        ans = self.api.get_fast_recitation_ans(ref)
        if self.api.random_single_verse:
            # @@@ TODO: The API should be able to pull a verse by reference
            # @@@ TODO: This is broken
            #for verse in self.api.passage.verses:
                #if verse.reference.ref_str == ref.ref_str:
                    #passage_words = verse.text.split()
                    #break
            pass
        else:
            passage_words = self.api.passage.show().split()

        self.clear()
        print(f"[{TC.CYAN}{ref.ref_str}{TC.WHITE}]")

        i = 0
        n_wrong, n_right = 0, 0
        recitation = ""
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
                recitation += key
                key_press = f"{TC.GREEN}{key}{TC.WHITE}"
            elif try_again:
                try_again = False
                key_press = f"{TC.RED}{key}{TC.WHITE}"
            else:
                n_wrong += 1
                try_again = True
                passage_so_far += f"{TC.RED}{passage_words[i]}{TC.WHITE} "
                i += 1
                recitation += key
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

    def text_recitation(self, ref: Reference) -> None:
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

    def referenceloop(self) -> None:
        print(self.messages.REFERENCE_WELCOME())
        selected_reference_indices = []

        while True:
            try:
                key = readchar.readkey().lower()
            except KeyboardInterrupt:
                break

            # Exit
            if user_input == "q":
                break

            # Add Reference
            elif user_input == "a":
                ref_str = input(self.messages.REFERENCE_PROMPT())
                self.api.add_reference(ref_str)

            # Delete Selected References
            elif user_input == "d":
                confirmation = input(self.messages.CONFIRM_REFERENCE_DELETION()).lower()
                if confirmation == "y" or confirmation == "yes":
                    for index in selected_reference_indices:
                        self.api.delete_reference(index)

            # Toggle Reference Selection
            elif user_input == " ":
                pass

            # Practice Reference
            elif user_input == "p":
                pass

    def mainloop(self) -> None:
        print(self.messages.WELCOME())

        while True:
            try:
                user_input = input(self.messages.CLI_PROMPT()).strip().lower()
            except KeyboardInterrupt:
                break

            # Exit
            if user_input == "q" or user_input == "quit":
                break

            # Current State
            elif user_input == "l" or user_input == "list":
                print(self.messages.REFERENCE())
                print(self.messages.TRANSLATION())
                print(self.messages.SINGLE_VERSE_RECITATIONS())
                print(self.messages.INLCUDE_VERSE_NUMBERS())
                print(self.messages.FAST_RECITATIONS())

            # Set (Toggle) Random Single Verse
            elif user_input == "m" or user_input == "single":
                self.api.toggle_one_verse_recitation()
                print(self.messages.SET_ONE_VERSE_RECITATION())

            # Set (Toggle) the Verse Numbers
            elif user_input == "n" or user_input == "numbers":
                self.api.toggle_include_verse_numbers()
                print(self.messages.SET_VERSE_NUMBERS())

            # Set (Toggle) Fast Recitations
            elif user_input == "f" or user_input == "fast":
                self.api.toggle_fast_recitations()
                print(self.messages.SET_FAST_RECITATIONS())

            # @@@ FIX
            # Set Reference
            elif user_input == "r" or user_input == "reference":
                ref_str = input(self.messages.REFERENCE_PROMPT())
                # @@@ TODO: Rather not make a Reference IN the CLI
                self.api.set_passage(Reference(ref_str))

            # @@@ FIX
            # View Passage
            elif user_input == "v" or user_input == "view":
                print(self.messages.PASSAGE())

            # Set Translation
            elif user_input == "t" or user_input == "translation":
                translation = input(self.messages.TRANSLATION_PROMPT()).upper()
                try:
                    self.api.set_translation(translation)
                except InvalidTranslation:
                    print(self.messages.INVALID_TRANSLATION())

            # View Translations
            elif user_input == "i" or user_input == "inquire":
                print(self.messages.AVAILABLE_TRANSLATIONS())

            # @@@ FIX
            # Practice Passage
            elif user_input == "p" or user_input == "practice":
                try:
                    reference = self.api.get_reference()
                    if self.api.fast_recitations:
                        self.fast_recitation(reference)
                    else:
                        self.text_recitation(reference)
                except NoReferences:
                    print(self.messages.NO_REFERENCE())

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
