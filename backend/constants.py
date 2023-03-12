#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from typing import Final


MODE: Final[str] = "dev"
PORT: Final[int] = 5000
NUM_THREADS: Final[int] = 50
DB_ENGINE: Final[str] = "mysql"
DB_CHARSET: Final[str] = "utf8mb4"
MAX_LANGUAGES_COUNT: Final[int] = 8
MAX_LOGIN_SIZE: Final[int] = 32
MAX_FULLNAME_SIZE: Final[int] = 256
MAX_NAME_SIZE: Final[int] = 64
MAX_PROJECT_NAME_SIZE: Final[int] = 512
MAX_TAG_SIZE: Final[int] = 256
MAX_USER_COMMENT_SIZE: Final[int] = 512
MAX_QUESTION_COMMENT_SIZE: Final[int] = 512
MAX_BLOCK_NAME_SIZE: Final[int] = 64
MAX_QUESTION_TEXT_SIZE: Final[int] = 256
MAX_ANSWER_BLOCK_NAME: Final[int] = 128
MAX_ANSWER_OPTION_SIZE: Final[int] = 128
MAX_SHORT_ANSWER_OPTION_SIZE: Final[int] = 32
MAX_SHEET_TITLE_SIZE: Final[int] = 16
MAX_ANSWER_SIZE: Final[int] = 2048
MAX_TOPONYM_SIZE: Final[int] = 128
MAX_SHORT_QUESTION_SIZE: Final[int] = 32
MAX_TEXT_SIZE: Final[int] = 4096
INT_MIN: Final[int] = -0xffffffffffffffff
INT_MAX: Final[int] = -INT_MIN
SOURCE_QUESTION_ID: Final[int] = -1
ANSWER_ROW_QUESTION_ID: Final[int] = -2
DATE_FORMAT: Final[str] = "%Y-%m-%d"
DATETIME_FORMAT: Final[str] = DATE_FORMAT + " %H:%M:%S"
REQUEST_CONTEXT_USE_DELETED_ITEMS: Final[str] = "use_deleted_items"
JWT_ACCESS_TOKEN_EXPIRES: Final[int] = 1
JWT_REFRESH_EXPIRING_TIME: Final[int] = 30
NAME_COLUMN_NAME = {
    'ru': 'Имя/Название',
    'en': 'Name'
}
TOPONYMS_TABLE_URL: Final[str] = "https://simplemaps.com/static/data/country-cities/id/id.json"
TOPONYMS_REQUEST_TIMEOUT: Final[int] = 179
DEFAULT_LANGUAGE: Final[str] = 'en'
ALL_LANGUAGES_TAG: Final[str] = 'all'

MAX_LEADERS_PAGE_SIZE: int = 200
MAX_PROJECTS_PAGE_SIZE: int = 200
MAX_COMMENT_SIZE_IN_LEADERS_LIST: int = 10
