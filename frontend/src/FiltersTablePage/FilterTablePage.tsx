import { Box, Stack } from "@mui/system";
import { Card, Typography, IconButton, } from "@mui/material";
import { AnswerType } from "../types/global.d"
import ClearIcon from '@material-ui/icons/Clear'
import AddIcon from '@material-ui/icons/Add'
import * as Test from './_testFunctions'
import * as Filters from './TypedFilters'
import { useState } from "react";

interface Question {
    id: number,
    text: string,
    type: AnswerType
}

function SingleFilter({id, text, type} : Question) {

    let filter: JSX.Element

    switch (type) {
        case AnswerType.Number :
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

    return (
        <Stack component={Card} direction="row" spacing={2} justifyContent="space-between" alignItems="center" variant="outlined">
            <Stack direction="row" spacing={2} justifyContent="flex-start" alignItems="center" padding={1}>
                <Typography variant="h6">{text}</Typography>
                {filter}
            </Stack>
            <IconButton>
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

    const filters = filtersList.map((question: {id: number, text: string, type: AnswerType}) => (
        <SingleFilter {...question}/>
    ))

    return (
        <Stack direction="column" spacing={1} >
            {filters}
            <Stack direction="row" spacing={1} >
                <Filters.ListChoice options={questions.map(question => question.text)}
                    defaultIdx={0}
                    returnValue={setNewQuestion}
                    />
                <IconButton onClick={handleAdd}>
                    <AddIcon htmlColor="green" fontSize="large"/>
                </IconButton>
            </Stack>
        </Stack>
    )
}

export default FilterTablePage;