import { AnswerVariant, AnswerFilter } from "./TypedFilters"
import { SERVER_ADDRESS } from "../types/global"
import { FormsResponse, ColumnGroup, Row } from './_testFunctions'
import i18next, { i18n } from "i18next"
import axios, { AxiosError } from "axios"
import { NavigateFunction, useNavigate } from "react-router-dom"
import { TableData, HeadColumn } from "./MainTable"

interface TranslatedText {
    [language: string]: string
}

interface AnswerBlockResponse {
    options: {
        id: number,
        name: string
    }[]
}

interface FiltersRequestData {
    form_type: 'LEADER' | 'PROJECT',
    answer_filters: string
}

export function getLanguage() {
    return i18next.language.split('-', 1)[0]
}

export function handleError(navigate: NavigateFunction, error: AxiosError) {
    if (error.response)
        navigate('/error/' + error.response.status, { replace: true })
    else {
        navigate('/error/Network', { replace: true })
    }
}

export async function getUsersList(navigate: NavigateFunction) : Promise<AnswerVariant[]> {
    return await axios.get(SERVER_ADDRESS + '/users', { withCredentials: true })
        .then((response) => {
            console.log("Users response:", response.status, response.data)
            return <AnswerVariant[]>response.data
        })
        .catch((error) => {
            console.log(error)
            const navigate = useNavigate()
            handleError(navigate, error)
            return []
        })
}

export async function getAnswersList(questionId: number, navigate: NavigateFunction) : Promise<AnswerVariant[]> {
    return await axios.get(SERVER_ADDRESS + '/answer_block',
        { withCredentials: true, params: { id: questionId } })
        .then((response) => {
            console.log("Answer block response:", response.status, response.data)
            return (<AnswerBlockResponse>response.data).options.map((option) => ({
                id: option.id,
                name: option.name
            }))
        })
        .catch((error) => {
            console.log(error)
            handleError(navigate, error)
            return []
        })
}

export async function getObjectsList(type: 'LEADER' | 'PROJECT', navigate: NavigateFunction) : Promise<AnswerVariant[]> {
    return await axios.get(SERVER_ADDRESS + '/forms_lightweight',
        { withCredentials: true, params: { form_type: type } })
        .then((response) => {
            console.log(type, " response:", response.status, response.data)
            return response.data as AnswerVariant[];
        })
        .catch((error) => {
            console.log("EEERRORRRORRR!")
            console.log(error)
            handleError(navigate, error)
            return []
        })
}

export async function getToponymsList(navigate: NavigateFunction) : Promise<AnswerVariant[]> {
    return await axios.get(SERVER_ADDRESS + '/all_toponyms',
        { withCredentials: true})
        .then((response) => {
            console.log("Answer options response:", response.status, response.data)
            // return <AnswerVariant[]>response.data
            return []
        })
        .catch((error) => {
            console.log(error)
            handleError(navigate, error)
            return []
        })
}

export async function getFilteredTableData(data: FiltersRequestData,
                    navigate: NavigateFunction) : Promise<TableData> {

    function stringify(value: string | number | boolean) : string {
        switch (typeof value) {
            case 'string' :
                return value
            case 'number' :
                return String(value)
            case 'boolean' :
                return value ? '*yes*' : '-'
        }
    }

    function makeLink(id: number, relType: 'LEADER' | 'PROJECT') {
        return '/' + relType.toLowerCase() + '/' + id
    }

    console.log("Requesting /forms with data: ", data)
    return await axios.get(SERVER_ADDRESS + '/forms', { params: data, withCredentials: true })
        .then((response) => {
            console.log("Forms request with data:", data, "returns", response.status, response.data)
            const responseData = <FormsResponse>response.data
            const tableData : TableData = {
                headColumns: responseData.table.map((column, idx) => ({
                    name: column.column_name,
                    numeric: column.values.length > 0 && column.values[0].answers.length > 0
                        && column.values[0].answers[0].type === 'NUMBER',
                    id: idx
                })),
                rows: []
            }
            if (responseData.table.length === 0) {
                console.log("Empty table")
                return tableData
            }
            for (let i = 0; i < responseData.table[0].values.length; i++) {
                tableData.rows.push({
                    id: responseData.table[0].values[i].answers[0].ref_id,
                    columns: responseData.table.map((column) => (
                        column.values[i].answers.map((ans) => ({
                            data: stringify(ans.value),
                            link: ans.type === 'RELATION' ?
                                makeLink(ans.ref_id, ans.relation_type) : undefined
                        }))
                    ))
                })
            }
            return tableData
        })
        .catch((error) => {
            console.log("Error while requesting /forms:", error)
            handleError(navigate, error)
            return {
                headColumns: [],
                rows: []
            }
        })
}

export async function makeNewObject(navigate: NavigateFunction,
                formType: 'LEADER' | 'PROJECT', name?: string) : Promise<number> {
    return await axios.post(SERVER_ADDRESS + '/forms', {
        state: 'PLANNED',
        name: name ? name : "insert name here",
        form_type: formType,
        answers: []
    }, { withCredentials: true })
    .then((response) => (response.data as number))
    .catch((error) => {
        console.log("Error while requesting /forms by POST request:", error)
        handleError(navigate, error)
        return -1
    })
}