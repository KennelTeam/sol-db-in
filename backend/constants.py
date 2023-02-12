#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from typing import final


MODE: final(str) = "dev"
PORT: final(int) = 5000
NUM_THREADS: final(int) = 50
DB_ENGINE: final(str) = "mysql"
DB_CHARSET: final(str) = "utf8mb4"
MAX_LANGUAGES_COUNT: final(int) = 8
MAX_LOGIN_SIZE: final(int) = 32
MAX_FULLNAME_SIZE: final(int) = 256
MAX_NAME_SIZE: final(int) = 64
MAX_PROJECT_NAME_SIZE: final(int) = 512
MAX_TAG_SIZE: final(int) = 256
MAX_COMMENT_SIZE: final(int) = 512
MAX_BLOCK_NAME_SIZE: final(int) = 64
MAX_QUESTION_TEXT_SIZE: final(int) = 256
MAX_ANSWER_BLOCK_NAME: final(int) = 128
MAX_ANSWER_OPTION_SIZE: final(int) = 128
MAX_SHORT_ANSWER_OPTION_SIZE: final(int) = 32
MAX_SHEET_TITLE_SIZE: final(int) = 16
MAX_ANSWER_SIZE: final(int) = 2048
MAX_TOPONYM_SIZE: final(int) = 128
MAX_TEXT_SIZE: final(int) = 4096
INT_MIN: final(int) = -0xffffffffffffffff
INT_MAX: final(int) = -INT_MIN
SOURCE_QUESTION_ID: final(int) = -1
ANSWER_ROW_QUESTION_ID: final(int) = -2
DATE_FORMAT: final(str) = "%Y-%m-%d"
DATETIME_FORMAT: final(str) = DATE_FORMAT + " %H:%M:%S"
REQUEST_CONTEXT_USE_DELETED_ITEMS: final(str) = "use_deleted_items"
JWT_ACCESS_TOKEN_EXPIRES: final(int) = 1
JWT_REFRESH_EXPIRING_TIME: final(int) = 30
