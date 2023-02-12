import { Paper } from "@mui/material";
import Question, { QuestionInterface } from "./Question";

export interface BlockInterface {
    title: string;
    items: Array<QuestionInterface>;
}

function Block(blockData: BlockInterface): JSX.Element {
    const components = blockData.items.map((questionData) => {
        return <Question {...questionData}/>
    })
    return <Paper elevation={1} sx={{ padding: "5px", marginBottom: "10px" }}>
        <h2 style={{ marginTop: "5px", marginBottom: "15px" }}>{blockData.title}</h2>
        {components}
    </Paper>
}


export default Block;