# scripture_phaser helps you to memorize the Bible.
# Copyright (C) 2023-2025 Nolan McMahon
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

from peewee import fn
from dataclasses import dataclass
from itertools import accumulate
from fastapi import APIRouter
from scripture_phaser.backend.exceptions import InvalidReference
from scripture_phaser.backend.enums import Bible, Bible_Books, Reverse_Bible_Books
from scripture_phaser.backend.user import User, validate_token
from scripture_phaser.backend.models import User as UserModel
from scripture_phaser.backend.models import Reference as ReferenceModel
from scripture_phaser.backend.models import Recitation as RecitationModel

api = APIRouter(tags=["Reference"])


@dataclass
class PassageID:
    start: int
    end: int


@dataclass
class VerseTriplet:
    book: int
    chapter: int
    verse: int


@dataclass
class Reference:
    ref: str
    passage: PassageID
    first: VerseTriplet
    last: VerseTriplet


@api.post("/new_reference")
def new_reference(ref: str, translation: str, user: User | None) -> Reference:
    reference = string_to_reference(ref)
    if user is not None:
        validate_token(user.token)
        user_model = UserModel.get(UserModel.username == user.username)
        ReferenceModel.get_or_create(
            user=user_model, ref=reference.ref, translation=translation
        )
    return reference


@api.delete("/delete_reference")
def delete_reference(ref: str, translation: str, user: User) -> None:
    validate_token(user.token)
    reference = ReferenceModel.select().where(
        (ReferenceModel.ref == ref) & (ReferenceModel.translation == translation)
    )

    user_model = UserModel.get(UserModel.username == user.username)
    n_ref_recitations = RecitationModel.select(fn.COUNT).where(
        (RecitationModel.reference == reference)
        & (RecitationModel.user == user_model)
    )

    if n_ref_recitations > 0:
        reference.active = False
    else:
        reference.delete_instance()
    reference.save()


@api.get("/list_references")
def list_references(user: User) -> list[Reference]:
    validate_token(user.token)
    return list(ReferenceModel.select().join(UserModel).where(ReferenceModel.user.username == user.username))


def string_to_reference(ref: str) -> Reference:
    first_verse, last_verse = _interpret_reference(ref)
    passage = _reference_to_id(first_verse, last_verse)
    _validate_reference(passage, first_verse, last_verse)
    ref = _standardize_reference(first_verse, last_verse)
    return Reference(ref, passage, first_verse, last_verse)


def id_to_reference(start_id: int, end_id: int | None = None) -> Reference:
    first_verse = _id_to_reference(start_id)
    if end_id is not None:
        last_verse = _id_to_reference(end_id)
    else:
        end_id = start_id
        last_verse = first_verse

    passage = PassageID(start_id, end_id)
    _validate_reference(passage, first_verse, last_verse)
    ref = _standardize_reference(first_verse, last_verse)
    return Reference(ref, passage, first_verse, last_verse)


