#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from enum import Enum


class RelationType(Enum):
    LEADER = 1
    PROJECT = 2

    @staticmethod
    def __contains__(item: str) -> bool:
        return item in RelationType.__members__
