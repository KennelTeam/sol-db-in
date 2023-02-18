#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from datetime import datetime
from backend.constants import DATETIME_FORMAT, DATE_FORMAT


def string_to_datetime(source: str) -> datetime:
    return datetime.strptime(source, DATETIME_FORMAT)


def string_to_date(source: str) -> datetime:
    return datetime.strptime(source, DATE_FORMAT)


def datetime_to_string(source: datetime) -> str:
    return source.strftime(DATETIME_FORMAT)


def date_to_string(source: datetime) -> str:
    return source.strftime(DATE_FORMAT)
