import { Box, TextField } from "@mui/material";
import { useState } from "react";
import { CommonQuestionProperties } from "./common";

export interface NumberQuestionInterface extends CommonQuestionProperties {
    initialValue: number | null;
}

function NumberQuestion(props: { questionData: NumberQuestionInterface; onChange: (arg0: any) => void; }): JSX.Element {
    let questionData: NumberQuestionInterface = props.questionData
    const [value, setValue] = useState(questionData)
    const [ans, setAns] = useState(questionData.initialValue ? questionData.initialValue : 0)
    return <Box display="inline-block">
        <TextField
        type="number"
        label={questionData.label}
        size="small"
        sx={{ display: "inline-block", maxWidth: "200px", minWidth: "120px" }}
        value={ans.toString()}
        onChange={(event) => {
            if (!event.target.validity.badInput) {
                if (event.target.value === '') {
                }
                else {
                    let data = value
                    data.initialValue = +event.target.value
                    data.value = data.initialValue
                    setAns(+event.target.value)
                    setValue(data)
                    props.onChange(value)
                }
            }
            event.preventDefault()
        }}
        />
    </Box>
}

export default NumberQuestion;