def _interpret_reference(ref: str) -> tuple[VerseTriplet, VerseTriplet]:
    ref = _clean_reference(ref)

    # Handle a Single Whole Book Reference [Genesis]
    if ref in Reverse_Bible_Books:
        book_start = Reverse_Bible_Books.get(ref, -1)
        book_end = book_start
        chapter_start = 0
        chapter_end = len(Bible[book_end]) - 1
        verse_start = 0
        verse_end = Bible[book_end][chapter_end] - 1

    else:
        ref_components = ref.split(" - ")

        # No Split Reference (no "-")
        if len(ref_components) == 1:
            split_components = ref_components[0].split(" ")

            # Get Book Name (Even if it is Multiple Words)
            i = 0
            while i < len(split_components) and split_components[i].isalpha():
                i += 1
            book_start = book_end = Reverse_Bible_Books.get(
                " ".join(split_components[:i]), -1
            )

            # Book Name is not in the Bible (Billy)
            if book_start == -1:
                raise InvalidReference()

            # Get Chapter:Verse Split
            loc_components = split_components[-1].split(":")

            if len(loc_components) == 1:
                # Handle Single Chapter Books (Jude 10)
                if len(Bible[book_start]) == 1:
                    chapter_start = chapter_end = 0
                    verse_start = verse_end = int(loc_components[0]) - 1
                # Handle Entire Chapter References (John 1)
                else:
                    chapter_start = chapter_end = int(loc_components[0]) - 1
                    verse_start = 0
                    verse_end = Bible[book_start][chapter_start] - 1

            # Handle Single Verse References [John 1:1]
            else:
                chapter_start = chapter_end = int(loc_components[0]) - 1
                verse_start = verse_end = int(loc_components[1]) - 1

        # Split Reference (one "-")
        elif len(ref_components) == 2:
            # Handle First Half of Split
            split_components = ref_components[0].split(" ")

            # Get Book Name (Even if it is Multiple Words)
            i = 0
            while i < len(split_components) and split_components[i].isalpha():
                i += 1
            book_start = Reverse_Bible_Books.get(" ".join(split_components[:i]), -1)

            # Book Name is not in the Bible (Billy)
            if book_start == -1:
                raise InvalidReference()

            # Get Chapter:Verse Split (if part of reference isn't book name)
            if not split_components[-1].isalpha():
                loc_components = split_components[-1].split(":")

                if len(loc_components) == 1:
                    # Handle Single Chapter Books (Jude 10)
                    if len(Bible[book_start]) == 1:
                        chapter_start = 0
                        verse_start = int(loc_components[0]) - 1
                    # Handle Entire Chapter References (John 1)
                    else:
                        chapter_start = int(loc_components[0]) - 1
                        verse_start = 0

                # Handle Single Verse References [John 1:1]
                else:
                    chapter_start = int(loc_components[0]) - 1
                    verse_start = int(loc_components[1]) - 1
            # Handle Just a Book (Genesis)
            else:
                chapter_start = verse_start = 0

            # Handle Second Half of Split
            split_components = ref_components[1].split(" ")

            # Check for Book Name
            if split_components[0].isalpha():
                # Get Book Name (Even if it is Multiple Words)
                i = 0
                while i < len(split_components) and split_components[i].isalpha():
                    i += 1
                book_end = Reverse_Bible_Books.get(" ".join(split_components[:i]), -1)
            # Second Book is Not Specified [John 1:1 - 1:2]
            else:
                book_end = book_start

            # Book Name is not in the Bible (Billy)
            if book_end == -1:
                raise InvalidReference()

            # Get Chapter:Verse Split (if part of reference isn't book name)
            if not split_components[-1].isalpha():
                loc_components = split_components[-1].split(":")

                if len(loc_components) == 1:
                    # Handle Single Chapter Books (Jude 10)
                    if len(Bible[book_end]) == 1:
                        chapter_end = 0
                        verse_end = int(loc_components[0]) - 1
                    # Handle Entire Chapter References (John 1)
                    # Handle Chapter Ranges (John 1 - 2)
                    elif book_end != book_start or ":" not in ref_components[0]:
                        chapter_end = int(loc_components[0]) - 1
                        verse_end = Bible[book_end][chapter_end] - 1
                    # Handle Single Values As Verses not Chapters (John 1:4 - 6)
                    else:
                        chapter_end = chapter_start
                        verse_end = int(loc_components[0]) - 1

                # Handle Single Verse References [John 1:1]
                else:
                    chapter_end = int(loc_components[0]) - 1
                    verse_end = int(loc_components[1]) - 1
            # Handle Just a Book (Genesis)
            else:
                chapter_end = len(Bible[book_end]) - 1
                verse_end = Bible[book_end][chapter_end] - 1

        # More than One Split is No Good (two+ "-")
        else:
            raise InvalidReference()

    start_verse = VerseTriplet(book_start, chapter_start, verse_start)
    end_verse = VerseTriplet(book_end, chapter_end, verse_end)
    return start_verse, end_verse


