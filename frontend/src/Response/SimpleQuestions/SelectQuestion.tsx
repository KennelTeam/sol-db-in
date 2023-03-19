import { Autocomplete, Box, TextField } from "@mui/material";
import { CommonQuestionProperties } from "./common";
import {useState} from "react";

export interface SingleSelectItemInterface {
  id: number;
  name: string;
}

export interface SelectQuestionInterface extends CommonQuestionProperties {
  initialValue: string | null; // value
  dataToChooseFrom: Array<SingleSelectItemInterface>;
}

function SelectQuestion(props: { questionData: SelectQuestionInterface; onChange: (arg0: SelectQuestionInterface) => void; }): JSX.Element {
  let questionData: SelectQuestionInterface = props.questionData
  const [value, setValue] = useState(questionData)
  const [ans, setAns] = useState(questionData.initialValue)

  return <Box display="inline-block" sx={{ verticalAlign: "middle" }}>
    <Box display="block">
      <Autocomplete
        disablePortal
        options={questionData.dataToChooseFrom.map((x) => x.name)}
        value={ans}
        size="small"
        sx={{ display: "block", minWidth: "300px" }}
        renderInput={(params) => <TextField {...params}
          label={questionData.label}
        />}
        onChange={(e, val) => {
          e.preventDefault()
          let data = value
          data.initialValue = val
          data.value = data.dataToChooseFrom.find((item) => item.name == val)?.id
          setAns(val)
          setValue(data)
          props.onChange(value)
        }
        }
      />
    </Box>
  </Box>
}

export default SelectQuestion;