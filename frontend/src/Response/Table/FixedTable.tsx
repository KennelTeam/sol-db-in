import { QuestionInterface } from "../Question";
import InputInfo, { InputInfoInterface } from "../SimpleQuestions/InputInfo";
import { WithInputInfoInterface } from "../SimpleQuestions/LabeledQuestion";
import SimpleQuestion, { SimpleQuestionInterface } from "../SimpleQuestions/SimpleQuestion";
import BaseTable from "./BaseTable";

export interface FixedTableInterface {
    inputInfoOnTop: Array<InputInfoInterface>;
    inputInfoOnLeft: Array<InputInfoInterface>;
    questionData: SimpleQuestionInterface;
}

interface FixedTableWithInputInfoInterface extends FixedTableInterface, WithInputInfoInterface {}

function FixedTable(fixedTableData: FixedTableWithInputInfoInterface): JSX.Element {
    const topQuestions = fixedTableData.inputInfoOnTop.map((inputInfoData) => {return <InputInfo {...inputInfoData} />})
    topQuestions.splice(0, 0, <></>)
    const otherComponents = fixedTableData.inputInfoOnLeft.map((inputInfoData) => {
        const fieldsRow = [...Array(fixedTableData.inputInfoOnTop.length)].map((index) => {
            return <SimpleQuestion {...fixedTableData.questionData} />
        })
        return [<InputInfo {...inputInfoData} />, ...fieldsRow]
    })
    return <BaseTable inputInfo={fixedTableData.inputInfo} rows={[topQuestions].concat(otherComponents)} />
}

export default FixedTable;