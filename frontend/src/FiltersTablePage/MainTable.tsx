import { TableCell, TableRow, TableHead, Table, List, ListItem, TableBody, Card, TableContainer, TablePagination, TableSortLabel } from '@mui/material'
import { Link } from 'react-router-dom'
import CheckIcon from '@mui/icons-material/Check'
import { _getRows, _getColumns } from './_testFunctions'
import { Box, styled } from '@mui/system'
import { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { visuallyHidden } from '@mui/utils'

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
function descendingComparator(a: Row, b: Row, orderBy: number) {
    let a_n: number | string = 0;
    let b_n: number | string = 0;
    try {
        a_n = a.columns[orderBy].length > 0 ? Number(a.columns[orderBy][0].data) : 0
        b_n = b.columns[orderBy].length > 0 ? Number(b.columns[orderBy][0].data) : 0
    } catch(e) {
        a_n = a.columns[orderBy].length > 0 ? a.columns[orderBy][0].data : ""
        b_n = b.columns[orderBy].length > 0 ? b.columns[orderBy][0].data : ""
    }
    if (b_n < a_n) {
        return -1;
    }
    if (b_n > a_n) {
        return 1;
    }
    return 0
}
  
type Order = 'asc' | 'desc';
  
function getComparator(
        order: Order,
        orderBy: number,
    ): (
        a: Row,
        b: Row,
    ) => number {
    return order === 'desc'
      ? (a, b) => descendingComparator(a, b, orderBy)
      : (a, b) => -descendingComparator(a, b, orderBy);
}

function stableSort(array: readonly Row[], comparator: (a: Row, b: Row) => number) {
    const stabilizedThis = array.map((el, index) => [el, index] as [Row, number]);
    console.log("stabilizedThis:", array, stabilizedThis)
    stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0])
      if (order !== 0) {
        return order;
      }
      return a[1] - b[1];
    })
    console.log("stabilizedThis sorted:", stabilizedThis)
    return stabilizedThis.map((el) => el[0]);
}

export interface Row {
    id: number,
    columns: {
        link?: string,
        data: string
    }[][]
}

export interface HeadColumn {
    name: string,
    numeric: boolean,
    id: number
}

interface HeadProps {
    columns: HeadColumn[],
    order: Order,
    orderBy: number
    onRequestSort: (event: React.MouseEvent<unknown>, newOrderBy: number) => void
}

export interface TableData {
    headColumns: HeadColumn[]
    rows: Row[]
}

function Head(props: HeadProps) {

    const { columns, order, orderBy, onRequestSort } = props

    const createSortHandler =
    (newOrderBy: number) => (event: React.MouseEvent<unknown>) => {
      onRequestSort(event, newOrderBy);
    }
    return (
        <TableHead>
            <TableRow>
                <StyledTableCell style={{ fontWeight: "bold" }}>
                    id
                </StyledTableCell>
                {columns.map(({ name, numeric, id }) => (
                    <StyledTableCell style={{ fontWeight: "bold" }}>
                        {numeric ? 
                            (
                                <TableSortLabel
                                    active={orderBy === id}
                                    direction={orderBy === id ? order : 'asc'}
                                    onClick={createSortHandler(id)}
                                >
                                {name}
                                {orderBy === id ? (
                                    <Box component="span" sx={visuallyHidden}>
                                    {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                                    </Box>
                                ) : null}
                                </TableSortLabel>
                            )
                        : name}
                    </StyledTableCell>
                ))}
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
    const [order, setOrder] = useState<Order>('asc');
    const [orderBy, setOrderBy] = useState<number>(0)
    const [visibleRows, setVisibleRows] = useState<Row[]>([])

    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    }

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    }
    console.log(props.headColumns)

    const handleRequestSort = (event: React.MouseEvent<unknown>, newOrderBy: number) => {
          const isAsc = orderBy === newOrderBy && order === 'asc';
          const toggledOrder = isAsc ? 'desc' : 'asc';
          setOrder(toggledOrder)
          setOrderBy(newOrderBy)

          console.log("handleRequestSort:", visibleRows)
          const sortedRows = stableSort(visibleRows,
            getComparator(toggledOrder, newOrderBy));
          const updatedRows = sortedRows.slice(
            page * rowsPerPage,
            page * rowsPerPage + rowsPerPage,
          );
          console.log("Sorted Rows:", sortedRows)
          setVisibleRows(updatedRows);
        }

    const head : HeadProps = {
        columns: props.headColumns,
        order: 'asc',
        orderBy: 0,
        onRequestSort: handleRequestSort
    }

    useEffect(() => {
        console.log("useEffect:", props.rows)
        const newRows : Row[] = props.rows.map(
            (row) => (JSON.parse(JSON.stringify(row)))
            )
        if (props.rows.length > 0) {
            console.log("New Rows:", JSON.parse(JSON.stringify(props.rows)))
            setVisibleRows(JSON.parse(JSON.stringify(props.rows)))
        }
        console.log("visibleRows:", visibleRows)
    }, [props.rows])

    return (
        <Box component={Card}>
            <TableContainer>
                <Table size="small" stickyHeader>
                    <Head {...head}/>
                    <TableBody>
                        {visibleRows
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
