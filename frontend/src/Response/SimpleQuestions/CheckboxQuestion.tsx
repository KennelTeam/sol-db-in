import { Box, Checkbox, FormControl, FormControlLabel } from "@mui/material";
import {useEffect, useState} from "react";
import { CommonQuestionProperties } from "./common";

export interface SingleCheckboxQuestionInterface extends CommonQuestionProperties {
    initialValue: boolean;
}

export interface CheckboxQuestionInterface extends CommonQuestionProperties {
    questions: SingleCheckboxQuestionInterface[];
}

function SingleCheckboxQuestion(props: { question: SingleCheckboxQuestionInterface; onChange: (arg0: SingleCheckboxQuestionInterface) => void; }): JSX.Element {
    let questionData: SingleCheckboxQuestionInterface = props.question
    console.log(questionData)
    const [value, setValue] = useState(questionData);
    const [ans, setAns] = useState(questionData.initialValue)
    useEffect(() => {
        setValue(props.question)
        setAns(props.question.initialValue)
    }, [props.question])


    return <Box display="inline-block">
        <FormControlLabel
            control={<Checkbox checked={ans} onChange={(event) => {
                let data = value
                data.initialValue = event.target.checked
                setAns(event.target.checked)
                setValue(data);
                props.onChange(value)
            }} />}
            label={questionData.label}
            sx={{ whiteSpace: "nowrap" }}
        />
    </Box>
}


function CheckboxQuestion(props: { questionData: CheckboxQuestionInterface; onChange: any; }): JSX.Element {
    let questionData: CheckboxQuestionInterface = props.questionData
    questionData.questions.sort((a, b) => {
        if (!a.label) {
            return -1
        }
        if (!b.label) {
            return 1
        }
        return a.label > b.label ? 1 : -1
    })
    const components = questionData.questions.map((question) => <SingleCheckboxQuestion question={question} onChange={props.onChange}/>)


    return <Box display="inline-block">
        <FormControl sx={{display: "inline-block"}}>
            {components}
        </FormControl>
    </Box>
}

export default CheckboxQuestion;