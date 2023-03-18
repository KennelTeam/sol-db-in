import { Box, Checkbox, FormControl, FormControlLabel } from "@mui/material";
import { useState } from "react";
import { CommonQuestionProperties } from "./common";

export interface SingleCheckboxQuestionInterface extends CommonQuestionProperties {
    initialValue: boolean;
}

export interface CheckboxQuestionInterface {
    questions: SingleCheckboxQuestionInterface[];
}

function SingleCheckboxQuestion(questionData: SingleCheckboxQuestionInterface): JSX.Element {
    const [value, setValue] = useState(questionData.initialValue);
    return <Box display="inline-block">
        <FormControlLabel
            control={<Checkbox checked={value} onChange={(event) => setValue(event.target.checked)} />}
            label={questionData.label}
            sx={{ whiteSpace: "nowrap" }}
        />
    </Box>
}


function CheckboxQuestion(questionData: CheckboxQuestionInterface): JSX.Element {
    const components = questionData.questions.map((question) => <SingleCheckboxQuestion {...question} />)
    return <Box display="inline-block">
        <FormControl sx={{display: "inline-block"}}>
            {components}
        </FormControl>
    </Box>
}

export default CheckboxQuestion;