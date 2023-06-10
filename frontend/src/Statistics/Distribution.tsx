import { Box, InputLabel, MenuItem, Select, Table, TableCell, TableContainer, TableHead, TableRow, TableBody } from "@mui/material";
import axios from "axios";
import React, {useState} from "react";
import { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { SERVER_ADDRESS } from "../types/global";
import {getRequest} from "../Response/APIRequests";
import {Link, useNavigate} from "react-router-dom";
import {APIForm, APIFormSimple, APIFormType} from "../Response/APIObjects";


function DistributionStatistics() {
    const [t] = useTranslation('translation', { keyPrefix: "statistics" });
    const [selectedQuestion, setSelectedQuestion] = useState({text: "Select form type, please", id: -1})
    const [options, setOptions] = useState([] as Array<{text: string, id: number}>)
    const [formType, setFormType] = useState("NONE")
    const navigate = useNavigate()
    const [statistics, setStatistics] = useState({} as {[id: string]: {[d: string]: Array<APIFormSimple>}})
    const [dataToShow, setDataToShow] = useState([] as Array<APIFormSimple>)
    async function load_options(current_form_type: string) {
        let data = await getRequest("questions_lightweight", {form_type: current_form_type}, navigate) as unknown as {data:{questions: Object}}
        console.log(data)
        let questions = data.data.questions as Array<{text: string, id: number}>
        setOptions(questions)
    }

    const changeFormType = (new_type: string) => {
        load_options(new_type).then(r => console.log("Succeed"))
        setFormType(new_type)
    }

    async function load_statistics(questionId: number) {
        let statistics = (await getRequest("statistics", {question_id: questionId}, navigate)).data as unknown as {[id: string]: {[d: string]: Array<APIFormSimple>}}
        setStatistics(statistics)
    }

    const onQuestionSelected = (question_id: number, question_text: string) => {
        load_statistics(question_id).then(r => {
            console.log("Statistics successfully loaded")
            console.log(statistics)
        })
        setSelectedQuestion({text: question_text, id: question_id})
    }

    useEffect(() => {
    }, [options, selectedQuestion]);

    const prepareHead = () => {
        let data = []
        for (const key in statistics) {
            data.push(key)
        }
        return data.map((item) => <TableCell>{item}</TableCell>)
    }

    const showItems = (items: Array<APIFormSimple>) => {
        setDataToShow(items)
    }

    const prepareTable = () => {
        console.log(statistics)
        let rows = []
        for (const key in statistics) {
            for (const key2 in statistics[key]) {
                rows.push({
                    values: [] as Array<Array<APIFormSimple>>,
                    title: key2
                })
            }
            break
        }
        for (const key in statistics) {
            let i = 0
            for (const key2 in statistics[key]) {
                rows[i].values.push(statistics[key][key2])
                i += 1
            }
        }
        return rows.map((row) =>
            <TableRow>
                <TableCell>{row.title}</TableCell>
                {
                    row.values.map((cell) =>
                        <TableCell onClick={() => showItems(cell)}>{cell.length}</TableCell>
                    )
                }
            </TableRow>
        )
    }

    return <Box>
        <h1>{t("stats")}</h1>
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'row',
                justifyContent: 'space-around',
                alignItems: 'center',
            }}
            style={{minWidth: "70%"}}
        >
            <Box style={{minWidth: "50%"}}>
                <h3>{t('form-type-selector')}</h3>
                <Select
                    style={{minWidth: "30%"}}
                    label={t('form-type-selector')}
                    value={formType}
                    onChange={(event) => { changeFormType(event.target.value) }}
                >
                    <MenuItem value="NONE">Select</MenuItem>
                    <MenuItem value="LEADER">{t('form-type-leader')}</MenuItem>
                    <MenuItem value="PROJECT">{t('form-type-project')}</MenuItem>
                </Select>
            </Box>

            <Box style={{minWidth: "50%"}}>
                <h3>{t('question-selector')}</h3>
                <Select
                    label={t('question-selector')}
                    value={selectedQuestion.id}
                    onChange={(event) => { console.log(event.target.value)
                        onQuestionSelected(+event.target.value, "test") }}
                    style={{minWidth: "50%"}}
                >
                    {
                        options.map((option) =>
                            <MenuItem value={option.id}>{option.text}</MenuItem>)
                    }
                </Select>
            </Box>
        </Box>
        <div>
            {dataToShow.length > 0 ? <h3>Selected cell elements:</h3> : <div></div>}
            {dataToShow.map((form: APIFormSimple) => <div>
                <Link to={(form.form_type === 'LEADER' ? '/leader/' : '/project/')
                    + form.id} target={"_blanc"}>{form.name}</Link>
            </div>)}
        </div>
        <TableContainer>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell></TableCell>
                        {
                            prepareHead()
                        }
                    </TableRow>
                </TableHead>
                <TableBody>
                    {
                        prepareTable()
                    }
                </TableBody>
            </Table>
        </TableContainer>
    </Box>
}

export default DistributionStatistics;