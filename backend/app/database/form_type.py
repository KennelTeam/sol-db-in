#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from enum import Enum
from typing import Set


class FormType(Enum):
    LEADER = 0
    PROJECT = 1

    @staticmethod
    def items() -> Set[str]:
        return set(FormType.__members__.keys())
