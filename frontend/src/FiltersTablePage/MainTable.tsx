import { TableCell, TableRow, TableHead, Table, List, ListItem, TableBody, Card, TableContainer, TablePagination } from '@mui/material'
import { Link } from 'react-router-dom'
import CheckIcon from '@mui/icons-material/Check'
import { Row, _getRows, _getColumns } from './_testFunctions'
import { Box, styled } from '@mui/system'
import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { TableData } from './requests'

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
                <StyledTableCell style={{ fontWeight: "bold" }}>
                    id
                </StyledTableCell>
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

export default function MainTable(props: TableData) {
    const { t } = useTranslation('translation', { keyPrefix: "filters" })

    const [rowsPerPage, setRowsPerPage] = useState(10)
    const [page, setPage] = useState<number>(0)

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    }

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    }
    console.log(props.rows)
    console.log(props.column_groups)
    return (
        <Box component={Card}>
            <TableContainer>
                <Table size="small" stickyHeader>
                    <Head columnGroups={props.column_groups}/>
                    <TableBody>
                        {props.rows
                            .slice(page * rowsPerPage, (page + 1) * rowsPerPage)
                            .map((row: Row) => (<RenderRow {...row}/>))}
                    </TableBody>
                </Table>
            </TableContainer>
            <TablePagination
                rowsPerPage={rowsPerPage}
                count={props.rows.length}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
                labelRowsPerPage={t('rows_per_page')}
                showFirstButton
                showLastButton
            />
        </Box>
    )
}
