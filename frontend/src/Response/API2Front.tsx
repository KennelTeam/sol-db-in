import {
    APIAnswer,
    APIAnswerBlock,
    APIFixedTable,
    APIForm,
    APIOption,
    APIQuestion,
    APIQuestionBlock,
    APIQuestionElement,
    APIQuestionTable
} from "./APIObjects";
import {ResponseDataInterface} from "./ResponseData";
import {BlockInterface} from "./Block";
import {QuestionInterface} from "./Question";
import {SimpleQuestionInterface, SimpleQuestionType, SimpleQuestionTypesList} from "./SimpleQuestions/SimpleQuestion";
import {TextQuestionInterface} from "./SimpleQuestions/TextQuestion";
import {NumberQuestionInterface} from "./SimpleQuestions/NumberQuestion";
import i18n from "../i18n";
import {SelectQuestionInterface, SingleSelectItemInterface} from "./SimpleQuestions/SelectQuestion";
import {CheckboxQuestionInterface, SingleCheckboxQuestionInterface} from "./SimpleQuestions/CheckboxQuestion";
import {getRequest} from "./APIRequests";
import {TableType} from "./Table/BaseTable";
import {InputInfoInterface} from "./SimpleQuestions/InputInfo";
import {DynamicTableInterface} from "./Table/DynamicTable";
import FixedTable, {FixedTableInterface} from "./Table/FixedTable";

export async function GetFormInfo(id: number): Promise<ResponseDataInterface> {

    const res_form = await getRequest("form_page", {id: id})
    const form = res_form.data as APIForm;

    return {
        title: form.name,
        blocks: await Promise.all(form.answers.map(ProcessBlock))
    } as ResponseDataInterface
}


async function ProcessBlock(block: APIQuestionBlock): Promise<BlockInterface> {

    let questions = await Promise.all(block.elements.map(ProcessBlockElement));

    return {
        title: block.name,
        items: questions
    } as BlockInterface
}

async function ProcessBlockElement(element: APIQuestionElement): Promise<QuestionInterface | null> {
    switch (element.type) {
        case "question": {
            return ProcessQuestion(element.value as APIQuestion, (element.value as APIQuestion).answers);
        }
        case "table_question": {
            return ProcessTable(element.value as APIQuestionTable);
        }
        case "fixed_table_question": {
            return ProcessFixedTable(element.value as APIFixedTable);
        }
        default: {
            return null;
        }
    }
}

async function ProcessQuestion(question: APIQuestion, answers: Array<APIAnswer>): Promise<QuestionInterface> {
    let questionData: SimpleQuestionTypesList;
    switch (question.question_type) {
        case SimpleQuestionType.NUMBER: {
            let initialValue = answers.length > 0 ? answers[0].value : -1;
            questionData = {
                // @ts-ignore
                label: question.text[i18n.language],
                initialValue: initialValue as number
            } as NumberQuestionInterface
            break;
        }
        case SimpleQuestionType.RELATION:
        case SimpleQuestionType.LOCATION:
        case SimpleQuestionType.USER:
        case SimpleQuestionType.MULTIPLE_CHOICE: {
            let options: Array<APIOption>;
            if (question.question_type == SimpleQuestionType.MULTIPLE_CHOICE) {
                const options_resp = await getRequest("answer_block", {id: question.answer_block_id})
                const block = options_resp.data as APIAnswerBlock
                options = block.options.map((option) => {
                    return {
                        id: option.id,
                        // @ts-ignore
                        name: option.name[i18n.language]
                    }
                })
            } else if (question.question_type == SimpleQuestionType.LOCATION) {
                const options_resp = await getRequest("all_toponyms")
                options = options_resp.data as Array<APIOption>
            } else if (question.question_type == SimpleQuestionType.USER){
                const options_resp = await getRequest("users")
                options = options_resp.data as Array<APIOption>
            } else {
                const options_resp = await getRequest("forms_lightweight",
                    {form_type: question.relation_settings?.relation_type})
                options = options_resp.data as Array<APIOption>
            }

            let initialValue = answers.length > 0 ? answers[0].value : -1;
            questionData = {
                // @ts-ignore
                label: question.text[i18n.language],
                initialValue: initialValue as number,
                dataToChooseFrom: options.map((option) => {
                    return {
                        id: option.id,
                        // @ts-ignore
                        name: option.name[i18n.language]
                    } as SingleSelectItemInterface
                })
            } as SelectQuestionInterface
            break;
        }
        case SimpleQuestionType.CHECKBOX: {
            let options_resp = await getRequest("answer_block", {id: question.answer_block_id})
            const block = options_resp.data as APIAnswerBlock
            const options = block.options

            questionData = {
                questions: options.map((option) => {
                    return {
                        id: option.id,
                        // @ts-ignore
                        label: option.name[i18n.language],
                        initialValue: answers.find((item) => {return item.value == option.id}) !== undefined
                    } as SingleCheckboxQuestionInterface
                })
            } as CheckboxQuestionInterface
            break;
        }
        default: {
            let initialValue = answers.length > 0 ? answers[0].value as string : "";
            questionData = {
                initialValue: initialValue
            } as TextQuestionInterface
        }
    }

    return {
        questionType: question.question_type,
        inputInfo: {
            // @ts-ignore
            title: question.text[i18n.language],
            // @ts-ignore
            description: question.comment[i18n.language]
        },
        questionData: questionData
    }
}