def _standardize_reference(first: VerseTriplet, last: VerseTriplet) -> str:
    one_book = first.book == last.book
    one_chapter = one_book and first.chapter == last.chapter
    one_verse = one_chapter and first.verse == last.verse
    entire_book = (
        one_book
        and first.chapter == 0
        and last.chapter == len(Bible[first.book]) - 1
        and first.verse == 0
        and last.verse == Bible[last.book][last.chapter] - 1
    )
    many_entire_books = (
        first.chapter == 0
        and last.chapter == len(Bible[last.book]) - 1
        and first.verse == 0
        and last.verse == Bible[last.book][last.chapter] - 1
    )
    entire_chapter = (
        one_book
        and one_chapter
        and first.verse == 0
        and last.verse == Bible[first.book][first.chapter] - 1
    )
    one_book_entire_chapters = (
        one_book
        and first.verse == 0
        and last.verse == Bible[last.book][last.chapter] - 1
    )
    many_books_entire_chapters = (
        not one_book
        and first.verse == 0
        and last.verse == Bible[last.book][last.chapter] - 1
    )
    first_book_is_single_chapter = len(Bible[first.book]) == 1
    last_book_is_single_chapter = len(Bible[last.book]) == 1

    if entire_book:
        # Genesis
        return f"{Bible_Books[first.book]}"
    if many_entire_books:
        # Genesis - Leviticus
        return f"{Bible_Books[first.book]} - {Bible_Books[last.book]}"
    if entire_chapter:
        # Genesis 1
        return f"{Bible_Books[first.book]} {first.chapter + 1}"
    if one_book_entire_chapters:
        # Genesis 1-3
        return f"{Bible_Books[first.book]} {first.chapter + 1}-{last.chapter + 1}"
    if (
        many_books_entire_chapters
        and not first_book_is_single_chapter
        and not last_book_is_single_chapter
    ):
        # Genesis 50 - Exodus 1
        return (
            f"{Bible_Books[first.book]} {first.chapter + 1} - "
            f"{Bible_Books[last.book]} {last.chapter + 1}"
        )
    if (
        many_books_entire_chapters
        and first_book_is_single_chapter
        and not last_book_is_single_chapter
    ):
        # Jude - Revelation 1
        return (
            f"{Bible_Books[first.book]} - {Bible_Books[last.book]} {last.chapter + 1}"
        )
    if (
        many_books_entire_chapters
        and not first_book_is_single_chapter
        and last_book_is_single_chapter
    ):
        # James 1 - Jude
        return f"{Bible_Books[first.book]} {first.chapter + 1} - {Bible_Books[last.book]}"
    if one_verse and first_book_is_single_chapter:
        # Jude 1
        return f"{Bible_Books[first.book]} " f"{first.verse + 1}"
    if one_verse and not first_book_is_single_chapter:
        # Genesis 1:1
        return f"{Bible_Books[first.book]} " f"{first.chapter + 1}:{first.verse + 1}"
    if one_chapter and first_book_is_single_chapter:
        # Jude 2-4
        return f"{Bible_Books[first.book]} " f"{first.verse + 1}-{last.verse + 1}"
    if one_chapter and not first_book_is_single_chapter:
        # Genesis 1:2-4
        return (
            f"{Bible_Books[first.book]} "
            f"{first.chapter + 1}:"
            f"{first.verse + 1}-{last.verse + 1}"
        )
    if one_book:  # Implicitly the book is not a single chapter
        # Genesis 1:2-2:3
        return (
            f"{Bible_Books[first.book]} "
            f"{first.chapter + 1}:{first.verse + 1}-"
            f"{last.chapter + 1}:{last.verse + 1}"
        )
    if not one_book and first_book_is_single_chapter and last_book_is_single_chapter:
        # Obadiah 1 - Jude 2
        return (
            f"{Bible_Books[first.book]} {first.verse + 1} "
            f"- {Bible_Books[last.book]} {last.verse + 1}"
        )
    if (
        not one_book
        and not first_book_is_single_chapter
        and last_book_is_single_chapter
    ):
        # James 1:1 - Jude 2
        return (
            f"{Bible_Books[first.book]} {first.chapter + 1}:"
            f"{first.verse + 1} - {Bible_Books[last.book]} "
            f"{last.verse + 1}"
        )
    if (
        not one_book
        and first_book_is_single_chapter
        and not last_book_is_single_chapter
    ):
        # Jude 2 - Revelation 1:1
        return (
            f"{Bible_Books[first.book]} {first.verse + 1} "
            f"- {Bible_Books[last.book]} {last.chapter + 1}:"
            f"{last.verse + 1}"
        )
    if (
        not one_book
        and not first_book_is_single_chapter
        and not last_book_is_single_chapter
    ):
        # Genesis 1:1 - Exodus 2:2
        return (
            f"{Bible_Books[first.book]} {first.chapter + 1}:"
            f"{first.verse + 1} - {Bible_Books[last.book]} "
            f"{last.chapter + 1}:{last.verse + 1}"
        )

    return ""


