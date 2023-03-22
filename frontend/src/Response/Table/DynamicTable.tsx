import { QuestionInterface } from "../Question";
import InputInfo, { InputInfoInterface } from "../SimpleQuestions/InputInfo";
import { WithInputInfoInterface } from "../SimpleQuestions/LabeledQuestion";
import SimpleQuestion, { SimpleQuestionInterface, SimpleQuestionType } from "../SimpleQuestions/SimpleQuestion";
import BaseTable from "./BaseTable";
import {Box, Button} from "@mui/material";
import {useState} from "react";


export interface DynamicTableInterface {
    inputInfos: InputInfoInterface[];
    questions: SimpleQuestionInterface[][];
    sample: SimpleQuestionInterface[];
}

interface DynamicTableWithInputInfoInterface extends DynamicTableInterface, WithInputInfoInterface { }

function DynamicTable(props: { dynamicTableData: DynamicTableInterface, inputInfo: InputInfoInterface, onChange: (arg0: any) => void; }): JSX.Element {
    const [dynamicTableData, setTable] = useState(props.dynamicTableData as DynamicTableWithInputInfoInterface)
    const [a, setA] = useState(dynamicTableData.questions.length)
    console.log("REDRAW")

    let inputInfoComponents = dynamicTableData.inputInfos.map((inputInfo) => {
        return <InputInfo {...inputInfo} />
    })
    let questionComponents = dynamicTableData.questions.map((quetionsDataRow) =>
        quetionsDataRow.map((question) => <SimpleQuestion questionData={question} onChange={props.onChange} />)
    )

    const addRow = () => {
        console.log("here")
        let data = dynamicTableData
        data.questions.push(JSON.parse(JSON.stringify(dynamicTableData.sample)))
        for (let i = 0; i < dynamicTableData.sample.length; ++i) {
            data.questions[data.questions.length - 1][i].questionData.table_row = data.questions.length - 1
        }
        setA(a + 1)
        setTable(data)
    }

    const removeRow = () => {
        if (a > 0) {
            for (let question of dynamicTableData.questions[dynamicTableData.questions.length - 1]) {
                question.questionData.deleted = true
                props.onChange(question.questionData)
            }
            let data = dynamicTableData
            data.questions.pop()
            setA(a - 1)
            setTable(data)
        }
    }

    return <Box>
        <BaseTable inputInfo={props.inputInfo} rows={[inputInfoComponents].concat(questionComponents)} />
        <Button onClick={addRow}>+</Button>
        <Button onClick={removeRow}>-</Button>
    </Box>
}

export default DynamicTable;