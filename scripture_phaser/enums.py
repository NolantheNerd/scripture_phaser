import enum

class App(enum.Enum):
    Name = "scripture_phaser"

class Translations(enum.Enum):
    ESV = "English Standard Version"
    NIV = "New International Version"
    KJV = "King James Version"
    NKJV = "New King James Version"
    NLT = "New Living Translation"
    NASB = "New American Standard Bible"
    RSV = "Revised Standard Version"
    NCV = "New Century Version"
    MSG = "The Message"

class Agents(enum.Enum):
    BibleGateway = "https://www.biblegateway.com/passage/?"
    ESVAPI = "https://api.esv.org/v3/passage/text/?"

class Genesis_(enum.Enum):
    _1 = 31
    _2 = 25
    _3 = 24
    _4 = 26
    _5 = 32
    _6 = 22
    _7 = 24
    _8 = 22
    _9 = 29
    _10 = 32
    _11 = 32
    _12 = 20
    _13 = 18
    _14 = 24
    _15 = 21
    _16 = 16
    _17 = 27
    _18 = 33
    _19 = 38
    _20 = 18
    _21 = 34
    _22 = 24
    _23 = 20
    _24 = 67
    _25 = 34
    _26 = 35
    _27 = 46
    _28 = 22
    _29 = 35
    _30 = 43
    _31 = 55
    _32 = 32
    _33 = 20
    _34 = 31
    _35 = 29
    _36 = 43
    _37 = 36
    _38 = 30
    _39 = 23
    _40 = 23
    _41 = 57
    _42 = 38
    _43 = 34
    _44 = 34
    _45 = 28
    _46 = 34
    _47 = 31
    _48 = 22
    _49 = 33
    _50 = 26

class Exodus_(enum.Enum):
    _1 = 22
    _2 = 25
    _3 = 22
    _4 = 31
    _5 = 23
    _6 = 30
    _7 = 25
    _8 = 32
    _9 = 35
    _10 = 29
    _11 = 10
    _12 = 51
    _13 = 22
    _14 = 31
    _15 = 27
    _16 = 36
    _17 = 16
    _18 = 27
    _19 = 25
    _20 = 26
    _21 = 36
    _22 = 31
    _23 = 33
    _24 = 18
    _25 = 40
    _26 = 37
    _27 = 21
    _28 = 43
    _29 = 46
    _30 = 38
    _31 = 18
    _32 = 35
    _33 = 23
    _34 = 35
    _35 = 35
    _36 = 38
    _37 = 29
    _38 = 31
    _39 = 43
    _40 = 38

class Leviticus_(enum.Enum):
    _1 = 17
    _2 = 16
    _3 = 17
    _4 = 35
    _5 = 19
    _6 = 30
    _7 = 38
    _8 = 36
    _9 = 24
    _10 = 20
    _11 = 47
    _12 = 8
    _13 = 59
    _14 = 57
    _15 = 33
    _16 = 34
    _17 = 16
    _18 = 30
    _19 = 37
    _20 = 27
    _21 = 24
    _22 = 33
    _23 = 44
    _24 = 23
    _25 = 55
    _26 = 46
    _27 = 34

class Numbers_(enum.Enum):
    _1 = 54
    _2 = 34
    _3 = 51
    _4 = 49
    _5 = 31
    _6 = 27
    _7 = 89
    _8 = 26
    _9 = 23
    _10 = 36
    _11 = 35
    _12 = 16
    _13 = 33
    _14 = 45
    _15 = 41
    _16 = 50
    _17 = 13
    _18 = 32
    _19 = 22
    _20 = 29
    _21 = 35
    _22 = 41
    _23 = 30
    _24 = 25
    _25 = 18
    _26 = 65
    _27 = 23
    _28 = 31
    _29 = 40
    _30 = 16
    _31 = 54
    _32 = 42
    _33 = 56
    _34 = 29
    _35 = 34
    _36 = 13

