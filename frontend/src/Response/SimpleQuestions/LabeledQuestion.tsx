import { Box } from "@mui/material";
import InputInfo, { InputInfoInterface } from "./InputInfo";
import SimpleQuestion, {SimpleQuestionInterface, SimpleQuestionType, SimpleQuestionTypesList} from "./SimpleQuestion";


export interface WithInputInfoInterface {
    inputInfo: InputInfoInterface;
}

export interface LabeledQuestionInterface extends SimpleQuestionInterface, WithInputInfoInterface {}

function LabeledQuestion(props: { questionData: SimpleQuestionTypesList; questionType: SimpleQuestionType; inputInfo: InputInfoInterface; onChange: (arg0: any) => void; }): JSX.Element {
    let questionData: SimpleQuestionTypesList = props.questionData
    let questionType: SimpleQuestionType = props.questionType
    let inputInfo: InputInfoInterface = props.inputInfo

    const questionComponent = <SimpleQuestion onChange={props.onChange}
                                              questionData={{
        questionData: questionData,
        questionType: questionType,
        inputInfo: inputInfo
    } as SimpleQuestionInterface
                                              } />;
    return (
        <Box display="inline-block" sx={{
            marginBottom: "10px",
            width: "100%",
            display: "block"
        }}>
            <InputInfo {...inputInfo} />
            {questionComponent}
        </Box>
    )
}

export default LabeledQuestion;