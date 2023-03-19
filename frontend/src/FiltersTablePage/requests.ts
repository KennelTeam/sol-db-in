import { AnswerVariant, AnswerFilter } from "./TypedFilters"
import { SERVER_ADDRESS } from "../types/global"
import { FormResponse } from './FilterTablePage'
import { FormsResponse, ColumnGroup, Row } from './_testFunctions'
import i18next, { i18n } from "i18next"
import axios from "axios"

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

export interface TableData {
    column_groups: ColumnGroup[]
    rows: Row[]
}

export function getLanguage() {
    return i18next.language.split('-', 1)[0]
}

export async function getUsersList() : Promise<AnswerVariant[]> {
    return await axios.get(SERVER_ADDRESS + '/users', { withCredentials: true })
        .then((response) => {
            console.log("Users response:", response.status, response.data)
            return <AnswerVariant[]>response.data
        })
        .catch((error) => {
            console.log(error)
            return []
        })
}

export async function getAnswersList(questionId: number) : Promise<AnswerVariant[]> {
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
            return []
        })
}

export async function getObjectsList(type: 'LEADER' | 'PROJECT') : Promise<AnswerVariant[]> {
    return await axios.get(SERVER_ADDRESS + '/forms',
        { withCredentials: true, params: { form_type: type, answer_filters: [] } })
        .then((response) => {
            console.log(type, " response:", response.status, response.data)
            const data = <FormsResponse>response.data
            return data.table[0].values.map((cell) => ({
                id: cell.answers[0].id,
                name: <string>cell.answers[0].value
            }))
        })
        .catch((error) => {
            console.log(error)
            return []
        })
}

export async function getToponymsList() : Promise<AnswerVariant[]> {
    return await axios.get(SERVER_ADDRESS + '/all_toponyms',
        { withCredentials: true})
        .then((response) => {
            console.log("Answer options response:", response.status, response.data)
            // return <AnswerVariant[]>response.data
            return []
        })
        .catch((error) => {
            console.log(error)
            return []
        })
}

export async function getFilteredTableData(data: FiltersRequestData) : Promise<TableData> {

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
                column_groups: responseData.table.map((column) => ({
                    name: column.column_name,
                    columns: [column.column_name]
                })),
                rows: []
            }
            if (responseData.table.length === 0) {
                console.log("Empty table")
                return tableData
            }
            for (let i = 0; i < responseData.table[0].values.length; i++) {
                tableData.rows.push({
                    id: responseData.table[0].values[0].answers[0].id,
                    columns: responseData.table.map((column) => (
                        column.values[i].answers.map((ans) => ({
                            data: stringify(ans.value),
                            link: ans.type === 'RELATION' ?
                                makeLink(ans.id, ans.relation_settings.relation_type) : undefined
                        }))
                    ))
                })
            }
            return tableData
        })
        .catch((error) => {
            console.log("Error while requesting /forms:", error)
            return {
                column_groups: [],
                rows: []
            }
        })
}

export async function makeNewObject(formType: 'LEADER' | 'PROJECT') {
    return await axios.post(SERVER_ADDRESS + '/forms', {
        state: 'PLANNED',
        name: "insert name here",
        form_type: formType,
        answers: []
    }, { withCredentials: true })
    .then((response) => (response.data))
    .catch((error) => {
        console.log("Error while requesting /forms by POST request:", error)
        return {
            column_groups: [],
            rows: []
        }
    })
}