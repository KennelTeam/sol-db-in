import { Box } from "@mui/material";
import CheckboxQuestion, { CheckboxQuestionInterface } from "./CheckboxQuestion";
import InputInfo from "./InputInfo";
import NumberQuestion, { NumberQuestionInterface } from "./NumberQuestion";
import SelectQuestion, { SelectQuestionInterface } from "./SelectQuestion";
import TextQuestion, { TextQuestionInterface } from "./TextQuestion";

export enum SimpleQuestionType {
    TEXT = "TEXT",
    NUMBER = "NUMBER",
    SELECT = "SELECT",
    CHECKBOX = "CHECKBOX",
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
        case SimpleQuestionType.TEXT:
            component = <TextQuestion {...(questionData.questionData as TextQuestionInterface)} />;
            break;
        case SimpleQuestionType.SELECT:
            component = <SelectQuestion {...(questionData.questionData as SelectQuestionInterface)} />;
            break;
        case SimpleQuestionType.CHECKBOX:
            component = <CheckboxQuestion {...(questionData.questionData as CheckboxQuestionInterface)} />;
            break;
    }
    return component;
}

export default SimpleQuestion;