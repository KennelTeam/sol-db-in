#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from enum import Enum


class RelationType(Enum):
    LEADER_TO_LEADER = 0
    LEADER_TO_PROJECT = 1
    PROJECT_TO_LEADER = 2
    PROJECT_TO_PROJECT = 3

    @staticmethod
    def __contains__(item: str) -> bool:
        return item in RelationType.__members__
