#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from enum import Enum
from typing import Set


class VisualizationType(Enum):
    FULL = 1
    NAMES_ONLY = 2
    NOTHING = 3

    @staticmethod
    def items() -> Set[str]:
        return set(VisualizationType.__members__.keys())
