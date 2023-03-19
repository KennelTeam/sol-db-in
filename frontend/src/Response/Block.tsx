import { Paper } from "@mui/material";
import Question, { QuestionInterface } from "./Question";
import {SimpleQuestionTypesList} from "./SimpleQuestions/SimpleQuestion";

export interface BlockInterface {
    title: string;
    items: Array<QuestionInterface>;
}

function Block(props: { onChange: any; blockData: BlockInterface; }): JSX.Element {
    const callBack = props.onChange;
    const blockData: BlockInterface = props.blockData;

    const components = blockData.items.map((questionData) => {
        return <Question questionData={questionData} onChange={callBack}/>
    })
    return <Paper elevation={1} sx={{ padding: "5px", marginBottom: "10px" }}>
        <h2 style={{ marginTop: "5px", marginBottom: "15px" }}>{blockData.title}</h2>
        {components}
    </Paper>
}


export default Block;