class Deuteronomy_(enum.Enum):
    _1 = 46
    _2 = 37
    _3 = 29
    _4 = 49
    _5 = 33
    _6 = 25
    _7 = 26
    _8 = 20
    _9 = 29
    _10 = 22
    _11 = 32
    _12 = 32
    _13 = 18
    _14 = 29
    _15 = 23
    _16 = 22
    _17 = 20
    _18 = 22
    _19 = 21
    _20 = 20
    _21 = 23
    _22 = 30
    _23 = 25
    _24 = 22
    _25 = 19
    _26 = 19
    _27 = 26
    _28 = 68
    _29 = 29
    _30 = 20
    _31 = 30
    _32 = 52
    _33 = 29
    _34 = 12

class Joshua_(enum.Enum):
    _1 = 18
    _2 = 24
    _3 = 17
    _4 = 24
    _5 = 15
    _6 = 27
    _7 = 26
    _8 = 35
    _9 = 27
    _10 = 43
    _11 = 23
    _12 = 24
    _13 = 33
    _14 = 15
    _15 = 63
    _16 = 10
    _17 = 18
    _18 = 28
    _19 = 51
    _20 = 9
    _21 = 45
    _22 = 34
    _23 = 16
    _24 = 33

class Judges_(enum.Enum):
    _1 = 36
    _2 = 23
    _3 = 31
    _4 = 24
    _5 = 31
    _6 = 40
    _7 = 25
    _8 = 35
    _9 = 57
    _10 = 18
    _11 = 40
    _12 = 15
    _13 = 25
    _14 = 20
    _15 = 20
    _16 = 31
    _17 = 13
    _18 = 31
    _19 = 30
    _20 = 48
    _21 = 25

class Ruth_(enum.Enum):
    _1 = 22
    _2 = 23
    _3 = 18
    _4 = 22

class One_Samuel_(enum.Enum):
    _1 = 28
    _2 = 36
    _3 = 21
    _4 = 22
    _5 = 12
    _6 = 21
    _7 = 17
    _8 = 22
    _9 = 27
    _10 = 27
    _11 = 15
    _12 = 25
    _13 = 23
    _14 = 52
    _15 = 35
    _16 = 23
    _17 = 58
    _18 = 30
    _19 = 24
    _20 = 42
    _21 = 15
    _22 = 23
    _23 = 29
    _24 = 22
    _25 = 44
    _26 = 25
    _27 = 12
    _28 = 25
    _29 = 11
    _30 = 31
    _31 = 13

class Two_Samuel_(enum.Enum):
    _1 = 27
    _2 = 32
    _3 = 39
    _4 = 12
    _5 = 25
    _6 = 23
    _7 = 29
    _8 = 18
    _9 = 13
    _10 = 19
    _11 = 27
    _12 = 31
    _13 = 39
    _14 = 33
    _15 = 37
    _16 = 23
    _17 = 29
    _18 = 33
    _19 = 43
    _20 = 26
    _21 = 22
    _22 = 51
    _23 = 39
    _24 = 25

class One_Kings_(enum.Enum):
    _1 = 53
    _2 = 46
    _3 = 28
    _4 = 34
    _5 = 18
    _6 = 38
    _7 = 51
    _8 = 66
    _9 = 28
    _10 = 29
    _11 = 43
    _12 = 33
    _13 = 34
    _14 = 31
    _15 = 34
    _16 = 34
    _17 = 24
    _18 = 46
    _19 = 21
    _20 = 43
    _21 = 29
    _22 = 53

class Two_Kings_(enum.Enum):
    _1 = 18
    _2 = 25
    _3 = 27
    _4 = 44
    _5 = 27
    _6 = 33
    _7 = 20
    _8 = 29
    _9 = 37
    _10 = 36
    _11 = 21
    _12 = 21
    _13 = 25
    _14 = 29
    _15 = 38
    _16 = 20
    _17 = 41
    _18 = 37
    _19 = 37
    _20 = 21
    _21 = 26
    _22 = 20
    _23 = 37
    _24 = 20
    _25 = 30

class One_Chronicles_(enum.Enum):
    _1 = 54
    _2 = 55
    _3 = 24
    _4 = 43
    _5 = 26
    _6 = 81
    _7 = 40
    _8 = 40
    _9 = 44
    _10 = 14
    _11 = 47
    _12 = 40
    _13 = 14
    _14 = 17
    _15 = 29
    _16 = 43
    _17 = 27
    _18 = 17
    _19 = 19
    _20 = 8
    _21 = 30
    _22 = 19
    _23 = 32
    _24 = 31
    _25 = 31
    _26 = 32
    _27 = 34
    _28 = 21
    _29 = 30

