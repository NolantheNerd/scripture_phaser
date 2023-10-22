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

import enum

class _Defaults(enum.Enum):
    tui = True
    translation = "NIV"
    random_mode = False
    esv_api_key = None

class App(enum.Enum):
    Name = "scripture_phaser"
    Database = "scripture_phaser_db"
    Defaults = _Defaults

class Translations(enum.Enum):
    ESV = "English Standard Version"
    NIV = "New International Version"
    KJV = "King James Version"
    NKJV = "New King James Version"
    NLT = "New Living Translation"
    NASB = "New American Standard Bible"
    NRSV = "New Revised Standard Version"
    WEB = "World English Bible"
    BBE = "Bible in Basic English"

class Agents(enum.Enum):
    ESVBGW = "ESV"
    NIVBGW = "NIV"
    NKJVBGW = "NKJV"
    NLTBGW = "NLT"
    NRSVBGW = "NRSV"
    NASBBGW = "NASB"
    ESVAPI = "https://api.esv.org/v3/passage/text/?"
    KJVAPI = "https://bible-api.com/"
    WEBAPI = "https://bible-api.com/"
    BBEAPI = "https://bible-api.com/"

Genesis = [31, 25, 24, 26, 32, 22, 24, 22, 29, 32, 32, 20, 18, 24, 21, 16, 27,
           33, 38, 18, 34, 24, 20, 67, 34, 35, 46, 22, 35, 43, 55, 32, 20, 31,
           29, 43, 36, 30, 23, 23, 57, 38, 34, 34, 28, 34, 31, 22, 33, 26]

Exodus = [22, 25, 22, 31, 23, 30, 25, 32, 35, 29, 10, 51, 22, 31, 27, 36, 16,
          27, 25, 26, 36, 31, 33, 18, 40, 37, 21, 43, 46, 38, 18, 35, 23, 35,
          35, 38, 29, 31, 43, 38]

Leviticus = [17, 16, 17, 35, 19, 30, 38, 36, 24, 20, 47, 8, 59, 57, 33, 34, 16,
             30, 37, 27, 24, 33, 44, 23, 55, 46, 34]

Numbers = [54, 34, 51, 49, 31, 27, 89, 26, 23, 36, 35, 16, 33, 45, 41, 50, 13,
           32, 22, 29, 35, 41, 30, 25, 18, 65, 23, 31, 40, 16, 54, 42, 56, 29,
           34, 13]

Deuteronomy = [46, 37, 29, 49, 33, 25, 26, 20, 29, 22, 32, 32, 18, 29, 23, 22,
               20, 22, 21, 20, 23, 30, 25, 22, 19, 19, 26, 68, 29, 20, 30, 52,
               29, 12]

Joshua = [18, 24, 17, 24, 15, 27, 26, 35, 27, 43, 23, 24, 33, 15, 63, 10, 18,
          28, 51, 9, 45, 34, 16, 33]

Judges = [36, 23, 31, 24, 31, 40, 25, 35, 57, 18, 40, 15, 25, 20, 20, 31, 13,
          31, 30, 48, 25]

Ruth = [22, 23, 18, 22]

One_Samuel = [28, 36, 21, 22, 12, 21, 17, 22, 27, 27, 15, 25, 23, 52, 35, 23,
              58, 30, 24, 42, 15, 23, 29, 22, 44, 25, 12, 25, 11, 31, 13]

Two_Samuel = [27, 32, 39, 12, 25, 23, 29, 18, 13, 19, 27, 31, 39, 33, 37, 23,
              29, 33, 43, 26, 22, 51, 39, 25]

One_Kings = [53, 46, 28, 34, 18, 38, 51, 66, 28, 29, 43, 33, 34, 31, 34, 34,
             24, 46, 21, 43, 29, 53]

Two_Kings = [18, 25, 27, 44, 27, 33, 20, 29, 37, 36, 21, 21, 25, 29, 38, 20,
             41, 37, 37, 21, 26, 20, 37, 20, 30]

