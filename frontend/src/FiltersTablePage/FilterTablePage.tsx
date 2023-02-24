import { Stack } from "@mui/system";
import { Card, Typography, IconButton, ListItem, List } from "@mui/material";
import { AnswerType } from "../types/global.d"
import ClearIcon from '@material-ui/icons/Clear'
import AddIcon from '@material-ui/icons/Add'
import * as Test from './_testFunctions'
import * as Filters from './TypedFilters'
import { useState } from "react";
import LeadersTable from "./MainTable";

interface Question {
    id: number,
    text: string,
    type: AnswerType
}

interface SingleFilterProps extends Question {
    filterIdx: number,
    deleteFilter: (idx: number) => void
}

function SingleFilter({id, text, type, filterIdx, deleteFilter} : SingleFilterProps) {

    let filter: JSX.Element

    switch (type) {
        case AnswerType.Number:
            filter = (<Filters.NumberFilter/>)
            break
        case AnswerType.Text :
            filter = (<Filters.TextFilter/>)
            break
        case AnswerType.Checkbox :
            filter = (<Filters.CheckboxFilter/>)
            break
        case AnswerType.List :
            filter = (<Filters.ChoiceFilter variants={Test._getAnswersList(id)}/>)
            break
        case AnswerType.User :
            filter = (<Filters.ChoiceFilter variants={Test._getUsersList()}/>)
            break
        case AnswerType.Leader :
            filter = (<Filters.AutocompleteChoiceFilter variants={Test._getLeadersList()}/>)
            break
        case AnswerType.Project :
            filter = (<Filters.AutocompleteChoiceFilter variants={Test._getProjectsList()}/>)
            break
        case AnswerType.Date :
            filter = (<Filters.DateFilter/>)
            break
        case AnswerType.Location :
            filter = (<Filters.ChoiceFilter variants={Test._getLocationsList()}/>)
            break
        default :
            filter = (<Typography color="error" variant="h3">Wrong AnswerType</Typography>)
    }

    const handleDelete = () => {
        deleteFilter(filterIdx)
    }

    return (
        <Stack component={ListItem} direction="row" spacing={2} justifyContent="space-between" alignItems="center" disablePadding>
            <Stack direction="row" spacing={2} justifyContent="flex-start" alignItems="center" padding={1}>
                <Typography variant="h6">{text}</Typography>
                {filter}
            </Stack>
            <IconButton onClick={handleDelete}>
                <ClearIcon color="error" fontSize="large"/>
            </IconButton>
        </Stack>
    )
}

function FilterTablePage() {

    const questions = Test._getFilterableQuestionsList()
    const [filtersList, setFiltersList] = useState<Question[]>([])
    const [newQuestion, setNewQuestion] = useState(questions[0].text)

    const handleAdd = () => {
        setFiltersList([...filtersList, questions.filter(question => (question.text === newQuestion))[0]])
    }

    function deleteFilter(idx: number) {
        // let newFiltersList = filtersList
        // newFiltersList.splice(idx, 1)
        // console.log(newFiltersList)
        setFiltersList(filtersList.filter((value: Question, index: number) => (index !== idx)))
    }

    const filters = filtersList.map((question: Question, idx: number) => (
        <SingleFilter {...question} filterIdx={idx} deleteFilter={deleteFilter}/>
    ))

    return (
        <Stack direction="column" spacing={1}>
            <List disablePadding>
                {filters}
            </List>
            <Card>
                <Stack direction="row" spacing={1} padding={2} alignItems="center">
                    <Typography variant="caption">Add filter:</Typography>
                    <Filters.ListChoice options={questions.map(question => question.text)}
                        defaultIdx={0}
                        returnValue={setNewQuestion}
                        />
                    <IconButton onClick={handleAdd}>
                        <AddIcon htmlColor="green" fontSize="large"/>
                    </IconButton>
                </Stack>
            </Card>
            <Card>
                <LeadersTable/>
            </Card>
        </Stack>
    )
}

export default FilterTablePage;