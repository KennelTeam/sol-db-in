import {
    APIFixedTable,
    APIForm,
    APIFormState,
    APIFormType,
    APIQuestion,
    APIQuestionBlock, APIQuestionElement,
    APIQuestionTable
} from "./APIObjects";
import { ResponseDataInterface } from "./ResponseData";
import axios from "axios";
import {BlockInterface} from "./Block";
import {QuestionInterface} from "./Question";

async function GetFormInfo(id: number): ResponseDataInterface {

    const res_form = await axios.get(`http://127.0.0.1:5000/forms?id=${id}`, {withCredentials: true})
    const form = res_form.data as APIForm;
    const res_schema = await axios.get(`http://127.0.0.1:5000/form/form_type=${form.form_type.toString()}`,
        {withCredentials: true})
    const schema = res_schema.data as {
        form_type: APIFormType,
        question_blocks: Array<APIQuestionBlock>
    }
}


async function ProcessBlock(block: APIQuestionBlock, data: APIForm): BlockInterface {
    let questions = Array<QuestionInterface>();
    for (var element of block.elements) {
        questions.push(await ProcessBlockElement(element, data))
    }
    return {
        title: block.name,
        items: questions
    }
}

async function ProcessBlockElement(element: APIQuestionElement, data: APIForm): QuestionInterface {

}
