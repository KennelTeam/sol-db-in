#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved

from backend.app.flask_app import FlaskApp
from backend.auxiliary import TranslatedText
from backend.constants import ALL_LANGUAGES_TAG, DEFAULT_LANGUAGE


def localize(text: TranslatedText) -> str | TranslatedText:
    if not isinstance(text, dict):
        return text
    lang = FlaskApp().get_language()
    if lang == ALL_LANGUAGES_TAG:
        return text
    return text[lang] if lang in text else text[DEFAULT_LANGUAGE]