def _reference_to_id(start: VerseTriplet, end: VerseTriplet) -> PassageID:
    start_id = sum([sum(book) for book in Bible[: start.book]])
    start_id += sum(Bible[start.book][: start.chapter])
    start_id += start.verse

    if start != end:
        end_id = sum([sum(book) for book in Bible[: end.book]])
        end_id += sum(Bible[end.book][: end.chapter])
        end_id += end.verse
    else:
        end_id = start_id

    return PassageID(start_id, end_id)


def _id_to_reference(verse_id: int) -> VerseTriplet:
    verse_sums = list(accumulate([sum(book) for book in Bible]))
    book_id = [verse_id < bound for bound in verse_sums].index(True)

    if book_id > 0:
        verse_id -= verse_sums[book_id - 1]

    book_sums = list(accumulate(Bible[book_id]))
    chapter_id = [verse_id < bound for bound in book_sums].index(True)

    if chapter_id > 0:
        verse_id -= book_sums[chapter_id - 1]

    return VerseTriplet(book_id, chapter_id, verse_id)


def _clean_reference(ref: str) -> str:
    ref = " ".join(ref.split())  # Multiple Whitespaces -> One Whitespace
    ref = ref.strip().lower().title()

    new_ref = ""
    prev_char = ""
    for i, char in enumerate(ref):
        next_char = ref[min(len(ref) - 1, i + 1)]
        # Insert Space After Book Name and Before Chapter/Verse Number
        if char.isdigit() and prev_char.isalpha():
            new_ref += " "

        # Insert Space After Verse Number and Before Second Book Name
        elif char.isalpha() and prev_char.isdigit():
            new_ref += " "

        # Insert Space Between Number and "-"
        elif char == "-" and prev_char != " " and prev_char != "":
            new_ref += " "

        # Insert Space Between "-" and Number/Book
        elif prev_char == "-" and char != " ":
            new_ref += " "

        elif char == " ":
            # Remove Space Before ":" and After Chapter Number
            if prev_char.isdigit() and next_char == ":":
                prev_char = ref[max(0, i)]
                continue
            # Remove Space After ":" and Before Verse Number
            elif prev_char == ":" and next_char.isdigit():
                prev_char = ref[max(0, i)]
                continue

        prev_char = ref[max(0, i)]
        new_ref += ref[i]

    new_ref = _reference_replacements(new_ref)

    return new_ref


