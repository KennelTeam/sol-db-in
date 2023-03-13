import { Box, Paper } from "@mui/material";
import Block from "./Block";
import { ResponseDataInterface } from "./ResponseData";

function Response(responseData: ResponseDataInterface): JSX.Element {
    const blocksComponents = responseData.blocks.map((blockData) => {return <Block {...blockData}/>})
    return <Box>
        <h1>{responseData.title}</h1>
        {blocksComponents}
    </Box>
}

export default Response;