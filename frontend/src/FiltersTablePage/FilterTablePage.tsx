import { Stack } from "@mui/system";
import { Card, Typography, IconButton, ListItem, List, TextField, TextFieldProps, Autocomplete, Button, Box } from "@mui/material";
import { AnswerType, SERVER_ADDRESS } from "../types/global"
import ClearIcon from '@material-ui/icons/Clear'
import AddIcon from '@material-ui/icons/Add'
import * as Test from './_testFunctions'
import { NumberFilter, TextFilter, CheckboxFilter, ChoiceFilter, AutocompleteChoiceFilter, DateFilter, AnswerFilter, AnswerVariant } from './TypedFilters'
import { getUsersList, getAnswersList, getObjectsList, getToponymsList, getFilteredTableData, TableData, makeNewObject } from "./requests";
import { useState, useEffect, useRef } from "react";
import MainTable from "./MainTable";
import { useImmer } from "use-immer"
import { useTranslation } from 'react-i18next'
import i18next from "i18next";
import axios from "axios";
import { Buffer } from "buffer";
import { Link, useNavigate } from "react-router-dom";

interface QuestionAttributes {
    id: number,
    text: string,
    type: AnswerType
    answer_block_id?: number
}

interface SingleFilterProps extends QuestionAttributes {
    setFilter: (newValue: AnswerFilter) => void
}

export interface FormResponse {
    question_blocks: {
        questions: {
            type: string,
            value: {
                id: number,
                question_type: 'DATE' | 'USER' | 'LONG_TEXT' | 'SHORT_TEXT' | 
                'MULTIPLE_CHOICE' |'CHECKBOX' | 'LOCATION' | 'NUMBER' | 'BOOLEAN' | 'RELATION',
                text: { [language: string]: string },
                relation_settings: {
                    relation_type: 'LEADER' | 'PROJECT'
                } | any,
                answer_block_id: number
            }
        }[]
    }[]
}