def _reference_replacements(ref: str) -> str:
    source = [
        ".",
        "Psalm",
        "Psalmss",
        "First",
        "Second",
        "Third",
        "1 Samuel",
        "1 Kings",
        "1 Chronicles",
        "1 Corinthians",
        "1 Thessalonians",
        "1 Timothy",
        "1 Peter",
        "1 John",
        "2 Samuel",
        "2 Kings",
        "2 Chronicles",
        "2 Corinthians",
        "2 Thessalonians",
        "2 Timothy",
        "2 Peter",
        "2 John",
        "3 John",
        "Gen ",
        "Ex ",
        "Lev ",
        "Num ",
        "Deut ",
        "Josh ",
        "Judg ",
        "1Sam ",
        "1sam ",
        "1 Sam ",
        "2Sam ",
        "2sam ",
        "2 Sam ",
        "1Chron ",
        "1chron ",
        "1 Chron ",
        "Neh ",
        "Est ",
        "Ps ",
        "Prov ",
        "Eccles ",
        "Song ",
        "Isa ",
        "Jer ",
        "Lam ",
        "Ezek ",
        "Dan ",
        "Hos ",
        "Obad ",
        "Mic ",
        "Nah ",
        "Hab ",
        "Zeph ",
        "Hag ",
        "Zech ",
        "Mal ",
        "Matt ",
        "Rom ",
        "1Cor ",
        "1cor ",
        "1 Cor ",
        "2Cor ",
        "2cor ",
        "2 Cor ",
        "Gal ",
        "Eph ",
        "Phil ",
        "Col ",
        "1Thess ",
        "1thess ",
        "1 Thess ",
        "2Thess ",
        "2thess ",
        "2 Thess ",
        "1Tim ",
        "1tim ",
        "1 Tim ",
        "2Tim ",
        "2tim ",
        "2 Tim ",
        "Philem ",
        "Heb ",
        "1Pet ",
        "1pet ",
        "1 Pet ",
        "2Pet ",
        "2pet ",
        "2 Pet ",
        "Rev ",
    ]

    replacement = [
        "",
        "Psalms",
        "Psalms",
        "One",
        "Two",
        "Three",
        "One Samuel",
        "One Kings",
        "One Chronicles",
        "One Corinthians",
        "One Thessalonians",
        "One Timothy",
        "One Peter",
        "One John",
        "Two Samuel",
        "Two Kings",
        "Two Chronicles",
        "Two Corinthians",
        "Two Thessalonians",
        "Two Timothy",
        "Two Peter",
        "Two John",
        "Three John",
        "Genesis ",
        "Exodus ",
        "Leviticus ",
        "Numbers ",
        "Deuteronomy ",
        "Joshua ",
        "Judges ",
        "One Samuel ",
        "One Samuel ",
        "One Samuel ",
        "Two Samuel ",
        "Two Samuel ",
        "Two Samuel ",
        "One Chronicles ",
        "One Chronicles ",
        "One Chronicles ",
        "Nehemiah ",
        "Esther ",
        "Psalms ",
        "Proverbs ",
        "Ecclesiastes ",
        "Song of Songs ",
        "Isaiah ",
        "Jeremiah ",
        "Lamentations ",
        "Ezekiel ",
        "Daniel ",
        "Hosea ",
        "Obadiah ",
        "Micah ",
        "Nahum ",
        "Habakkuk ",
        "Zephaniah ",
        "Haggai ",
        "Zechariah ",
        "Malachi ",
        "Matthew ",
        "Romans ",
        "One Corinthians ",
        "One Corinthians ",
        "One Corinthians ",
        "Two Corinthians ",
        "Two Corinthians ",
        "Two Corinthians ",
        "Galatians ",
        "Ephesians ",
        "Philippians ",
        "Colossians ",
        "One Thessalonians ",
        "One Thessalonians ",
        "One Thessalonians ",
        "Two Thessalonians ",
        "Two Thessalonians ",
        "Two Thessalonians ",
        "One Timothy ",
        "One Timothy ",
        "One Timothy ",
        "Two Timothy ",
        "Two Timothy ",
        "Two Timothy ",
        "Philemon ",
        "Hebrews ",
        "One Peter ",
        "One Peter ",
        "One Peter ",
        "Two Peter ",
        "Two Peter ",
        "Two Peter ",
        "Revelation ",
    ]

    for i in range(len(source)):
        ref = ref.replace(source[i], replacement[i])
    return ref


def _validate_reference(
    passage: PassageID, first_verse: VerseTriplet, last_verse: VerseTriplet
) -> None:
    ref_out_of_order = passage.start > passage.end
    if ref_out_of_order:
        raise InvalidReference()
    books_out_of_order = first_verse.book > last_verse.book
    if books_out_of_order:
        raise InvalidReference()
    start_chapter_in_book = first_verse.chapter < len(Bible[first_verse.book])
    if not start_chapter_in_book:
        raise InvalidReference()
    end_chapter_in_book = last_verse.chapter < len(Bible[last_verse.book])
    if not end_chapter_in_book:
        raise InvalidReference()
    start_verse_in_chapter = (
        first_verse.verse < Bible[first_verse.book][first_verse.chapter]
    )
    if not start_verse_in_chapter:
        raise InvalidReference()
    end_verse_in_chapter = (
        last_verse.verse < Bible[last_verse.book][last_verse.chapter]
    )
    if not end_verse_in_chapter:
        raise InvalidReference()