One_Chronicles = [54, 55, 24, 43, 26, 81, 40, 40, 44, 14, 47, 40, 14, 17, 29,
                  43, 27, 17, 19, 8, 30, 19, 32, 31, 31, 32, 34, 21, 30]

Two_Chronicles = [17, 18, 17, 22, 14, 42, 22, 18, 31, 19, 23, 16, 22, 15, 19,
                  14, 19, 34, 11, 37, 20, 12, 21, 27, 28, 23, 9, 27, 36, 27,
                  21, 33, 25, 33, 27, 23]

Ezra = [11, 70, 13, 24, 17, 22, 28, 36, 15, 44]

Nehemiah = [11, 20, 32, 23, 19, 19, 73, 18, 38, 39, 36, 47, 31]

Esther = [22, 23, 15, 17, 14, 14, 10, 17, 32, 3]

Job = [22, 13, 26, 21, 27, 30, 21, 22, 35, 22, 20, 25, 28, 22, 35, 22, 16, 21,
       29, 29, 34, 30, 17, 25, 6, 14, 23, 28, 25, 31, 40, 22, 33, 37, 16, 33,
       24, 41, 30, 24, 34, 17]

Psalms = [6, 12, 8, 8, 12, 10, 17, 9, 20, 18, 7, 8, 6, 7, 5, 11, 15, 50, 14, 9,
          13, 31, 6, 10, 22, 12, 14, 9, 11, 12, 24, 11, 22, 22, 28, 12, 40, 22,
          13, 17, 13, 11, 5, 26, 17, 11, 9, 14, 20, 23, 19, 9, 6, 7, 23, 13,
          11, 11, 17, 12, 8, 12, 11, 10, 13, 20, 7, 35, 36, 5, 24, 20, 28, 23,
          10, 12, 20, 72, 13, 19, 16, 8, 18, 12, 13, 17, 7, 18, 52, 17, 16, 15,
          5, 23, 11, 13, 12, 9, 9, 5, 8, 28, 22, 35, 45, 48, 43, 13, 31, 7, 10,
          10, 9, 8, 18, 19, 2, 29, 176, 7, 8, 9, 4, 8, 5, 6, 5, 6, 8, 8, 3, 18,
          3, 3, 21, 26, 9, 8, 24, 13, 10, 7, 12, 15, 21, 10, 20, 14, 9, 6]

Proverbs = [33, 22, 35, 27, 23, 35, 27, 36, 18, 32, 31, 28, 25, 35, 33, 33, 28,
            24, 29, 30, 31, 29, 35, 34, 28, 28, 27, 28, 27, 33, 31]

Ecclesiastes = [18, 26, 22, 16, 20, 12, 29, 17, 18, 20, 10, 14]

Song_of_Songs = [17, 17, 11, 16, 16, 13, 13, 14]

Isaiah = [31, 22, 26, 6, 30, 13, 25, 22, 21, 34, 16, 6, 22, 32, 9, 14, 14, 7,
          25, 6, 17, 25, 18, 23, 12, 21, 13, 29, 24, 33, 9, 20, 24, 17, 10, 22,
          38, 22, 8, 31, 29, 25, 28, 28, 25, 13, 15, 22, 26, 11, 23, 15, 12,
          17, 13, 12, 21, 14, 21, 22, 11, 12, 19, 12, 25, 24]

Jeremiah = [19, 37, 25, 31, 31, 30, 34, 22, 26, 25, 23, 17, 27, 22, 21, 21, 27,
            23, 15, 18, 14, 30, 40, 10, 38, 24, 22, 17, 32, 24, 40, 44, 26, 22,
            19, 32, 21, 28, 18, 16, 18, 22, 13, 30, 5, 28, 7, 47, 39, 46, 64,
            34]

Lamentations = [22, 22, 66, 22, 22]

Ezekiel = [28, 10, 27, 17, 17, 14, 27, 18, 11, 22, 25, 28, 23, 23, 8, 63, 24,
           32, 14, 49, 32, 31, 49, 27, 17, 21, 36, 26, 21, 26, 18, 32, 33, 31,
           15, 38, 28, 23, 29, 49, 26, 20, 27, 31, 25, 24, 23, 35]

