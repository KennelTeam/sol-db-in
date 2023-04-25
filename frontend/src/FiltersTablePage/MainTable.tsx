import { TableCell, TableRow, TableHead, Table, List, ListItem, TableBody, Card, TableContainer, TablePagination } from '@mui/material'
import { Link } from 'react-router-dom'
import CheckIcon from '@mui/icons-material/Check'
import { Row, _getRows, _getColumns } from './_testFunctions'
import { Box, styled } from '@mui/system'
import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { TableData } from './requests2API'

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

function Head({ columnGroups, callBack }: { columnGroups: { name: string, columns: string[] }[], callBack:(index: number)=>void }) {

    return (
        <TableHead>
            <TableRow>
                <StyledTableCell style={{ fontWeight: "bold" }}>
                    id
                </StyledTableCell>
                {columnGroups.map((group, group_index) => (
                    group.columns.map(columnName => (
                    <StyledTableCell style={{ fontWeight: "bold" }} onClick={(item) => {callBack(group_index)}}>
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

    props.columns = props.columns.map(col => col.filter((value, index) => {
        if (col[index].data == "DELETED") {
            return false;
        }
        for (let i = 0; i < index; ++i) {
            if (col[i].data == value.data) {
                return false;
            }
        }
        return true;
    }))

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

    const [rowsPerPage, setRowsPerPage] = useState(50)
    const [page, setPage] = useState<number>(0)

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    }

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    }

    let sortTable = (index: number) => {
        /*console.log("sorting")
        console.log(props.rows)
        props.rows.sort((rowl ,rowr) => {
            console.log(rowl)
            console.log(rowr)
            if (rowl === undefined) {
                return 1
            }
            if (rowr === undefined) {
                return -1
            }
            // @ts-ignore
            console.log(rowl[index])
            // @ts-ignore
            console.log(rowr[index])
            // @ts-ignore
            if (rowl[index].data < rowr[index].data) {
                return -1;
                // @ts-ignore
            } else if (rowl[index] === rowr[index]) {
                return 0;
            }
            return 1;
        })
        console.log(props.rows)*/
    }

    console.log(props.rows)
    console.log(props.column_groups)
    return (
        <Box component={Card}>
            <TableContainer>
                <Table size="small" stickyHeader>
                    <Head columnGroups={props.column_groups} callBack={sortTable}/>
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
