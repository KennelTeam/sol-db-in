import { QuestionInterface } from "../Question";
import InputInfo, { InputInfoInterface } from "../SimpleQuestions/InputInfo";
import { WithInputInfoInterface } from "../SimpleQuestions/LabeledQuestion";
import SimpleQuestion, { SimpleQuestionInterface, SimpleQuestionType, SimpleQuestionTypesList } from "../SimpleQuestions/SimpleQuestion";
import BaseTable from "./BaseTable";

export interface FixedTableInterface {
    inputInfoOnTop: Array<InputInfoInterface>;
    inputInfoOnLeft: Array<InputInfoInterface>;
    questionType: SimpleQuestionType;
    questionData: SimpleQuestionTypesList[][];
}

interface FixedTableWithInputInfoInterface extends FixedTableInterface, WithInputInfoInterface {}

function FixedTable(fixedTableData: FixedTableWithInputInfoInterface): JSX.Element {
    const topQuestions = fixedTableData.inputInfoOnTop.map((inputInfoData) => {return <InputInfo {...inputInfoData} />})
    topQuestions.splice(0, 0, <></>)
    const otherComponents = fixedTableData.inputInfoOnLeft.map((inputInfoData, row_index) => {
        const fieldsRow = [...Array(fixedTableData.inputInfoOnTop.length)].map((_, column_index) => {
            return <SimpleQuestion
                questionType={fixedTableData.questionType}
                questionData={fixedTableData.questionData[row_index][column_index]}
            />
        })
        return [<InputInfo {...inputInfoData} />, ...fieldsRow]
    })
    return <BaseTable inputInfo={fixedTableData.inputInfo} rows={[topQuestions].concat(otherComponents)} />
}

export default FixedTable;