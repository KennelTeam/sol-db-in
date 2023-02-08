import { Autocomplete, Box, TextField } from "@mui/material";
import { CommonQuestionProperties } from "./common";

interface SingleSelectItemInterface {
  id: number;
  name: string;
}

export interface SelectQuestionInterface extends CommonQuestionProperties {
  initialValue: number; // id
  dataToChooseFrom: Array<SingleSelectItemInterface>;
}

function SelectQuestion(questionData: SelectQuestionInterface): JSX.Element {
  return <Box display="inline-block" sx={{ verticalAlign: "middle" }}>
    <Box display="block">
      <Autocomplete
        disablePortal
        options={questionData.dataToChooseFrom.map((x) => x.name)}
        size="small"
        sx={{ display: "block", minWidth: "300px" }}
        renderInput={(params) => <TextField {...params}
          label={questionData.label}
        />}
      />
    </Box>
  </Box>
}

export default SelectQuestion;