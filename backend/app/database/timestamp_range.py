#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from datetime import datetime


class TimestampRange:
    begin: datetime
    end: datetime

    def __init__(self, begin=datetime.min, end=datetime.max):
        self.begin = begin
        self.end = end