Daniel = [21, 49, 30, 37, 31, 28, 28, 27, 27, 21, 45, 13]

Hosea = [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9]

Joel = [20, 32, 21]

Amos = [15, 16, 15, 13, 27, 14, 17, 14, 15]

Obadiah = [21]

Jonah = [17, 10, 10, 11]

Micah = [16, 13, 12, 13, 15, 16, 20]

Nahum = [15, 13, 19]

Habakkuk = [17, 20, 19]

Zephaniah = [18, 15, 20]

Haggai = [15, 23]

Zechariah = [21, 13, 10, 14, 11, 15, 14, 23, 17, 12, 17, 14, 9, 21]

Malachi = [14, 17, 18, 6]

Matthew = [25, 23, 17, 25, 48, 34, 29, 34, 38, 42, 30, 50, 58, 36, 39, 28, 27,
           35, 30, 34, 46, 46, 39, 51, 46, 75, 66, 20]

Mark = [45, 28, 35, 41, 43, 56, 37, 38, 50, 52, 33, 44, 37, 72, 47, 20]

Luke = [80, 52, 38, 44, 39, 49, 50, 56, 62, 42, 54, 59, 35, 35, 32, 31, 37, 43,
        48, 47, 38, 71, 56, 53]

John = [51, 25, 36, 54, 47, 71, 53, 59, 41, 42, 57, 50, 38, 31, 27, 33, 26, 40,
        42, 31, 25]

Acts = [26, 47, 26, 37, 42, 15, 60, 40, 43, 48, 30, 25, 52, 28, 41, 40, 34, 28,
        41, 38, 40, 30, 35, 27, 27, 32, 44, 31]

Romans = [32, 29, 31, 25, 21, 23, 25, 39, 33, 21, 36, 21, 14, 26, 33, 25]

One_Corinthians = [31, 16, 23, 21, 13, 20, 40, 13, 27, 33, 34, 31, 13, 40, 58,
                   24]

Two_Corinthians = [24, 17, 18, 18, 21, 18, 16, 24, 15, 18, 33, 21, 14]

Galatians = [24, 21, 29, 31, 26, 18]

Ephesians = [23, 22, 21, 32, 33, 24]

Philippians = [30, 30, 21, 23]

Colossians = [29, 23, 25, 18]

One_Thessalonians = [10, 20, 13, 18, 28]

Two_Thessalonians = [12, 17, 18]

One_Timothy = [20, 15, 16, 16, 25, 21]

Two_Timothy = [18, 26, 17, 22]

Titus = [16, 15, 15]

Philemon = [25]
Hebrews = [14, 18, 19, 16, 14, 20, 28, 13, 28, 39, 40, 29, 25]

James = [27, 26, 18, 17, 20]

One_Peter = [25, 25, 22, 19, 14]

Two_Peter = [21, 22, 18]

One_John = [10, 29, 24, 21, 21]

Two_John = [13]

Three_John = [14]

Jude = [25]

Revelation = [20, 29, 22, 11, 14, 17, 17, 13, 21, 11, 19, 17, 18, 20, 8, 21,
              18, 24, 21, 15, 27, 21]

Bible = [
    Genesis, Exodus, Leviticus, Numbers, Deuteronomy, Joshua, Judges, Ruth,
    One_Samuel, Two_Samuel, One_Kings, Two_Kings, One_Chronicles,
    Two_Chronicles, Ezra, Nehemiah, Esther, Job, Psalms, Proverbs,
    Ecclesiastes, Song_of_Songs, Isaiah, Jeremiah, Lamentations, Ezekiel,
    Daniel, Hosea, Joel, Amos, Obadiah, Jonah, Micah, Nahum, Habakkuk,
    Zephaniah, Haggai, Zechariah, Malachi, Matthew, Mark, Luke, John, Acts,
    Romans, One_Corinthians, Two_Corinthians, Galatians, Ephesians,
    Philippians, Colossians, One_Thessalonians, Two_Thessalonians, One_Timothy,
    Two_Timothy, Titus, Philemon, Hebrews, James, One_Peter, Two_Peter,
    One_John, Two_John, Three_John, Jude, Revelation
]