class Two_Chronicles_(enum.Enum):
    _1 = 17
    _2 = 18
    _3 = 17
    _4 = 22
    _5 = 14
    _6 = 42
    _7 = 22
    _8 = 18
    _9 = 31
    _10 = 19
    _11 = 23
    _12 = 16
    _13 = 22
    _14 = 15
    _15 = 19
    _16 = 14
    _17 = 19
    _18 = 34
    _19 = 11
    _20 = 37
    _21 = 20
    _22 = 12
    _23 = 21
    _24 = 27
    _25 = 28
    _26 = 23
    _27 = 9
    _28 = 27
    _29 = 36
    _30 = 27
    _31 = 21
    _32 = 33
    _33 = 25
    _34 = 33
    _35 = 27
    _36 = 23

class Ezra_(enum.Enum):
    _1 = 11
    _2 = 70
    _3 = 13
    _4 = 24
    _5 = 17
    _6 = 22
    _7 = 28
    _8 = 36
    _9 = 15
    _10 = 44

class Nehemiah_(enum.Enum):
    _1 = 11
    _2 = 20
    _3 = 32
    _4 = 23
    _5 = 19
    _6 = 19
    _7 = 73
    _8 = 18
    _9 = 38
    _10 = 39
    _11 = 36
    _12 = 47
    _13 = 31

class Esther_(enum.Enum):
    _1 = 22
    _2 = 23
    _3 = 15
    _4 = 17
    _5 = 14
    _6 = 14
    _7 = 10
    _8 = 17
    _9 = 32
    _10 = 3

class Job_(enum.Enum):
    _1 = 22
    _2 = 13
    _3 = 26
    _4 = 21
    _5 = 27
    _6 = 30
    _7 = 21
    _8 = 22
    _9 = 35
    _10 = 22
    _11 = 20
    _12 = 25
    _13 = 28
    _14 = 22
    _15 = 35
    _16 = 22
    _17 = 16
    _18 = 21
    _19 = 29
    _20 = 29
    _21 = 34
    _22 = 30
    _23 = 17
    _24 = 25
    _25 = 6
    _26 = 14
    _27 = 23
    _28 = 28
    _29 = 25
    _30 = 31
    _31 = 40
    _32 = 22
    _33 = 33
    _34 = 37
    _35 = 16
    _36 = 33
    _37 = 24
    _38 = 41
    _39 = 30
    _40 = 24
    _41 = 34
    _42 = 17

class Psalms_(enum.Enum):
    _1 = 6
    _2 = 12
    _3 = 8
    _4 = 8
    _5 = 12
    _6 = 10
    _7 = 17
    _8 = 9
    _9 = 20
    _10 = 18
    _11 = 7
    _12 = 8
    _13 = 6
    _14 = 7
    _15 = 5
    _16 = 11
    _17 = 15
    _18 = 50
    _19 = 14
    _20 = 9
    _21 = 13
    _22 = 31
    _23 = 6
    _24 = 10
    _25 = 22
    _26 = 12
    _27 = 14
    _28 = 9
    _29 = 11
    _30 = 12
    _31 = 24
    _32 = 11
    _33 = 22
    _34 = 22
    _35 = 28
    _36 = 12
    _37 = 40
    _38 = 22
    _39 = 13
    _40 = 17
    _41 = 13
    _42 = 11
    _43 = 5
    _44 = 26
    _45 = 17
    _46 = 11
    _47 = 9
    _48 = 14
    _49 = 20
    _50 = 23
    _51 = 19
    _52 = 9
    _53 = 6
    _54 = 7
    _55 = 23
    _56 = 13
    _57 = 11
    _58 = 11
    _59 = 17
    _60 = 12
    _61 = 8
    _62 = 12
    _63 = 11
    _64 = 10
    _65 = 13
    _66 = 20
    _67 = 7
    _68 = 35
    _69 = 36
    _70 = 5
    _71 = 24
    _72 = 20
    _73 = 28
    _74 = 23
    _75 = 10
    _76 = 12
    _77 = 20
    _78 = 72
    _79 = 13
    _80 = 19
    _81 = 16
    _82 = 8
    _83 = 18
    _84 = 12
    _85 = 13
    _86 = 17
    _87 = 7
    _88 = 18
    _89 = 52
    _90 = 17
    _91 = 16
    _92 = 15
    _93 = 5
    _94 = 23
    _95 = 11
    _96 = 13
    _97 = 12
    _98 = 9
    _99 = 9
    _100 = 5
    _101 = 8
    _102 = 28
    _103 = 22
    _104 = 35
    _105 = 45
    _106 = 48
    _107 = 43
    _108 = 13
    _109 = 31
    _110 = 7
    _111 = 10
    _112 = 10
    _113 = 9
    _114 = 8
    _115 = 18
    _116 = 19
    _117 = 2
    _118 = 29
    _119 = 176
    _120 = 7
    _121 = 8
    _122 = 9
    _123 = 4
    _124 = 8
    _125 = 5
    _126 = 6
    _127 = 5
    _128 = 6
    _129 = 8
    _130 = 8
    _131 = 3
    _132 = 18
    _133 = 3
    _134 = 3
    _135 = 21
    _136 = 26
    _137 = 9
    _138 = 8
    _139 = 24
    _140 = 13
    _141 = 10
    _142 = 7
    _143 = 12
    _144 = 15
    _145 = 21
    _146 = 10
    _147 = 20
    _148 = 14
    _149 = 9
    _150 = 6

