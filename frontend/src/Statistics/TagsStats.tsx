import React, { useEffect } from 'react'
import { TableCell, TableRow, TableHead, Table, TableBody, TableContainer } from '@mui/material'
import styled from '@emotion/styled'
import axios from 'axios'
import { SERVER_ADDRESS } from '../types/global'
import { useTranslation } from 'react-i18next'

const StyledTableCell = styled(TableCell)({
    fontSize: '13px',
    size: 'small',
    padding: 6,
    borderRightWidth: 1,
    borderRightColor: "lightgray",
    borderRightStyle: "solid",
    margin: 3,
    textAlign: "center",
    minWidth: 150
})

export default function TagsStats() {

  const [data, setData] = React.useState<number[][]>([])
  const [columns, setColumns] = React.useState<string[]>([])
  const [rows, setRows] = React.useState<string[]>([])

  const { t } = useTranslation('translation', { keyPrefix: 'statistics' })

  useEffect(() => {
    axios.get(SERVER_ADDRESS + '/tags_statistics', { withCredentials: true })
      .then((response) => {
        console.log("Successfully get data from /tags_statistics:", response.data)
        setData(response.data.values)
        setColumns(response.data.columns.map((column: { text: string }) => (column.text)))
        setRows(response.data.rows.map((row: { text: string }) => (row.text)))
      })
  }, [])
  
  return (
    <div>
      <h1>{t("tags-stats")}</h1>
      <TableContainer sx={{ overflowX: 'scroll', scrollMarginBlockEnd: 60}}>
        <Table size="small" stickyHeader>
          <TableHead>
            <TableRow>
              <StyledTableCell style={{ fontWeight: "bold" }}>
                Tags
              </StyledTableCell>
              {columns.map((name: string) => (
                <StyledTableCell style={{ fontWeight: "bold" }}>
                  {name}
                </StyledTableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((rowName: string, idx: number) => (
              <TableRow>
                <StyledTableCell style={{ fontWeight: "bold" }}>
                  {rowName}
                </StyledTableCell>
                {data[idx].map((value: number) => (<StyledTableCell>{value}</StyledTableCell>))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  )
}
