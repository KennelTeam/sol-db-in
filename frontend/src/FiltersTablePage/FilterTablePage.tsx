import { Stack } from "@mui/system";
import { Card, Typography, IconButton, ListItem, List, TextField, TextFieldProps, Autocomplete, Button } from "@mui/material";
import { AnswerType, SERVER_ADDRESS } from "../types/global"
import ClearIcon from '@material-ui/icons/Clear'
import AddIcon from '@material-ui/icons/Add'
import * as Test from './_testFunctions'
import { NumberFilter, TextFilter, CheckboxFilter, ChoiceFilter, AutocompleteChoiceFilter, DateFilter, AnswerFilter } from './TypedFilters'
import React, { useState } from "react";
import MainTable from "./MainTable";
import { useImmer } from "use-immer"
import { useTranslation } from 'react-i18next'
import axios from "axios";

interface QuestionAttributes {
    id: number,
    text: string,
    type: AnswerType
}

interface SingleFilterProps extends QuestionAttributes {
    setFilter: (newValue: AnswerFilter) => void
}

function SingleFilter(props : SingleFilterProps) {

    const { id, text, type, setFilter } = props
    const [active, setActive] = useState(true)

    let filter: JSX.Element

    switch (type) {
        case AnswerType.Number :
            filter = <NumberFilter setFilter={setFilter}/>
            break
        case AnswerType.Text :
            filter = <TextFilter setFilter={setFilter}/>
            break
        case AnswerType.Checkbox :
            filter = <CheckboxFilter setFilter={setFilter}/>
            break
        case AnswerType.List :
            filter = <ChoiceFilter variants={Test._getAnswersList(id)} setFilter={setFilter}/>
            break
        case AnswerType.User :
            filter = <ChoiceFilter variants={Test._getUsersList()} setFilter={setFilter}/>
            break
        case AnswerType.Leader :
            filter = <AutocompleteChoiceFilter variants={Test._getLeadersList()} setFilter={setFilter}/>
            break
        case AnswerType.Project :
            filter = <AutocompleteChoiceFilter variants={Test._getProjectsList()} setFilter={setFilter}/>
            break
        case AnswerType.Date :
            filter = <DateFilter setFilter={setFilter}/>
            break
        case AnswerType.Location :
            filter = <AutocompleteChoiceFilter variants={Test._getLocationsList()} setFilter={setFilter}/>
            break
        default :
            filter = <Typography color="error" variant="h3">Wrong AnswerType</Typography>
    }

    const handleDelete = () => {
        setActive(false)
        setFilter({
            question_id: -1
        })
    }

    return (
        <div>{ active ? (
            <Stack component={ListItem}
                direction="row"
                spacing={2}
                justifyContent="space-between"
                alignItems="center"
                disablePadding
                >
                <Stack direction="row"
                    spacing={2}
                    justifyContent="flex-start"
                    alignItems="center"
                    padding={1}
                    >
                    <Typography variant="h6">{text}</Typography>
                    {filter}
                </Stack>
                <IconButton onClick={handleDelete}>
                    <ClearIcon color="error" fontSize="large"/>
                </IconButton>
            </Stack>
        ) : null }
        </div>
    )
}

function FilterTablePage() {
    const { t } = useTranslation('translation', { keyPrefix: "filters" })

    const questions = Test._getFilterableQuestionsList()
    const [filtersList, setFiltersList] = useState<JSX.Element[]>([])
    const [newQuestion, setNewQuestion] = useState(questions[0].text)
    const [filtersData, changeFiltersData] = useImmer<AnswerFilter[]>([])

    function changeFilters(newValue: AnswerFilter, idx: number) {
        changeFiltersData(draft => { draft.splice(idx, 1, newValue) })
    }

    const handleAdd = () => {
        const newQuestionData = questions.filter(question => (question.text === newQuestion))
        if (newQuestionData.length === 0) {
            return
        }
        const idx = filtersData.length
        changeFiltersData(draft => { draft.push({ question_id: -1 }) })
        console.log(filtersData)

        setFiltersList([...filtersList,
            <SingleFilter {...newQuestionData[0]} setFilter={(newValue: AnswerFilter) => {
                if (newValue.question_id !== -1) {
                    newValue.question_id = newQuestionData[0].id
                }
                changeFilters(newValue, idx)
            }}/>
        ])
    }

    const handleSubmitFilter = () => {
        const body = {
            form_type: "LEADER", // later must be a parameter from props
            answer_filters: filtersData.filter((f) => f.question_id !== -1)
        }
        console.log("PUT request to /forms with data:", body)
        const newTableData = axios.put(SERVER_ADDRESS + '/forms', body)
    }

    console.log(filtersData)
    return (
        <Stack direction="column" spacing={1}>
            <h2>{t('title')}</h2>
            <List disablePadding>
                {filtersList}
            </List>
            <Card>
                <Stack direction="row" spacing={1} padding={2} alignItems="center">
                    <Typography variant="caption">Add filter:</Typography>
                    <Autocomplete
                        disablePortal
                        options={questions.map(question => question.text)}
                        sx={{ width: 300 }}
                        value={newQuestion}
                        onChange={(event: any, newValue: string | null) => {
                            if (newValue !== null) {
                                setNewQuestion(newValue)
                            }
                        }}
                        renderInput={(params: TextFieldProps) => <TextField {...params} label={t('choose_filter')} />}
                    />
                    <IconButton onClick={handleAdd}>
                        <AddIcon htmlColor="green" fontSize="large"/>
                    </IconButton>
                </Stack>
            </Card>
            <Button variant="contained" onClick={handleSubmitFilter}>{t('submit_filter')}</Button>
            <h2>{t('table')}</h2>
            <Card>
                <MainTable/>
            </Card>
        </Stack>
    )
}

export default FilterTablePage;