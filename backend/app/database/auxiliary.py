#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import datetime

from .form import Form
from .localization import localize
from .user import User
from .toponym import Toponym
from .question import Question
from .answer import Answer
from .answer_option import AnswerOption
from .question_type import QuestionType
from backend.auxiliary import JSON
from backend.auxiliary.string_dt import date_to_string


def count_answers_with_answer_option(answer_option: AnswerOption) -> int:
    questions_query = Question.filter_by_answer_block(answer_option.answer_block_id).with_entities(Question.id)
    questions_ids = set(q.id for q in questions_query.all())
    query = Answer.query_for_question_ids(questions_ids)
    query = query.filter_by(value_int=answer_option.id)
    # somehow pytype thinks query.count() returns 'Any', when actually it's 'int'
    return query.count()  # type: ignore


def prettify_answer(answer: Answer) -> JSON:
    question = Question.get_by_id(answer.question_id)
    result = answer.to_json() | {
        'type': question.question_type.name
    }
    if question.question_type == QuestionType.DATE:
        result['value'] = date_to_string(answer.value) if isinstance(answer.value, datetime.datetime) else answer.value
    elif question.question_type == QuestionType.RELATION:
        if isinstance(answer.value, int):
            result['ref_id'] = answer.value
            items = Form.get_by_ids({answer.value})
            result['value'] = items[0].name if len(items) > 0 else "DELETED"
            result['relation_type'] = question.relation_settings.relation_type.name
        else:
            result['value'] = answer.value
            result['ref_id'] = -1
    elif question.question_type == QuestionType.USER:
        result['value'] = User.get_by_id(answer.value).name
        result['ref_id'] = answer.value
    elif question.question_type == QuestionType.LOCATION:
        result['ref_id'] = answer.value
        result['value'] = Toponym.get_by_id(answer.value).name
    elif question.question_type in {QuestionType.MULTIPLE_CHOICE, QuestionType.CHECKBOX}:
        result['ref_id'] = answer.value
        result['value'] = localize(AnswerOption.get_by_id(answer.value).name)
    else:
        result['value'] = answer.value
    return result
