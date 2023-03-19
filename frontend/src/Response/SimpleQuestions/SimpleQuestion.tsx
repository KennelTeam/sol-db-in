import { Box } from "@mui/material";
import CheckboxQuestion, { CheckboxQuestionInterface } from "./CheckboxQuestion";
import InputInfo from "./InputInfo";
import NumberQuestion, { NumberQuestionInterface } from "./NumberQuestion";
import SelectQuestion, { SelectQuestionInterface } from "./SelectQuestion";
import TextQuestion, { TextQuestionInterface } from "./TextQuestion";
import {DateQuestion} from './DateQuestion'

export enum SimpleQuestionType {
    DATE = "DATE",
    USER = "USER",
    LONG_TEXT = "LONG_TEXT",
    SHORT_TEXT = "SHORT_TEXT",
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE",
    CHECKBOX = "CHECKBOX",
    LOCATION = "LOCATION",
    NUMBER = "NUMBER",
    BOOLEAN = "BOOLEAN",
    RELATION = "RELATION"
}

export type SimpleQuestionTypesList = (
    TextQuestionInterface |
    NumberQuestionInterface |
    SelectQuestionInterface |
    CheckboxQuestionInterface
);

export interface SimpleQuestionInterface {
    questionType: SimpleQuestionType;
    questionData: SimpleQuestionTypesList;
}


function SimpleQuestion(props: { questionData: SimpleQuestionInterface; onChange: (arg0: any) => void; }): JSX.Element {
    let questionData: SimpleQuestionInterface = props.questionData
    let component;
    switch (questionData.questionType) {
        case SimpleQuestionType.NUMBER:
            component = <NumberQuestion questionData={(questionData.questionData as NumberQuestionInterface)} onChange={props.onChange}/>;
            break;
        case SimpleQuestionType.LONG_TEXT:
        case SimpleQuestionType.SHORT_TEXT:
            component = <TextQuestion questionData={(questionData.questionData as TextQuestionInterface)} onChange={props.onChange}/>;
            break;
        case SimpleQuestionType.RELATION:
        case SimpleQuestionType.USER:
        case SimpleQuestionType.LOCATION:
        case SimpleQuestionType.MULTIPLE_CHOICE:
            component = <SelectQuestion questionData={(questionData.questionData as SelectQuestionInterface)} onChange={props.onChange}/>;
            break;
        case SimpleQuestionType.CHECKBOX:
            component = <CheckboxQuestion questionData={(questionData.questionData as CheckboxQuestionInterface)} onChange={props.onChange}/>;
            break;
        case SimpleQuestionType.DATE:
            component = <DateQuestion questionData={(questionData.questionData as TextQuestionInterface)} onChange={props.onChange}/>;
            break;
        default:
            component = <div>Not implemented yet, sorry</div>
    }
    return component;
}

export default SimpleQuestion;