import { Stack } from "@mui/system";
import { Card, Typography, IconButton, ListItem, List, TextField, TextFieldProps, Autocomplete } from "@mui/material";
import { AnswerType } from "../types/global"
import ClearIcon from '@material-ui/icons/Clear'
import AddIcon from '@material-ui/icons/Add'
import * as Test from './_testFunctions'
import { ListChoice, NumberFilter, TextFilter, CheckboxFilter, ChoiceFilter, AutocompleteChoiceFilter, DateFilter } from './TypedFilters'
import { useState } from "react";
import MainTable from "./MainTable";
import { useTranslation } from 'react-i18next'

interface QuestionAttributes {
    id: number,
    text: string,
    type: AnswerType
}

interface SingleFilterProps extends QuestionAttributes {
    filterIdx: number
}

function SingleFilter({id, text, type, filterIdx} : SingleFilterProps) {

    const [active, setActive] = useState(true)

    let filter: JSX.Element

    switch (type) {
        case AnswerType.Number :
            filter = <NumberFilter/>
            break
        case AnswerType.Text :
            filter = <TextFilter/>
            break
        case AnswerType.Checkbox :
            filter = <CheckboxFilter/>
            break
        case AnswerType.List :
            filter = <ChoiceFilter variants={Test._getAnswersList(id)}/>
            break
        case AnswerType.User :
            filter = <ChoiceFilter variants={Test._getUsersList()}/>
            break
        case AnswerType.Leader :
            filter = <AutocompleteChoiceFilter variants={Test._getLeadersList()}/>
            break
        case AnswerType.Project :
            filter = <AutocompleteChoiceFilter variants={Test._getProjectsList()}/>
            break
        case AnswerType.Date :
            filter = <DateFilter/>
            break
        case AnswerType.Location :
            filter = <ChoiceFilter variants={Test._getLocationsList()}/>
            break
        default :
            filter = <Typography color="error" variant="h3">Wrong AnswerType</Typography>
    }

    const handleDelete = () => {
        setActive(false)
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
    const [indexes, setIndexes] = useState<number>(0)

    const handleAdd = () => {
        const newQuestionData = questions.filter(question => (question.text === newQuestion))
        if (newQuestionData.length === 0) {
            return
        }
        const curIndex: number = indexes
        console.log(curIndex)
        setFiltersList([...filtersList,
            <SingleFilter {...newQuestionData[0]} filterIdx={curIndex}/>
        ])
        setIndexes(indexes + 1)
    }

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
                        id="combo-box-demo"
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
            <h2>{t('table')}</h2>
            <Card>
                <MainTable/>
            </Card>
        </Stack>
    )
}

export default FilterTablePage;