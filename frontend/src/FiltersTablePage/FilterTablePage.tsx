import {Stack} from "@mui/system";
import {
    Autocomplete,
    Box,
    Button,
    Card,
    Dialog,
    IconButton,
    List,
    ListItem,
    TextField,
    TextFieldProps,
    Typography
} from "@mui/material";
import {AnswerType, SERVER_ADDRESS} from "../types/global"
import ClearIcon from '@material-ui/icons/Clear'
import AddIcon from '@material-ui/icons/Add'
import {
    AnswerFilter,
    AnswerVariant,
    AutocompleteChoiceFilter,
    ChoiceFilter,
    DateFilter,
    NumberFilter,
    TextFilter
} from './TypedFilters'
import {
    getAnswersList,
    getFilteredTableData,
    getObjectsList,
    getToponymsList,
    getUsersList,
    makeNewObject
} from "./requests2API";
import {useEffect, useRef, useState} from "react";
import MainTable, {TableData} from "./MainTable";
import {useImmer} from "use-immer"
import {useTranslation} from 'react-i18next'
import i18next from "i18next";
import axios from "axios";
import {Buffer} from "buffer";
import {useNavigate} from "react-router-dom";
import AddObjectPopup from "./AddObjectPopup";

interface QuestionAttributes {
    default_filter: boolean | null,
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
                formatting_settings: object;
                id: number,
                question_type: 'DATE' | 'USER' | 'LONG_TEXT' | 'SHORT_TEXT' | 
                'MULTIPLE_CHOICE' |'CHECKBOX' | 'LOCATION' | 'NUMBER' | 'BOOLEAN' | 'RELATION',
                text: { [language: string]: string },
                relation_settings: {
                    relation_type: 'LEADER' | 'PROJECT'
                } | any,
                answer_block_id: number,
                default_filter: boolean
            }
        }[]
    }[]
}

