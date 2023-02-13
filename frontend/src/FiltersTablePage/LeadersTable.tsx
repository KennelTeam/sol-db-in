import { TableCell, TableRow, TableHead, Table, List, ListItem, TableBody, Card, TableContainer } from '@mui/material'
import { Link } from 'react-router-dom'
import CheckIcon from '@mui/icons-material/Check'
import { leaderData, _getLeadersData } from './_testFunctions'
import { Box, styled } from '@mui/system'

const StyledTableCell = styled(TableCell)({
    fontSize: '11px',
    size: 'small',
    padding: 6,
    borderRightWidth: 1,
    borderRightColor: "lightgray",
    borderRightStyle: "solid",
    margin: 3
})

function Head() {
    const columns = ['id', 'Name', 'City', 'Category', 'Projects', 'Interviewer', 'Date',
                'Variant', 'Comment', 'Outcoming', 'Incoming', 'Check', 'Finish']

    return (
        <TableHead>
            <TableRow>
                <StyledTableCell colSpan={5} style={{ fontWeight: "bold" }}>
                    General
                </StyledTableCell>
                <StyledTableCell colSpan={4} style={{ fontWeight: "bold" }}>
                    Interview
                </StyledTableCell>
                <StyledTableCell colSpan={2} style={{ fontWeight: "bold" }}>
                    Recomendations
                </StyledTableCell>
                <StyledTableCell colSpan={2} style={{ fontWeight: "bold" }}>
                    Status
                </StyledTableCell>
            </TableRow>
            <TableRow>
                {columns.map((columnName) => (
                    <StyledTableCell style={{ fontWeight: "bold" }}>
                        {columnName}
                    </StyledTableCell>
                ))}
            </TableRow>
        </TableHead>
    )
}

function LeaderRow(props: leaderData) {

    const { id, name, city, category, projects, interviewer, date, interviewVariant,
        interviewComment, recomendationsOut, recomendationsIn, isCheck, isFinish } = props

    return (
        <TableRow>
            <StyledTableCell align="right">{id}</StyledTableCell>
            <StyledTableCell align="left">
                <Link to={"/leader/" + id}>{name}</Link>
            </StyledTableCell>
            <StyledTableCell align="left">{city}</StyledTableCell>
            <StyledTableCell align="left">{category}</StyledTableCell>
            <StyledTableCell align="left">
                <List disablePadding>
                {projects.map((project) => (
                    <ListItem disablePadding>
                        <Link to={"/project/" + project.id}>{project.name}</Link>
                    </ListItem>
                ))}
                </List>
            </StyledTableCell>
            <StyledTableCell align="left">{interviewer}</StyledTableCell>
            <StyledTableCell align="center">{date}</StyledTableCell>
            <StyledTableCell align="left">{interviewVariant}</StyledTableCell>
            <StyledTableCell align="left">{interviewComment}</StyledTableCell>
            <StyledTableCell align="right">{recomendationsOut}</StyledTableCell>
            <StyledTableCell align="right">{recomendationsIn}</StyledTableCell>
            <StyledTableCell align="center">
                {isCheck ? <CheckIcon htmlColor='green' fontSize="small"></CheckIcon> : "-"}
            </StyledTableCell>
            <StyledTableCell align="center">
                {isFinish ? <CheckIcon htmlColor='green' fontSize="small"></CheckIcon> : "-"}
            </StyledTableCell>
        </TableRow>
    )
}

export default function LeadersTable() {

    const leaders = _getLeadersData()

    return (
        <Box component={Card}>
            <TableContainer>
                <Table size="small" stickyHeader>
                    <Head/>
                    <TableBody>
                        {leaders.map((leader) => (<LeaderRow {...leader}/>))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    )
}
