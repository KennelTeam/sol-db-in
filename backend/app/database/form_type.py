#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from enum import Enum


class FormType(Enum):
    LEADER = 0
    PROJECT = 1

    @staticmethod
    def __contains__(item: str) -> bool:
        return item in FormType.__members__
