#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
import json
from dotenv import load_dotenv
from os import path
from typing import Dict, Any


class ConfigLoader:
    __config__: Dict[str, Any] = {}

    @staticmethod
    def __load_config__() -> None:
        with open(path.join("backend", "config.json"), 'r', encoding='utf-8') as f:
            ConfigLoader.__config__ = json.loads(f.read())

    @staticmethod
    def get_config(key: str):
        if len(ConfigLoader.__config__) == 0:
            load_dotenv(path.join("backend", '.env'))
            ConfigLoader.__load_config__()
        return ConfigLoader.__config__[key]

