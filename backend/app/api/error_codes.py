#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import enum


class HTTPErrorCode(enum.Enum):
    SUCCESS = 0
    INVALID_ARG_LOCATION = 1
    INVALID_ARG_TYPE = 2
    MISSING_ARGUMENT = 3
    WRONG_ID = 4
