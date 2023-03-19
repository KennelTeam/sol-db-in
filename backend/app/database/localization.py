#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved

from flask_jwt_extended import current_user
from backend.auxiliary import TranslatedText
from backend.constants import ALL_LANGUAGES_TAG, DEFAULT_LANGUAGE


def localize(text: TranslatedText) -> str | TranslatedText:
    print(text, current_user.selected_language)
    print(isinstance(text, dict))
    if not isinstance(text, dict):
        return text
    lang = current_user.selected_language
    if lang == ALL_LANGUAGES_TAG:
        return text
    return text[lang] if lang in text else text[DEFAULT_LANGUAGE]
