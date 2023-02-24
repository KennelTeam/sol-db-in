import { TableCell, TableRow, TableHead, Table, List, ListItem, TableBody, Card, TableContainer } from '@mui/material'
import { Link } from 'react-router-dom'
import CheckIcon from '@mui/icons-material/Check'
import { Row, _getRows, _getColumns } from './_testFunctions'
import { Box, styled } from '@mui/system'

const StyledTableCell = styled(TableCell)({
    fontSize: '11px',
    size: 'small',
    padding: 6,
    borderRightWidth: 1,
    borderRightColor: "lightgray",
    borderRightStyle: "solid",
    margin: 3,
    textAlign: "center"
})

function Head({ columnGroups }: { columnGroups: { name: string, columns: string[] }[] }) {

    return (
        <TableHead>
            <TableRow>
                {columnGroups.map((group) => (
                    <StyledTableCell colSpan={group.columns.length} style={{ fontWeight: "bold" }}>
                        {group.name}
                    </StyledTableCell>
                ))}
            </TableRow>
            <TableRow>
                {columnGroups.map((group) => (
                    group.columns.map((columnName) => (
                    <StyledTableCell style={{ fontWeight: "bold" }}>
                        {columnName}
                    </StyledTableCell>
                ))))}
            </TableRow>
        </TableHead>
    )
}

function RenderRow(props: Row) {

    const SingleElement = (props: {data: string, link?: string}) : JSX.Element => {
        if (props.link !== undefined) {
            return <Link to={props.link}>{props.data}</Link>
        } else {
            return <>{props.data === "*yes*" ? <CheckIcon fontSize="small" htmlColor="green"/> : props.data }</>
        }
    }

    return (
        <TableRow>
            <StyledTableCell>{props.id}</StyledTableCell>
            <StyledTableCell>
                <Link to={props.link}>{props.name}</Link>
            </StyledTableCell>
            {props.columns.map((col) => {
                if (col.length === 1) {
                    return (
                        <StyledTableCell>
                            <SingleElement {...col[0]}/>
                        </StyledTableCell>
                    )
                } else {
                    return (
                        <StyledTableCell>
                            <List disablePadding>
                                {col.map((element: {data: string, link?: string}) => (
                                    <ListItem disablePadding>
                                        <SingleElement {...element}/>
                                    </ListItem>
                                ))}
                            </List>
                        </StyledTableCell>
                    )
                }
            })}
        </TableRow>
    )
}

export default function LeadersTable() {

    const rows = _getRows()

    return (
        <Box component={Card}>
            <TableContainer>
                <Table size="small" stickyHeader>
                    <Head columnGroups={_getColumns()}/>
                    <TableBody>
                        {rows.map((row: Row) => (<RenderRow {...row}/>))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    )
}
