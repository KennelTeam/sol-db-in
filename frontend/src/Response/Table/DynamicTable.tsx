import { QuestionInterface } from "../Question";
import InputInfo, { InputInfoInterface } from "../SimpleQuestions/InputInfo";
import { WithInputInfoInterface } from "../SimpleQuestions/LabeledQuestion";
import SimpleQuestion, { SimpleQuestionInterface, SimpleQuestionType } from "../SimpleQuestions/SimpleQuestion";
import BaseTable from "./BaseTable";


export interface DynamicTableInterface {
    inputInfos: InputInfoInterface[];
    questions: SimpleQuestionInterface[][];
}

interface DynamicTableWithInputInfoInterface extends DynamicTableInterface, WithInputInfoInterface { }

function DynamicTable(dynamicTableData: DynamicTableWithInputInfoInterface): JSX.Element {
    const inputInfoComponents = dynamicTableData.inputInfos.map((inputInfo) => {
        return <InputInfo {...inputInfo} />
    })
    const questionComponents = dynamicTableData.questions.map((quetionsDataRow) =>
        quetionsDataRow.map((question) => <SimpleQuestion {...question} />)
    )
    return <BaseTable inputInfo={dynamicTableData.inputInfo} rows={[inputInfoComponents].concat(questionComponents)} />
}

export default DynamicTable;