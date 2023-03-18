import { Box } from "@mui/material";
import CheckboxQuestion, { CheckboxQuestionInterface } from "./CheckboxQuestion";
import InputInfo from "./InputInfo";
import NumberQuestion, { NumberQuestionInterface } from "./NumberQuestion";
import SelectQuestion, { SelectQuestionInterface } from "./SelectQuestion";
import TextQuestion, { TextQuestionInterface } from "./TextQuestion";

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


function SimpleQuestion(questionData: SimpleQuestionInterface): JSX.Element {
    let component;
    switch (questionData.questionType) {
        case SimpleQuestionType.NUMBER:
            component = <NumberQuestion {...(questionData.questionData as NumberQuestionInterface)} />;
            break;
        case SimpleQuestionType.LONG_TEXT:
        case SimpleQuestionType.SHORT_TEXT:
            component = <TextQuestion {...(questionData.questionData as TextQuestionInterface)} />;
            break;
        case SimpleQuestionType.MULTIPLE_CHOICE:
            component = <SelectQuestion {...(questionData.questionData as SelectQuestionInterface)} />;
            break;
        case SimpleQuestionType.CHECKBOX:
            component = <CheckboxQuestion {...(questionData.questionData as CheckboxQuestionInterface)} />;
            break;
        default:
            component = <div>Not implemented yet, sorry</div>
    }
    return component;
}

export default SimpleQuestion;