async function ProcessTable(table: APIQuestionTable): Promise<QuestionInterface> {
    let rows = 1 + Math.max(...table.questions.map(
        (question) => {
            return Math.max(...question.answers.map(
                (answer) => {
                    if (answer.table_row == null) {
                        return 0;
                    }
                    return answer.table_row;
                }
            ))
        }
    ))
    let columns = await Promise.all(table.questions.map(
        async (question) => {
            return await ProcessQuestionTableColumn(question, rows)
        }
    ))

    let inputInfos = columns.map((pair) => {return pair.inputInfo})
    let questions: SimpleQuestionInterface[][] = [];
    for (let row = 0; row < rows; ++row) {
        questions.push(
            columns.map((column) => {
                return column.answers[row]
            })
        )
    }

    return {
        questionType: TableType.DYNAMIC_TABLE,
        inputInfo: {
            title: "",
            description: ""
        },
        questionData: {
            inputInfos: inputInfos,
            questions: questions
        } as DynamicTableInterface
    } as QuestionInterface
}

async function ProcessFixedTable(table: APIFixedTable): Promise<QuestionInterface> {
    const questionToInputInfo = (question: APIQuestion) => {
        return {
            // @ts-ignore
            title: question.text[i18n.language],
            // @ts-ignore
            description: question.comment[i18n.language]
        }
    }

    let inputsOnLeft: Array<InputInfoInterface> = table.rows.map(questionToInputInfo)
    let inputsOnTop: Array<InputInfoInterface> = table.columns.map(questionToInputInfo)

    let answers: SimpleQuestionTypesList[][] = []

    for (let row = 0; row < inputsOnLeft.length; ++row) {
        let currentRow: SimpleQuestionTypesList[] = []
        for (let column = 0; column < inputsOnTop.length; ++column) {
            currentRow.push((await ProcessQuestion(table.columns[column], table.answers[row][column])).questionData as SimpleQuestionTypesList)
        }
        answers.push(currentRow)
    }

    return {
        questionType: TableType.FIXED_TABLE,
        inputInfo: {
            title: "",
            description: ""
        },
        questionData: {
            inputInfoOnTop: inputsOnTop,
            inputInfoOnLeft: inputsOnLeft,
            questionType: table.columns[0].question_type,
            questionData: answers
        } as FixedTableInterface
    } as QuestionInterface
}

async function ProcessQuestionTableColumn(column: APIQuestion, rows: number): Promise<{
    inputInfo: InputInfoInterface,
    answers: Array<SimpleQuestionInterface>
}> {
    let inputInfo = {
        // @ts-ignore
        title: column.text[i18n.language],
        // @ts-ignore
        description: column.comment[i18n.language]
    } as InputInfoInterface


    let answers: Array<SimpleQuestionInterface> = [];
    for (let row = 0; row < rows; ++row) {
        const cur_answers = column.answers.filter((answer) => answer.table_row == row)
        const res = await ProcessQuestion(column, cur_answers)
        answers.push({
            questionType: res.questionType,
            questionData: res.questionData
        } as SimpleQuestionInterface)
    }

    return {
        inputInfo: inputInfo,
        answers: answers
    }
}
