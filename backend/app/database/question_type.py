#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from enum import Enum


class QuestionType(Enum):
    DATE = 1
    USER = 2
    LONG_TEXT = 3
    SHORT_TEXT = 4
    MULTIPLE_CHOICE = 5
    CHECKBOX = 6
    LOCATION = 7
    NUMBER = 8
    BOOLEAN = 9
    RELATION = 10
