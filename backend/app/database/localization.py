#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved

from flask_jwt_extended import current_user
from backend.auxiliary import TranslatedText
from backend.constants import ALL_LANGUAGES_TAG, DEFAULT_LANGUAGE


def localize(text: TranslatedText) -> str | TranslatedText:
    lang = current_user.selected_language
    if lang == ALL_LANGUAGES_TAG:
        return text
    return text[lang] if lang in text else text[DEFAULT_LANGUAGE]
