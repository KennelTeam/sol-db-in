#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from enum import Enum


class VisualizationType(Enum):
    FULL = 1
    NAMES_ONLY = 2
    NOTHING = 3

    @staticmethod
    def __contains__(item: str) -> bool:
        return item in VisualizationType.__members__