function SingleFilter(props : SingleFilterProps) {

    const { id, text, type, answer_block_id, setFilter } = props
    const [active, setActive] = useState(true)
    const [variants, setVariants] = useState<AnswerVariant[]>([])

    useEffect(() => {
        switch (type) {
            case AnswerType.List :
                if (answer_block_id !== undefined) {
                    getAnswersList(answer_block_id).then((answers) => {
                        setVariants(answers)
                    })
                }
                break
            case AnswerType.User :
                getUsersList().then((users) => {
                    setVariants(users)
                })
                break
            case AnswerType.Leader :
                getObjectsList('LEADER').then((leaders) => {
                    setVariants(leaders)
                })
                break
            case AnswerType.Project :
                getObjectsList('PROJECT').then((leaders) => {
                    setVariants(leaders)
                })
                break
            case AnswerType.Location :
                getToponymsList().then((toponyms) => {
                    setVariants(toponyms)
                })
        }
    }, [])

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
            filter = <ChoiceFilter variants={variants} setFilter={setFilter}/>
            break
        case AnswerType.User :
            filter = <ChoiceFilter variants={variants} setFilter={setFilter}/>
            break
        case AnswerType.Leader :
            filter = <AutocompleteChoiceFilter variants={variants} setFilter={setFilter}/>
            break
        case AnswerType.Project :
            filter = <AutocompleteChoiceFilter variants={variants} setFilter={setFilter}/>
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

function FilterTablePage({ formType } : { formType: 'LEADER' | 'PROJECT' }) {
    const { t } = useTranslation('translation', { keyPrefix: "filters" })

    const [questions, setQuestions] = useState<QuestionAttributes[]>([])
    const [filtersList, setFiltersList] = useState<JSX.Element[]>([])
    const [newQuestion, setNewQuestion] = useState<QuestionAttributes>({
        id: -1,
        text: "Loading...",
        type: AnswerType.Text,

    })
    const [filtersData, changeFiltersData] = useImmer<AnswerFilter[]>([])
    const [tableData, setTableData] = useState<TableData>({
        column_groups: [],
        rows: []
    })
    const isInitialMount = useRef(true)
    const navigate = useNavigate()

    function changeFilters(newValue: AnswerFilter, idx: number) {
        changeFiltersData(draft => { draft.splice(idx, 1, newValue) })
    }

    const handleAdd = () => {
        const newQuestionData = questions.filter(question => (question.id === newQuestion.id))
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
        const buf = Buffer.from(JSON.stringify(filtersData.filter((filter) => (filter.question_id != -1))),
                "utf8")
        const body = {
            form_type: formType,
            answer_filters: buf.toString("base64")
        }
        getFilteredTableData(body).then((data) => {
            console.log("New Table data:", data)
            setTableData(data)
        })
    }

    const questionTypesMatch = {
        'DATE': AnswerType.Date,
        'USER': AnswerType.User,
        'LONG_TEXT': AnswerType.Text,
        'SHORT_TEXT': AnswerType.Text,
        'MULTIPLE_CHOICE': AnswerType.List,
        'CHECKBOX': AnswerType.Checkbox,
        'LOCATION': AnswerType.Location,
        'NUMBER': AnswerType.Number,
        'BOOLEAN': AnswerType.List
    }

    useEffect(() => {
        if (isInitialMount.current) {
            isInitialMount.current = false
        } else {
            return
        }
        // axios.post(SERVER_ADDRESS + '/login', { login: 'coffeekey', password: 'password', language: 'ru' }, { withCredentials: true })
        //     .then((loginResponse) => {
        //         console.log(loginResponse.status, loginResponse.data)
            console.log("Mounted")
            axios.get(SERVER_ADDRESS + '/form', { params: { form_type: formType }, withCredentials: true })
                .then((response) => {
                    console.log("Form response:", response.status, response.data)
                    const data : FormResponse = response.data
                    const newQuestions : QuestionAttributes[] = []
                    data.question_blocks.forEach( (questionBlock) => {
                        questionBlock.questions.forEach((questionResponse) => {
                            if (questionResponse.type === 'question') {
                                let qType : AnswerType
                                if (questionResponse.value.question_type !== 'RELATION') {
                                    qType = questionTypesMatch[questionResponse.value.question_type]
                                } else {
                                    qType = questionResponse.value.relation_settings.relation_type == 'LEADER' ?
                                        AnswerType.Leader : AnswerType.Project
                                }
                                newQuestions.push({
                                    id: questionResponse.value.id,
                                    text: questionResponse.value.text[i18next.language.split('-', 1)[0]],
                                    type: qType,
                                    answer_block_id: questionResponse.value.answer_block_id
                                })
                            }
                        })
                    })
                    setQuestions(newQuestions)
                    setNewQuestion(newQuestions[0])
                })
                .catch((error) => {
                    console.log("Error while accessing to the /form: ", error)
                })
            // })
        handleSubmitFilter()
    }, [])

    const isCorrectSelect = () => (
        questions.filter((q) => (q.id === newQuestion.id)).length !== 0
    )

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
                        options={questions}
                        getOptionLabel={(option) => (option.text)}
                        sx={{ width: 300 }}
                        value={newQuestion}
                        onChange={(event: any, newValue: QuestionAttributes | null) => {
                            if (newValue !== null) {
                                setNewQuestion(newValue)
                            }
                        }}
                        onOpen={() => {
                            console.log("AUTOCOMPLETE:", newQuestion, questions)
                        }}
                        renderInput={(params: TextFieldProps) => <TextField {...params} label={t('choose_filter')} />}
                    />
                    <IconButton onClick={handleAdd} disabled={!isCorrectSelect()}>
                        <AddIcon htmlColor={isCorrectSelect() ? "green" : "gray"} fontSize="large"/>
                    </IconButton>
                </Stack>
            </Card>
            <Box>
                <Button variant="contained" onClick={handleSubmitFilter} sx={{ m: 2 }}>{t('submit_filter')}</Button>
                <Button variant="outlined" sx={{ m: 2 }} onClick={(event: React.MouseEvent) => {
                    makeNewObject(formType).then((id) => {
                        const link = '/' + formType.toLowerCase() + '/' + id
                        navigate(link, { replace: true })
                    })
                }}>
                    {formType === 'LEADER' ? t('add_leader') : t('add_project')}
                </Button>
            </Box>
            <h2>{t('table')}</h2>
            <Card>
                <MainTable {...tableData}/>
            </Card>
        </Stack>
    )
}

export default FilterTablePage;