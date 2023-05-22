import { AccessRights } from '../types/global'
import { SimpleQuestionType } from "./SimpleQuestions/SimpleQuestion";

export interface APIQuestionBlock {
    questions: Array<APIQuestionElement>,
    name: string
}

export interface APIQuestionElement {
    type: string,
    value: APIQuestion | APIQuestionTable | APIFixedTable
}

export enum APIFormState {
    RECOMMENDED = "RECOMMENDED",
    PLANNED = "PLANNED",
    FINISHED = "FINISHED"
}

export interface APIForm {
    id: number,
    state: APIFormState,
    name: string,
    form_type: APIFormType,
    answers: Array<APIQuestionBlock>
}

export interface APITranslatedText {
    ru: string,
    en: string
}

export interface APIQuestion {
    id: number,
    question_type: SimpleQuestionType,
    comment: string,
    text: string,
    short_text: APITranslatedText,
    answer_block_id: number | null,
    related_question_id: number | null,
    tag_type_id: number | null,
    privacy_settings: APIPrivacySettings,
    formatting_settings: APIFormattingSettings,
    relation_settings: APIRelationSettings | null,
    answers: Array<APIAnswer>
}

export interface APIAnswer {
    id: number,
    form_id: number,
    question_id: number,
    table_row: number | null,
    table_column: number | null,
    row_question_id: number | null,
    value: number | string | boolean,
    ref_id: number | null,
    tags: Array<APITag>,
    create_timestamp: string,
    deleted: boolean
}

export interface APITag {
    id: number,
    name: APITranslatedText,
    type_id: number,
    parent_id: number,
    deleted: boolean
}

export interface APIPrivacySettings {
    id: number,
    editor_access: AccessRights,
    intern_access: AccessRights,
    guest_access: AccessRights,
    creation_timestamp: string,
    deleted: boolean
}

export interface APIFormattingSettings {
    id: number,
    block_sorting: number,
    table_row: number | null,
    table_column: number | null,
    show_on_main_page: boolean,
    block_id: number,
    table_id: number | null,
    fixed_table_id: number | null,
    creation_timestamp: string,
    deleted: boolean
}

export enum APIFormType {
    LEADER = "LEADER",
    PROJECT = "PROJECT"
}

export enum APIVisualizationType {
    ALL = "ALL",
    NAMES_ONLY = "NAMES_ONLY",
    NOTHING = "NOTHING"
}

export interface APIRelationSettings {
    id: number,
    relation_type: APIFormType,
    related_visualization_type: APIVisualizationType,
    related_visualization_sorting: number,
    forward_relation_sheet_name: string | null,
    inverse_relation_sheet_name: string | null,
    main_page_count_title: string | null,
    inverse_main_page_count_title: string | null,
    creation_timestamp: string,
    deleted: boolean
}

export interface APIOption {
    id: number,
    name: string
}

export interface APIQuestionTable {
    questions: Array<APIQuestion>
}

export interface APIFixedTable {
    columns: Array<APIQuestion>,
    rows: Array<APIQuestion>,
    answers: Array<Array<APIAnswer[]>>
}

export interface AnswersIndexed {
    [key: number]: Array<APIAnswer>
}

export interface APIAnswerOption {
    id: number,
    name: string,
    short_name: string,
    answer_block_id: number,
    deleted: boolean,
    creation_timestamp: string
}

export interface APIAnswerBlock {
    id: number,
    options: Array<APIAnswerOption>,
    name: APITranslatedText
}
