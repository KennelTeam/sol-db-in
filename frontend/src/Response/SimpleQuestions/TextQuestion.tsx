import { Box, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { CommonQuestionProperties } from "./common";
import {TextareaAutosize} from "@mui/core";

export interface TextQuestionInterface extends CommonQuestionProperties {
    initialValue: string;
}

function TextQuestion(props: { questionData: TextQuestionInterface; onChange: (arg0: TextQuestionInterface) => void; }): JSX.Element {
    let questionData: TextQuestionInterface = props.questionData
    const [value, setValue] = useState(questionData)
    const [text, setText] = useState(questionData.initialValue)

    useEffect(() => {
        setValue(props.questionData)
        setText(props.questionData.initialValue)
    }, [props.questionData])

    return <Box
      component={TextareaAutosize}
      display="inline-block"
      sx={{width: "100%"}}
      value={text}
      minRows={3}
      onChange={(event) => {
          let data = value
          data.initialValue = event.target.value
          data.value = data.initialValue
          setText(event.target.value)
          setValue(data)
          props.onChange(value)
      }}
  />
}

export default TextQuestion;