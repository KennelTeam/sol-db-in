#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
from .question import Question
from .answer import Answer
from .answer_option import AnswerOption


def count_answers_with_answer_option(answer_option: AnswerOption) -> int:
    questions_query = Question.filter_by_answer_block(answer_option.answer_block_id).with_entities(Question.id)
    questions_ids = set(q.id for q in questions_query.all())
    query = Answer.query_for_question_ids(questions_ids)
    query = query.filter_by(value_int=answer_option.id)
    # somehow pytype thinks query.count() returns 'Any', when actually it's 'int'
    return query.count()  # type: ignore
