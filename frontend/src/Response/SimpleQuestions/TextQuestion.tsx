import { Box, TextField } from "@mui/material";
import { useState } from "react";
import { CommonQuestionProperties } from "./common";

export interface TextQuestionInterface extends CommonQuestionProperties {
    initialValue: string;
}

function TextQuestion(questionData: TextQuestionInterface): JSX.Element {
    const [value, setValue] = useState<string>(questionData.initialValue)
    return <Box display="inline-block">
    <TextField
      size="small"
      type="text"
      sx={{ display: "block" }}
      label={questionData.label}
      value={value}
      onChange={(event) => setValue(event.target.value)}
    />
  </Box>
}

export default TextQuestion;