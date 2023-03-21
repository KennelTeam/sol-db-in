import {SetStateAction, useState} from "react";
import {Box, TextField} from "@mui/material";
import {TextQuestionInterface} from "./TextQuestion";
import {CommonQuestionProperties} from "./common";

export function DateQuestion(props: { questionData: TextQuestionInterface; onChange: (arg0: TextQuestionInterface) => void; }): JSX.Element {
    let questionData: TextQuestionInterface = props.questionData
    const [value, setValue] = useState(questionData)
    const [text, setText] = useState(questionData.initialValue)
    console.log(text)
    return <Box display="inline-block">
        <TextField
            size="small"
            type="date"
            sx={{ display: "block" }}
            value={questionData.initialValue}
            onChange={(event) => {
                let data = value
                data.initialValue = event.target.value
                data.value = event.target.value
                console.log(event.target.value)
                setText(event.target.value)
                setValue(data)
                props.onChange(value)
            }}
        />
    </Box>
}

