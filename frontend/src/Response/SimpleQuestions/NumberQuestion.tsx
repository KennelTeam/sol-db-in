import { Box, TextField } from "@mui/material";
import { useState } from "react";
import { CommonQuestionProperties } from "./common";

export interface NumberQuestionInterface extends CommonQuestionProperties {
    initialValue: number;
}

function NumberQuestion(questionData: NumberQuestionInterface): JSX.Element {
    const [value, setValue] = useState<number | null>(questionData.initialValue)
    return <Box display="inline-block">
        <TextField
        type="number"
        label={questionData.label}
        size="small"
        sx={{ display: "inline-block", maxWidth: "200px", minWidth: "120px" }}
        value={value? value.toString() : 0}
        onChange={(event) => {
            if (!event.target.validity.badInput) {
                if (event.target.value === '') setValue(null)
                else setValue(+event.target.value)
            }
            event.preventDefault()
        }}
        />
    </Box>
}

export default NumberQuestion;