class Proverbs_(enum.Enum):
    _1 = 33
    _2 = 22
    _3 = 35
    _4 = 27
    _5 = 23
    _6 = 35
    _7 = 27
    _8 = 36
    _9 = 18
    _10 = 32
    _11 = 31
    _12 = 28
    _13 = 25
    _14 = 35
    _15 = 33
    _16 = 33
    _17 = 28
    _18 = 24
    _19 = 29
    _20 = 30
    _21 = 31
    _22 = 29
    _23 = 35
    _24 = 34
    _25 = 28
    _26 = 28
    _27 = 27
    _28 = 28
    _29 = 27
    _30 = 33
    _31 = 31

class Ecclesiastes_(enum.Enum):
    _1 = 18
    _2 = 26
    _3 = 22
    _4 = 16
    _5 = 20
    _6 = 12
    _7 = 29
    _8 = 17
    _9 = 18
    _10 = 20
    _11 = 10
    _12 = 14

class Song_of_Songs_(enum.Enum):
    _1 = 17
    _2 = 17
    _3 = 11
    _4 = 16
    _5 = 16
    _6 = 13
    _7 = 13
    _8 = 14

class Isaiah_(enum.Enum):
    _1 = 31
    _2 = 22
    _3 = 26
    _4 = 6
    _5 = 30
    _6 = 13
    _7 = 25
    _8 = 22
    _9 = 21
    _10 = 34
    _11 = 16
    _12 = 6
    _13 = 22
    _14 = 32
    _15 = 9
    _16 = 14
    _17 = 14
    _18 = 7
    _19 = 25
    _20 = 6
    _21 = 17
    _22 = 25
    _23 = 18
    _24 = 23
    _25 = 12
    _26 = 21
    _27 = 13
    _28 = 29
    _29 = 24
    _30 = 33
    _31 = 9
    _32 = 20
    _33 = 24
    _34 = 17
    _35 = 10
    _36 = 22
    _37 = 38
    _38 = 22
    _39 = 8
    _40 = 31
    _41 = 29
    _42 = 25
    _43 = 28
    _44 = 28
    _45 = 25
    _46 = 13
    _47 = 15
    _48 = 22
    _49 = 26
    _50 = 11
    _51 = 23
    _52 = 15
    _53 = 12
    _54 = 17
    _55 = 13
    _56 = 12
    _57 = 21
    _58 = 14
    _59 = 21
    _60 = 22
    _61 = 11
    _62 = 12
    _63 = 19
    _64 = 12
    _65 = 25
    _66 = 24

