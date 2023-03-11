import {ResponseDataInterface} from "./ResponseData";
import {BlockInterface} from "./Block";
import {APIRequest, RESTMethod, TranslatedText} from "../API";
import {QuestionInterface} from "./Question";
import {SimpleQuestionType, SimpleQuestionTypesList} from "./SimpleQuestions/SimpleQuestion";
import {TableType} from "./Table/BaseTable";
import {FixedTableInterface} from "./Table/FixedTable";
import {DynamicTableInterface} from "./Table/DynamicTable";
import SelectQuestion, {SelectQuestionInterface, SingleSelectItemInterface} from "./SimpleQuestions/SelectQuestion";
import i18n from "../i18n";
import {InputInfoInterface} from "./SimpleQuestions/InputInfo";
import {CheckboxQuestionInterface} from "./SimpleQuestions/CheckboxQuestion";
import {TextQuestionInterface} from "./SimpleQuestions/TextQuestion";
import {NumberQuestionInterface} from "./SimpleQuestions/NumberQuestion";

interface APIBlock {
    name: TranslatedText
    questions: Array<{
        type: string,
        value: Object
    }>
}

interface APIQuestion {
    id: number,
    text: TranslatedText,
    short_text: TranslatedText,
    comment: TranslatedText,
    question_type: string,
    answer_block_id: number,
    formatting_settings: Object,
    privacy_settings: Object,
    relation_settings: Object | null,
    form_type: string
}

interface APIAnswer {
    question_id: number,
    table_row: number | null,
    table_column: number | null,
    row_question_id: number | null,
    tags: Array<Object>,
    value: string | number | boolean
}

interface APIOption {
    id: number,
    name: TranslatedText,
    short_name: TranslatedText
}

async function GetOptions(id: number): Promise<Array<SingleSelectItemInterface> | null> {
    let response = await APIRequest(RESTMethod.GET, "answer_block", {id: id});
    if (response == null) return null;
    let result = response as typeof response & {
        options: Array<APIOption>
    }
    let options: Array<SingleSelectItemInterface> = []
    result.options.forEach((opt) => { // @ts-ignore
        options.push({id:opt.id, name:opt.name[i18n.language]})})
    return options
}

async function GetNumberQuestion(answers: Array<APIAnswer>, question: APIQuestion): Promise<NumberQuestionInterface | null> {
    let questionData: NumberQuestionInterface;
    questionData = {
        label: "",
        initialValue: 0
    } as NumberQuestionInterface;
    let search_result = answers.filter((ans) => {return ans.question_id == question.id})
    if (search_result.length == 0) {
        questionData.initialValue = 0
    } else {
        questionData.initialValue = search_result[0].value as number
    }

    return questionData
}

async function GetTextQuestion(answers: Array<APIAnswer>, question: APIQuestion): Promise<TextQuestionInterface | null> {
    let questionData: TextQuestionInterface;
    questionData = {
        label: "",
        initialValue: ""
    } as TextQuestionInterface;
    let search_result = answers.filter((ans) => {return ans.question_id == question.id})
    if (search_result.length == 0) {
        questionData.initialValue = ""
    } else {
        questionData.initialValue = search_result[0].value as string
    }

    return questionData
}

async function GetSelectQuestion(answers: Array<APIAnswer>, question: APIQuestion): Promise<SelectQuestionInterface | null> {

    let questionData: SelectQuestionInterface;
    let dataToChoose = await GetOptions(question.answer_block_id);
    if (dataToChoose == null) return null;
    questionData = {
        label: "",
        initialValue: 0,
        dataToChooseFrom: dataToChoose
    } as SelectQuestionInterface;
    let search_result = answers.filter((ans) => {return ans.question_id == question.id})
    if (search_result.length == 0) {
        questionData.initialValue = 0
    } else {
        questionData.initialValue = search_result[0].value as number
    }
    return questionData
}

async function GetSimpleQuestion(answers: Array<APIAnswer>, question: APIQuestion): Promise<QuestionInterface | null> {
    let questionType: SimpleQuestionType;
    let questionData: SimpleQuestionTypesList | null = null;
    // @ts-ignore
    questionType = SimpleQuestionType[question.question_type];

    switch (questionType) {
        case SimpleQuestionType.SELECT:
            questionData = await GetSelectQuestion(answers, question);
            break;
        case SimpleQuestionType.CHECKBOX:
            break;
        case SimpleQuestionType.TEXT:
            questionData = await GetTextQuestion(answers, question);
            break;
        case SimpleQuestionType.NUMBER:
            questionData = await GetNumberQuestion(answers, question);
            break;
    }
    if (questionData == null) return null;
    // @ts-ignore
    questionData.label = question.text[i18n.language] as string
    return {
        questionData: questionData,
        questionType: questionType,
        inputInfo: {
            // @ts-ignore
            title: question.text[i18n.language],
            // @ts-ignore
            description: question.comment[i18n.language]
        }
    }
}

async function GetQuestion(answers: Array<Object>, type: string, question_element: Object): Promise<QuestionInterface | null> {
    let questionType: SimpleQuestionType | TableType;
    let questionData: SimpleQuestionTypesList | FixedTableInterface | DynamicTableInterface;
    let inputInfo: InputInfoInterface;

    let answers_v: Array<APIAnswer> = []
    answers.forEach((ans) => answers_v.push(ans as APIAnswer))

    switch (type) {
        case "question":
            return await GetSimpleQuestion(answers_v, question_element as APIQuestion)
        case "table_question":
            questionType = TableType.DYNAMIC_TABLE
            break;
        case "fixed_table_question":
            questionType = TableType.FIXED_TABLE
            break;
    }
}

async function GetBlock(answers: Array<Object>, block: APIBlock): Promise<BlockInterface | null> {
    let questions: Array<QuestionInterface | null> = []
    await block.questions.forEach(async (q) => {questions.push(await GetQuestion(answers, q.type, q.value))})
    if (questions.includes(null)) return null;
    return {title: block.name.en, items: questions as Array<QuestionInterface>}
}

async function GetResponse(id: number): Promise<ResponseDataInterface | null> {
    const answers_response = await APIRequest(RESTMethod.GET, "form_page", {id: id})
    if (answers_response == null) return null;
    let answers = answers_response as typeof answers_response & {
        id: number,
        state: string,
        name: string,
        form_type: string,
        answers: Array<Object>
    }
    const schema_response = await APIRequest(RESTMethod.GET, "form", {form_type: answers.form_type})
    if (schema_response == null) return null;
    let schema = schema_response as typeof schema_response & {
        form_type: string,
        question_blocks: Array<APIBlock>
    }
    let blocks: Array<BlockInterface> = []
    schema.question_blocks.forEach((block) => blocks.push(GetBlock(answers.answers, block)))
    return {title: answers.name, blocks: blocks}
}