function SingleFilter(props : SingleFilterProps) {

    const { id, text, type, answer_block_id, setFilter } = props
    const [active, setActive] = useState(true)
    const [variants, setVariants] = useState<AnswerVariant[]>([])
    const navigate = useNavigate()

    useEffect(() => {
        switch (type) {
            case AnswerType.Checkbox:
            case AnswerType.List :
                if (answer_block_id !== undefined) {
                    getAnswersList(answer_block_id, navigate).then((answers) => {
                        setVariants(answers)
                    })
                }
                break
            case AnswerType.User :
                getUsersList(navigate).then((users) => {
                    setVariants(users)
                })
                break
            case AnswerType.Leader :
                getObjectsList('LEADER', navigate).then((leaders) => {
                    setVariants(leaders)
                })
                break
            case AnswerType.Project :
                getObjectsList('PROJECT', navigate).then((leaders) => {
                    setVariants(leaders)
                })
                break
            case AnswerType.Location :
                getToponymsList(navigate).then((toponyms) => {
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
            filter = <ChoiceFilter variants={variants} setFilter={setFilter}/>
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
            filter = <AutocompleteChoiceFilter variants={variants} setFilter={setFilter}/>
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
        default_filter: false
    })
    const [name_substr, setNameSubstr] = useState<string>("")
    const [filtersData, changeFiltersData] = useImmer<AnswerFilter[]>([])
    const [tableData, setTableData] = useState<TableData>({
        headColumns: [],
        rows: []
    })
    const [addDialogOpen, setAddDialogOpen] = useState<boolean>(false)

    const [names, setNames] = useState<AnswerVariant[]>([])
    const [searchInputValue, setSearchInputValue] = useState<string>("")
    const [searchValue, setSearchValue] = useState<AnswerVariant>({
        name: "",
        id: -1
    })

    const handleSearchChange = (event: React.SyntheticEvent, newValue: string | AnswerVariant | null) => {
        setSearchValue(newValue as AnswerVariant)
    }

    const handleSearchInputChange = (event: React.SyntheticEvent, newInputValue: string | null) => {
        if (newInputValue !== null) {
            setSearchInputValue(newInputValue as string)
            setNameSubstr(newInputValue as string)
        }
    }

    const isInitialMount = useRef(true)
    const navigate = useNavigate()

    function changeFilters(newValue: AnswerFilter, idx: number) {
        changeFiltersData(draft => { draft.splice(idx, 1, newValue) })
    }

    const add = (nQuestions: QuestionAttributes[], questions: QuestionAttributes[]) => {
        console.log("ADDING")
        const newQuestionData = questions.filter(question => {
            for (let q of nQuestions) {
                if (q.id === question.id) {
                    return true;
                }
            }
            return false;
        })
        console.log(newQuestionData)
        console.log(questions)
        if (newQuestionData.length === 0) {
            return
        }
        const idx = filtersData.length
        changeFiltersData(draft => { draft.push({ question_id: -1 }) })
        console.log(filtersData)

        setFiltersList([...filtersList,
        ...newQuestionData.map(item => <SingleFilter {...item} setFilter={(newValue: AnswerFilter) => {
                if (newValue.question_id !== -1) {
                    newValue.question_id = item.id
                }
                changeFilters(newValue, idx)
            }}/>)
        ])
    }

    const handleAdd = () => {
        add([newQuestion], questions)
    }

    const handleSubmitFilter = () => {
        let filters = filtersData.filter((item) => {
            if (item.exact_values) {
                if (item.exact_values.length == 0) {
                    return false;
                }
            }
            return true;
        })
        console.log(filters)
        console.log("FILTERS")
        console.log(name_substr)
        const buf = Buffer.from(JSON.stringify(filters.filter((filter) => (filter.question_id != -1))),
                "utf8")
        const body = {
            form_type: formType,
            answer_filters: buf.toString("base64"),
            name_substr: name_substr
        }
        getFilteredTableData(body, navigate).then((data) => {
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
                                    answer_block_id: questionResponse.value.answer_block_id,
                                    // @ts-ignore
                                    default_filter: questionResponse.value.formatting_settings.default_filter
                                })
                            }
                        })
                    })
                    setQuestions(newQuestions)

                    setNewQuestion(newQuestions[0])
                    console.log("THERETHERE")
                    add(newQuestions.filter((q) => {
                        console.log(q)
                        return q.default_filter}), newQuestions)

                })
                .catch((error) => {
                    console.log("Error while accessing to the /form: ", error)
                })
            // })
        handleSubmitFilter()
        getObjectsList(formType, navigate).then((response) => {
            setNames(response)
        })
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
            <Autocomplete
                    sx={{ width: 450, margin: 5 }}
                    options={names}
                    disableCloseOnSelect
                    getOptionLabel={(option) => (typeof option === 'string' ?
                        option : option.name)}
                    value={searchValue}
                    inputValue={searchInputValue}
                    onChange={handleSearchChange}
                    onInputChange={handleSearchInputChange}
                    isOptionEqualToValue={(option, value) => (option.name.trim() === value.name.trim())}
                    freeSolo
                    renderInput={(params) => (
                        <TextField
                            {...params}
                            size="small"
                            label={t('name_search')}
                            inputProps={{
                                ...params.inputProps,
                                autoComplete: 'new-password',
                            }}
                            >
                        </TextField>
                    )}
                />
            <Card>
                <Stack direction="row" spacing={1} padding={2} alignItems="center">
                    <Typography variant="caption">{t("add_filter")}</Typography>
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
                    setAddDialogOpen(true)
                }}>
                    {formType === 'LEADER' ? t('add_leader') : t('add_project')}
                </Button>
            </Box>
            <h2>{t('table')}</h2>
            <Card>
                <MainTable {...JSON.parse(JSON.stringify(tableData))}/>
            </Card>
            <Dialog open={addDialogOpen}>
                <AddObjectPopup onCancel={() => {
                    setAddDialogOpen(false)
                }} onSubmit={(name: string) => {
                    setAddDialogOpen(false)
                    makeNewObject(navigate, formType, name).then((id) => {
                        const link = '/' + formType.toLowerCase() + '/' + id
                        navigate(link, { replace: true })
                    })
                }} formType={formType}/>
            </Dialog>
        </Stack>
    )
}

export default FilterTablePage;