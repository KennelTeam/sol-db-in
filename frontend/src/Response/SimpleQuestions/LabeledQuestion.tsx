import { Box } from "@mui/material";
import InputInfo, { InputInfoInterface } from "./InputInfo";
import SimpleQuestion, { SimpleQuestionInterface } from "./SimpleQuestion";


export interface WithInputInfoInterface {
    inputInfo: InputInfoInterface;
}

export interface LabeledQuestionInterface extends SimpleQuestionInterface, WithInputInfoInterface {}

function LabeledQuestion(questionData: LabeledQuestionInterface): JSX.Element {
    const questionComponent = <SimpleQuestion questionType={questionData.questionType} questionData={questionData.questionData} />;
    return (
        <Box display="inline-block" sx={{
            marginBottom: "10px"
        }}>
            <InputInfo {...questionData.inputInfo} />
            {questionComponent}
        </Box>
    )
}

export default LabeledQuestion;