Bible_Books = {
    0: "Genesis",
    1: "Exodus",
    2: "Leviticus",
    3: "Numbers",
    4: "Deuteronomy",
    5: "Joshua",
    6: "Judges",
    7: "Ruth",
    8: "1 Samuel",
    9: "2 Samuel",
    10: "1 Kings",
    11: "2 Kings",
    12: "1 Chronicles",
    13: "2 Chronicles",
    14: "Ezra",
    15: "Nehemiah",
    16: "Esther",
    17: "Job",
    18: "Psalms",
    19: "Proverbs",
    20: "Ecclesiastes",
    21: "Song of Songs",
    22: "Isaiah",
    23: "Jeremiah",
    24: "Lamentations",
    25: "Ezekiel",
    26: "Daniel",
    27: "Hosea",
    28: "Joel",
    29: "Amos",
    30: "Obadiah",
    31: "Jonah",
    32: "Micah",
    33: "Nahum",
    34: "Habakkuk",
    35: "Zephaniah",
    36: "Haggai",
    37: "Zechariah",
    38: "Malachi",
    39: "Matthew",
    40: "Mark",
    41: "Luke",
    42: "John",
    43: "Acts",
    44: "Romans",
    45: "1 Corinthians",
    46: "2 Corinthians",
    47: "Galatians",
    48: "Ephesians",
    49: "Philippians",
    50: "Colossians",
    51: "1 Thessalonians",
    52: "2 Thessalonians",
    53: "1 Timothy",
    54: "2 Timothy",
    55: "Titus",
    56: "Philemon",
    57: "Hebrews",
    58: "James",
    59: "1 Peter",
    60: "2 Peter",
    61: "1 John",
    62: "2 John",
    63: "3 John",
    64: "Jude",
    65: "Revelation"
}

Reverse_Bible_Books = {
    "Genesis": 0,
    "Exodus": 1,
    "Leviticus": 2,
    "Numbers": 3,
    "Deuteronomy": 4,
    "Joshua": 5,
    "Judges": 6,
    "Ruth": 7,
    "One Samuel": 8,
    "Two Samuel": 9,
    "One Kings": 10,
    "Two Kings": 11,
    "One Chronicles": 12,
    "Two Chronicles": 13,
    "Ezra": 14,
    "Nehemiah": 15,
    "Esther": 16,
    "Job": 17,
    "Psalms": 18,
    "Proverbs": 19,
    "Ecclesiastes": 20,
    "Song of Songs": 21,
    "Isaiah": 22,
    "Jeremiah": 23,
    "Lamentations": 24,
    "Ezekiel": 25,
    "Daniel": 26,
    "Hosea": 27,
    "Joel": 28,
    "Amos": 29,
    "Obadiah": 30,
    "Jonah": 31,
    "Micah": 32,
    "Nahum": 33,
    "Habakkuk": 34,
    "Zephaniah": 35,
    "Haggai": 36,
    "Zechariah": 37,
    "Malachi": 38,
    "Matthew": 39,
    "Mark": 40,
    "Luke": 41,
    "John": 42,
    "Acts": 43,
    "Romans": 44,
    "One Corinthians": 45,
    "Two Corinthians": 46,
    "Galatians": 47,
    "Ephesians": 48,
    "Philippians": 49,
    "Colossians": 50,
    "One Thessalonians": 51,
    "Two Thessalonians": 52,
    "One Timothy": 53,
    "Two Timothy": 54,
    "Titus": 55,
    "Philemon": 56,
    "Hebrews": 57,
    "James": 58,
    "One Peter": 59,
    "Two Peter": 60,
    "One John": 61,
    "Two John": 62,
    "Three John": 63,
    "Jude": 64,
    "Revelation": 65
}
