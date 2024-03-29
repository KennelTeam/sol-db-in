import { Box } from "@mui/material";
import CheckboxQuestion, { CheckboxQuestionInterface } from "./CheckboxQuestion";
import InputInfo from "./InputInfo";
import NumberQuestion, { NumberQuestionInterface } from "./NumberQuestion";
import SelectQuestion, { SelectQuestionInterface } from "./SelectQuestion";
import TextQuestion, { TextQuestionInterface } from "./TextQuestion";
import {DateQuestion} from './DateQuestion'
import RelationQuestion, { RelationQuestionProps } from "./RelationQuestion";
import { useEffect } from "react";

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
    CheckboxQuestionInterface |
    RelationQuestionProps
);

export interface SimpleQuestionInterface {
    questionType: SimpleQuestionType;
    questionData: SimpleQuestionTypesList;
}


function SimpleQuestion(props: { questionData: SimpleQuestionInterface; onChange: (arg0: any) => void; }): JSX.Element {
    let questionData: SimpleQuestionInterface = props.questionData

    const makeComponent = () => {
        let newComponent
        switch (questionData.questionType) {
            case SimpleQuestionType.NUMBER:
                newComponent = <NumberQuestion questionData={(questionData.questionData as NumberQuestionInterface)} onChange={props.onChange}/>;
                break;
            case SimpleQuestionType.LONG_TEXT:
            case SimpleQuestionType.SHORT_TEXT:
                newComponent = <TextQuestion
                    questionData={(questionData.questionData as TextQuestionInterface)}
                    onChange={props.onChange}
                    questionType={questionData.questionType}/>;
                break;
            case SimpleQuestionType.RELATION:
                console.log("RELATION TYPE:", questionData.questionData.initialValue)
                newComponent = <RelationQuestion questionData={questionData.questionData as RelationQuestionProps}
                    onChange={props.onChange}/>
                break;
            case SimpleQuestionType.USER:
            case SimpleQuestionType.LOCATION:
            case SimpleQuestionType.MULTIPLE_CHOICE:
                newComponent = <SelectQuestion questionData={(questionData.questionData as SelectQuestionInterface)} onChange={props.onChange}/>;
                break;
            case SimpleQuestionType.CHECKBOX:
                newComponent = <CheckboxQuestion questionData={(questionData.questionData as CheckboxQuestionInterface)} onChange={props.onChange}/>;
                break;
            case SimpleQuestionType.DATE:
                newComponent = <DateQuestion questionData={(questionData.questionData as TextQuestionInterface)} onChange={props.onChange}/>;
                break;
            default:
                newComponent = <div>Not implemented yet, sorry</div>
        }
        return newComponent
    }

    let component = makeComponent()

    useEffect(() => {
        component = makeComponent()
    }, [questionData])
    
    makeComponent()
    return component;
}

export default SimpleQuestion;