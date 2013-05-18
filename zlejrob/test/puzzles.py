puzzles = {
    'staircase' : {
        'robotCol': 3,
        'robotRow': 10,
        'robotDir': 0,
        'subs': [10, 0, 0, 0, 0],
        'allowedCommands': 0,
        'board': list(
            "                "
            "            BB  "
            "           BB   "
            "          BB    "
            "         BG     "
            "        BB      "
            "       BB       "
            "      BB        "
            "     BB         "
            "    BB          "
            "   bB           "
            "                "
        )
    },

    'two_function_staircase' : {
        'robotCol': 3,
        'robotRow': 10,
        'robotDir': 0,
        'subs': [3, 3, 0, 0, 0],
        'allowedCommands': 0,
        'board': list(
            "                "
            "            BB  "
            "           BB   "
            "          BB    "
            "         BG     "
            "        BB      "
            "       BB       "
            "      BB        "
            "     BB         "
            "    BB          "
            "   bB           "
            "                "
        )
    },

    'arbitrary_counting' : {
        'robotCol': 0,
        'robotRow': 6,
        'robotDir': 0,
        'subs': [4, 4, 0, 0, 0],
        'allowedCommands': 1,
        'board': list(
            "                "
            "     bgbb       "
            "     b  b       "
            "     b  g       "
            "     b  b       "
            "     b  b       "
            "bbbbgbbbb       "
            "     b          "
            "     b          "
            "     b          "
            "     bbbbbbgbbbB"
            "                "
        )
    },

    'colorful_bar': {
        'robotCol': 7,
        'robotRow': 6,
        'robotDir': 0,
        'subs': [5, 0, 0, 0, 0],
        'allowedCommands': 4,
        'board': list(
            "                "
            "                "
            "       RR       "
            "       BB       "
            "       GG       "
            "       RR       "
            "       bR       "
            "       RR       "
            "       GG       "
            "       BB       "
            "       RR       "
            "                "
        )
    },
}