class Jeremiah_(enum.Enum):
    _1 = 19
    _2 = 37
    _3 = 25
    _4 = 31
    _5 = 31
    _6 = 30
    _7 = 34
    _8 = 22
    _9 = 26
    _10 = 25
    _11 = 23
    _12 = 17
    _13 = 27
    _14 = 22
    _15 = 21
    _16 = 21
    _17 = 27
    _18 = 23
    _19 = 15
    _20 = 18
    _21 = 14
    _22 = 30
    _23 = 40
    _24 = 10
    _25 = 38
    _26 = 24
    _27 = 22
    _28 = 17
    _29 = 32
    _30 = 24
    _31 = 40
    _32 = 44
    _33 = 26
    _34 = 22
    _35 = 19
    _36 = 32
    _37 = 21
    _38 = 28
    _39 = 18
    _40 = 16
    _41 = 18
    _42 = 22
    _43 = 13
    _44 = 30
    _45 = 5
    _46 = 28
    _47 = 7
    _48 = 47
    _49 = 39
    _50 = 46
    _51 = 64
    _52 = 34

class Lamentations_(enum.Enum):
    _1 = 22
    _2 = 22
    _3 = 66
    _4 = 22
    _5 = 22

class Ezekiel_(enum.Enum):
    _1 = 28
    _2 = 10
    _3 = 27
    _4 = 17
    _5 = 17
    _6 = 14
    _7 = 27
    _8 = 18
    _9 = 11
    _10 = 22
    _11 = 25
    _12 = 28
    _13 = 23
    _14 = 23
    _15 = 8
    _16 = 63
    _17 = 24
    _18 = 32
    _19 = 14
    _20 = 49
    _21 = 32
    _22 = 31
    _23 = 49
    _24 = 27
    _25 = 17
    _26 = 21
    _27 = 36
    _28 = 26
    _29 = 21
    _30 = 26
    _31 = 18
    _32 = 32
    _33 = 33
    _34 = 31
    _35 = 15
    _36 = 38
    _37 = 28
    _38 = 23
    _39 = 29
    _40 = 49
    _41 = 26
    _42 = 20
    _43 = 27
    _44 = 31
    _45 = 25
    _46 = 24
    _47 = 23
    _48 = 35

class Daniel_(enum.Enum):
    _1 = 21
    _2 = 49
    _3 = 30
    _4 = 37
    _5 = 31
    _6 = 28
    _7 = 28
    _8 = 27
    _9 = 27
    _10 = 21
    _11 = 45
    _12 = 13

class Hosea_(enum.Enum):
    _1 = 11
    _2 = 23
    _3 = 5
    _4 = 19
    _5 = 15
    _6 = 11
    _7 = 16
    _8 = 14
    _9 = 17
    _10 = 15
    _11 = 12
    _12 = 14
    _13 = 16
    _14 = 9

class Joel_(enum.Enum):
    _1 = 20
    _2 = 32
    _3 = 21

class Amos_(enum.Enum):
    _1 = 15
    _2 = 16
    _3 = 15
    _4 = 13
    _5 = 27
    _6 = 14
    _7 = 17
    _8 = 14
    _9 = 15

class Obadiah_(enum.Enum):
    _1 = 21

class Jonah_(enum.Enum):
    _1 = 17
    _2 = 10
    _3 = 10
    _4 = 11

class Micah_(enum.Enum):
    _1 = 16
    _2 = 13
    _3 = 12
    _4 = 13
    _5 = 15
    _6 = 16
    _7 = 20

class Nahum_(enum.Enum):
    _1 = 15
    _2 = 13
    _3 = 19

class Habakkuk_(enum.Enum):
    _1 = 17
    _2 = 20
    _3 = 19

class Zephaniah_(enum.Enum):
    _1 = 18
    _2 = 15
    _3 = 20

class Haggai_(enum.Enum):
    _1 = 15
    _2 = 23

class Zechariah_(enum.Enum):
    _1 = 21
    _2 = 13
    _3 = 10
    _4 = 14
    _5 = 11
    _6 = 15
    _7 = 14
    _8 = 23
    _9 = 17
    _10 = 12
    _11 = 17
    _12 = 14
    _13 = 9
    _14 = 21

class Malachi_(enum.Enum):
    _1 = 14
    _2 = 17
    _3 = 18
    _4 = 6

