import { Box } from "@mui/material";
import CheckboxQuestion, { CheckboxQuestionInterface } from "./SimpleQuestions/CheckboxQuestion";
import { InputInfoInterface } from "./SimpleQuestions/InputInfo";
import LabeledQuestion from "./SimpleQuestions/LabeledQuestion";
import NumberQuestion, { NumberQuestionInterface } from "./SimpleQuestions/NumberQuestion";
import SelectQuestion, { SelectQuestionInterface } from "./SimpleQuestions/SelectQuestion";
import SimpleQuestion, { SimpleQuestionType, SimpleQuestionTypesList } from "./SimpleQuestions/SimpleQuestion";
import TextQuestion, { TextQuestionInterface } from "./SimpleQuestions/TextQuestion";
import { TableType } from "./Table/BaseTable";
import DynamicTable, { DynamicTableInterface } from "./Table/DynamicTable";
import FixedTable, { FixedTableInterface } from "./Table/FixedTable";


export interface QuestionInterface {
    questionType: SimpleQuestionType | TableType;
    questionData: SimpleQuestionTypesList | FixedTableInterface | DynamicTableInterface;
    inputInfo: InputInfoInterface;
}

function Question(props: { questionData: QuestionInterface; onChange: any; }): JSX.Element {
    let questionData: QuestionInterface = props.questionData;
    let callBack = props.onChange;

    let component: JSX.Element;
    if (questionData.questionType in SimpleQuestionType) {
        component = <LabeledQuestion
            questionType={questionData.questionType as SimpleQuestionType}
            questionData={questionData.questionData as SimpleQuestionTypesList}
            inputInfo={questionData.inputInfo}
            onChange={callBack}
        />
    } else if (questionData.questionType === TableType.FIXED_TABLE) {
        component = <FixedTable onChange={callBack} fixedTableData={
            {
                ...(questionData.questionData as FixedTableInterface),
                inputInfo: questionData.inputInfo
            }}/>
    } else if (questionData.questionType === TableType.DYNAMIC_TABLE) {
        component = <DynamicTable onChange={callBack} dynamicTableData={questionData.questionData as DynamicTableInterface}
        inputInfo={questionData.inputInfo}/>
    } else {
        component = <h1>Question type not found</h1>
    }
    return <Box display="block">{component}</Box>;
}

export default Question;