import { QuestionInterface } from "../Question";
import InputInfo, { InputInfoInterface } from "../SimpleQuestions/InputInfo";
import { WithInputInfoInterface } from "../SimpleQuestions/LabeledQuestion";
import SimpleQuestion, { SimpleQuestionInterface, SimpleQuestionType } from "../SimpleQuestions/SimpleQuestion";
import BaseTable from "./BaseTable";
import {Box, Button} from "@mui/material";


export interface DynamicTableInterface {
    inputInfos: InputInfoInterface[];
    questions: SimpleQuestionInterface[][];
    sample: SimpleQuestionInterface[];
}

interface DynamicTableWithInputInfoInterface extends DynamicTableInterface, WithInputInfoInterface { }

function DynamicTable(props: { dynamicTableData: DynamicTableInterface, inputInfo: InputInfoInterface, onChange: (arg0: any) => void; }): JSX.Element {
    let dynamicTableData: DynamicTableWithInputInfoInterface = props.dynamicTableData as DynamicTableWithInputInfoInterface
    const inputInfoComponents = dynamicTableData.inputInfos.map((inputInfo) => {
        return <InputInfo {...inputInfo} />
    })
    const questionComponents = dynamicTableData.questions.map((quetionsDataRow) =>
        quetionsDataRow.map((question) => <SimpleQuestion questionData={question} onChange={props.onChange} />)
    )

    const addRow = () => {
        dynamicTableData.questions.push(
            // deep copy
            JSON.parse(JSON.stringify(dynamicTableData.sample))
        )
    }

    const removeRow = () => {
        for (let question of dynamicTableData.questions[dynamicTableData.questions.length - 1]) {
            question.questionData.deleted = true
            props.onChange(question.questionData)
        }
        dynamicTableData.questions.pop()
    }

    return <Box>
        <BaseTable inputInfo={props.inputInfo} rows={[inputInfoComponents].concat(questionComponents)} />
        <Button onClick={addRow}>+</Button>
        <Button onClick={removeRow}>-</Button>
    </Box>
}

export default DynamicTable;