class Matthew_(enum.Enum):
    _1 = 25
    _2 = 23
    _3 = 17
    _4 = 25
    _5 = 48
    _6 = 34
    _7 = 29
    _8 = 34
    _9 = 38
    _10 = 42
    _11 = 30
    _12 = 50
    _13 = 58
    _14 = 36
    _15 = 39
    _16 = 28
    _17 = 27
    _18 = 35
    _19 = 30
    _20 = 34
    _21 = 46
    _22 = 46
    _23 = 39
    _24 = 51
    _25 = 46
    _26 = 75
    _27 = 66
    _28 = 20

class Mark_(enum.Enum):
    _1 = 45
    _2 = 28
    _3 = 35
    _4 = 41
    _5 = 43
    _6 = 56
    _7 = 37
    _8 = 38
    _9 = 50
    _10 = 52
    _11 = 33
    _12 = 44
    _13 = 37
    _14 = 72
    _15 = 47
    _16 = 20

class Luke_(enum.Enum):
    _1 = 80
    _2 = 52
    _3 = 38
    _4 = 44
    _5 = 39
    _6 = 49
    _7 = 50
    _8 = 56
    _9 = 62
    _10 = 42
    _11 = 54
    _12 = 59
    _13 = 35
    _14 = 35
    _15 = 32
    _16 = 31
    _17 = 37
    _18 = 43
    _19 = 48
    _20 = 47
    _21 = 38
    _22 = 71
    _23 = 56
    _24 = 53

class John_(enum.Enum):
    _1 = 51
    _2 = 25
    _3 = 36
    _4 = 54
    _5 = 47
    _6 = 71
    _7 = 53
    _8 = 59
    _9 = 41
    _10 = 42
    _11 = 57
    _12 = 50
    _13 = 38
    _14 = 31
    _15 = 27
    _16 = 33
    _17 = 26
    _18 = 40
    _19 = 42
    _20 = 31
    _21 = 25

class Acts_(enum.Enum):
    _1 = 26
    _2 = 47
    _3 = 26
    _4 = 37
    _5 = 42
    _6 = 15
    _7 = 60
    _8 = 40
    _9 = 43
    _10 = 48
    _11 = 30
    _12 = 25
    _13 = 52
    _14 = 28
    _15 = 41
    _16 = 40
    _17 = 34
    _18 = 28
    _19 = 41
    _20 = 38
    _21 = 40
    _22 = 30
    _23 = 35
    _24 = 27
    _25 = 27
    _26 = 32
    _27 = 44
    _28 = 31

class Romans_(enum.Enum):
    _1 = 32
    _2 = 29
    _3 = 31
    _4 = 25
    _5 = 21
    _6 = 23
    _7 = 25
    _8 = 39
    _9 = 33
    _10 = 21
    _11 = 36
    _12 = 21
    _13 = 14
    _14 = 26
    _15 = 33
    _16 = 25

class One_Corinthians_(enum.Enum):
    _1 = 31
    _2 = 16
    _3 = 23
    _4 = 21
    _5 = 13
    _6 = 20
    _7 = 40
    _8 = 13
    _9 = 27
    _10 = 33
    _11 = 34
    _12 = 31
    _13 = 13
    _14 = 40
    _15 = 58
    _16 = 24

class Two_Corinthians_(enum.Enum):
    _1 = 24
    _2 = 17
    _3 = 18
    _4 = 18
    _5 = 21
    _6 = 18
    _7 = 16
    _8 = 24
    _9 = 15
    _10 = 18
    _11 = 33
    _12 = 21
    _13 = 14

class Galatians_(enum.Enum):
    _1 = 24
    _2 = 21
    _3 = 29
    _4 = 31
    _5 = 26
    _6 = 18

class Ephesians_(enum.Enum):
    _1 = 23
    _2 = 22
    _3 = 21
    _4 = 32
    _5 = 33
    _6 = 24

class Philippians_(enum.Enum):
    _1 = 30
    _2 = 30
    _3 = 21
    _4 = 23

class Colossians_(enum.Enum):
    _1 = 29
    _2 = 23
    _3 = 25
    _4 = 18

class One_Thessalonians_(enum.Enum):
    _1 = 10
    _2 = 20
    _3 = 13
    _4 = 18
    _5 = 28

class Two_Thessalonians_(enum.Enum):
    _1 = 12
    _2 = 17
    _3 = 18

