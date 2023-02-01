#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved


# TBH just copy-pasted: https://stackoverflow.com/q/6760685/13200751
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
