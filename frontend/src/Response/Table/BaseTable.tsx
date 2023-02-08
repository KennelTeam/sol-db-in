import { Box, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";
import { WithInputInfoInterface } from "../SimpleQuestions/LabeledQuestion";


export interface BaseTableInterface extends WithInputInfoInterface {
    rows: Array<Array<JSX.Element>>;
}

export enum TableType {
    FIXED_TABLE = "FIXED_TABLE",
    DYNAMIC_TABLE = "DYNAMIC_TABLE",
}


function BaseTable(baseTableData: BaseTableInterface): JSX.Element {
    return (
        <Box display="block" component={Paper} sx={{
            marginTop: "40px",
            marginRight: "40%",
            paddingTop: "1px"
        }}>
            {baseTableData.inputInfo.title ? <h3 style={{ marginLeft: "10px", marginBottom: 0 }}>{baseTableData.inputInfo.title}</h3> : null}
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            {baseTableData.rows[0].map((component) => <TableCell>{component}</TableCell>)}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {baseTableData.rows.slice(1).map((row: JSX.Element[]) => (
                            <TableRow>
                                {row.map((component) => <TableCell>{component}</TableCell>)}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
}

export default BaseTable;