class One_Timothy_(enum.Enum):
    _1 = 20
    _2 = 15
    _3 = 16
    _4 = 16
    _5 = 25
    _6 = 21

class Two_Timothy_(enum.Enum):
    _1 = 18
    _2 = 26
    _3 = 17
    _4 = 22

class Titus_(enum.Enum):
    _1 = 16
    _2 = 15
    _3 = 15

class Philemon_(enum.Enum):
    _1 = 25

class Hebrews_(enum.Enum):
    _1 = 14
    _2 = 18
    _3 = 19
    _4 = 16
    _5 = 14
    _6 = 20
    _7 = 28
    _8 = 13
    _9 = 28
    _10 = 39
    _11 = 40
    _12 = 29
    _13 = 25

class James_(enum.Enum):
    _1 = 27
    _2 = 26
    _3 = 18
    _4 = 17
    _5 = 20

class One_Peter_(enum.Enum):
    _1 = 25
    _2 = 25
    _3 = 22
    _4 = 19
    _5 = 14

class Two_Peter_(enum.Enum):
    _1 = 21
    _2 = 22
    _3 = 18

class One_John_(enum.Enum):
    _1 = 10
    _2 = 29
    _3 = 24
    _4 = 21
    _5 = 21

class Two_John_(enum.Enum):
    _1 = 13

class Three_John_(enum.Enum):
    _1 = 14

class Jude_(enum.Enum):
    _1 = 25

class Revelation_(enum.Enum):
    _1 = 20
    _2 = 29
    _3 = 22
    _4 = 11
    _5 = 14
    _6 = 17
    _7 = 17
    _8 = 13
    _9 = 21
    _10 = 11
    _11 = 19
    _12 = 17
    _13 = 18
    _14 = 20
    _15 = 8
    _16 = 21
    _17 = 18
    _18 = 24
    _19 = 21
    _20 = 15
    _21 = 27
    _22 = 21

class Bible(enum.Enum):
    Genesis = Genesis_
    Exodus = Exodus_
    Leviticus = Leviticus_
    Numbers = Numbers_
    Deuteronomy = Deuteronomy_
    Joshua = Joshua_
    Judges = Judges_
    Ruth = Ruth_
    One_Samuel = One_Samuel_
    Two_Samuel = Two_Samuel_
    One_Kings = One_Kings_
    Two_Kings = Two_Kings_
    One_Chronicles = One_Chronicles_
    Two_Chronicles = Two_Chronicles_
    Ezra = Ezra_
    Nehemiah = Nehemiah_
    Esther = Esther_
    Job = Job_
    Psalms = Psalms_
    Proverbs = Proverbs_
    Ecclesiastes = Ecclesiastes_
    Song_of_Songs = Song_of_Songs_
    Isaiah = Isaiah_
    Jeremiah = Jeremiah_
    Lamentations = Lamentations_
    Ezekiel = Ezekiel_
    Daniel = Daniel_
    Hosea = Hosea_
    Joel = Joel_
    Amos = Amos_
    Obadiah = Obadiah_
    Jonah = Jonah_
    Micah = Micah_
    Nahum = Nahum_
    Habakkuk = Habakkuk_
    Zephaniah = Zephaniah_
    Haggai = Haggai_
    Zechariah = Zechariah_
    Malachi = Malachi_
    Matthew = Matthew_
    Mark = Mark_
    Luke = Luke_
    John = John_
    Acts = Acts_
    Romans = Romans_
    One_Corinthians = One_Corinthians_
    Two_Corinthians = Two_Corinthians_
    Galatians = Galatians_
    Ephesians = Ephesians_
    Philippians = Philippians_
    Colossians = Colossians_
    One_Thessalonians = One_Thessalonians_
    Two_Thessalonians = Two_Thessalonians_
    One_Timothy = One_Timothy_
    Two_Timothy = Two_Timothy_
    Titus = Titus_
    Philemon = Philemon_
    Hebrews = Hebrews_
    James = James_
    One_Peter = One_Peter_
    Two_Peter = Two_Peter_
    One_John = One_John_
    Two_John = Two_John_
    Three_John = Three_John_
    Jude = Jude_
    Revelation = Revelation_
