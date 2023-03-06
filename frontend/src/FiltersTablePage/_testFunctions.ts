import { AnswerType } from "../types/global"
import { AnswerVariant } from "./TypedFilters"
import axios from 'axios'

// TESTING FUNCTIONS //////////////////////////////////////
// later these functions will work with server API by passing requests

export function _getFilterableQuestionsList() : { id: number, text: string, type: AnswerType }[] {
    return [
        {id: 1, text: "Name", type: AnswerType.Text},
        {id: 2, text: "Second name", type: AnswerType.Text},
        {id: 3, text: "Age", type: AnswerType.Number},
        {id: 5, text: "Is married", type: AnswerType.Checkbox},
        {id: 6, text: "Favourite food", type: AnswerType.List},
        {id: 7, text: "Intervier", type: AnswerType.User},
        {id: 8, text: "Recomendation", type: AnswerType.Leader},
        {id: 10, text: "Main project", type: AnswerType.Project},
        {id: 12, text: "Start working on project", type: AnswerType.Date},
    ]
}

export function _getAnswersList(questionId: number) : AnswerVariant[] {
    if (questionId === 6) {
        return [
            {id: 1, name: "banana"},
            {id: 2, name: "carbonara"},
            {id: 3, name: "smoozi"},
            {id: 5, name: "porrige"},
            {id: 7, name: "kinder surprise"},
            {id: 8, name: "watermelon"}]
    } else {
        return [{id: -1, name: "WRONG QUESTION ID PASSED"}]
    }
}

export function _getUsersList() : AnswerVariant[] {
    return [
        {id: 2, name: "Andrey"},
        {id: 3, name: "Maria"},
        {id: 5, name: "Nikolay"},
        {id: 6, name: "Nikita"},
        {id: 10, name: "Lev"}
    ]
}

export function _getLeadersList() : AnswerVariant[] {
    return [
        {id: 1, name: "Elon Musk"},
        {id: 3, name: "Tim Cook"},
        {id: 4, name: "Rayan Gosling"},
        {id: 8, name: "Geyb Neuell"},
        {id: 10, name: "Notch"},
        {id: 11, name: "Sergey Brin"},
        {id: 12, name: "Bill Gates"},
        {id: 13, name: "Arkadiy Volosh"}
    ]
}

export function _getProjectsList() : AnswerVariant[] {
    return [
        {id: 1, name: "Tesla"},
        {id: 3, name: "Space X"},
        {id: 4, name: "PayPal"},
        {id: 8, name: "Google"},
        {id: 10, name: "Microsoft"},
        {id: 11, name: "Sergey Brin"},
        {id: 12, name: "Bill Gates"},
        {id: 13, name: "Apple"},
        {id: 14, name: "Mail.ru"}
    ]
}

export function _getLocationsList() : AnswerVariant[] {
    return [
        {id: 1, name: "Los-Angeles"},
        {id: 3, name: "Las-Vegas"},
        {id: 4, name: "Chelyabinsk"},
        {id: 8, name: "Himki"},
        {id: 10, name: "Tokyo"},
        {id: 11, name: "Berlin"},
    ]
}

export interface ColumnGroup {
    name: string,
    columns: string[]
}

export interface ColumnResponse {
    column_name: "string",
    values: {
        answers: {
            id: number,
            value: number | string | boolean,
            type: string
        }[]
    }[]
}

export interface Row {
    id: number,
    name: string,
    link: string
    columns: {
        link?: string,
        data: string
    }[][]
}

export function getColumnsFromResponse(data: ColumnResponse[]) : ColumnGroup[] {

    return data.map((column) => ({ name: column.column_name, columns: [column.column_name] }))
}

// export function getRowsFromResponse(data: ColumnResponse[], link: string) : Row[] {
//     const rows : Row[] = []
//     for (let i = 0; i < data[0].values.length; i++) {
//         rows.push(data.map((column) => ({
//             id: column.answers[0].id,

//         })))
//     }
// }

export function _getColumns() : { name: string, columns: string[] }[] {
    return [
        {
            name: "General",
            columns: ["id", "Name", "City", "Category", "Projects"]
        },
        {
            name: "Interview",
            columns: ["Interviewer", "Date", "Variant", "Comment"]
        },
        {
            name: "Recomendations",
            columns: ["Incoming", "Ountcoming"]
        },
        {
            name: "Status",
            columns: ["Check", "Filter"]
        }
    ]
}

export function _getRows() : Row[] {
    let list = [
        {
            id: 2,
            name: "Pavel Durov",
            link: "/leader/2",
            columns: [
                [{ data: "Los Angeles" }], 
                [{ data: "clever man" }],
                [
                    {
                        link: "/project/5",
                        data: "VKontakte"
                    },
                    {
                        link: "/project/4",
                        data: "Telegram"
                    },
                    {
                        link: "/project/228",
                        data: "Roscomnadzor"
                    }
                ],
                [{data: "Nikita"}],
                [{data: "30.02.2023"}],
                [{data: "in VK call"}],
                [{data: "Very klassny man and very beautiful"}],
                [{data: "7"}],
                [{data: "100500"}],
                [{data: "*yes*"}],
                [{data: "-"}]
            ]
        },
        {
            id: 4,
            name: "Elon Musk",
            link: "/leader/4",
            columns: [
                [{data: "Voronezh"}],
                [{data: "cool man"}],
                [
                    {
                        link: "/project/7",
                        data: "PayPal"
                    },
                    {
                        link: "/project/9",
                        data: "Tesla"
                    },
                    {
                        link: "/project/10",
                        data: "SpaceX"
                    },
                    {
                        link: "/project/11",
                        data: "SocBiz"
                    }
                ],
                [{data: "Nikolay"}],
                [{data: "30.02.2022"}],
                [{data: "in WhatsApp call"}],
                [{data: "Very cool and fun dude"}],
                [{data: "1"}],
                [{data: "99"}],
                [{data: "-"}],
                [{data: "*yes*"}]
            ]
        },
        {
            id: 7,
            name: "Mark Zuckerberg",
            link: "/leader/7",
            columns: [
                [{data: "Syktyvkar"}],
                [{data: "owner of Meta"}],
                [
                    {
                        link: "/project/12",
                        data: "Facebook"
                    },
                    {
                        link: "/project/55",
                        data: "Instagram"
                    },
                    {
                        link: "/project/23",
                        data: "WhatsApp"
                    }
                ],
                [{data: "Lev"}],
                [{data: "29.02.2023"}],
                [{data: "by telephone"}],
                [{data: "cool dude with beautiful smile"}],
                [{data: "77"}],
                [{data: "22"}],
                [{data: "*yes*"}],
                [{data: "*yes*"}]
            ]
        }
    ]
    for (let i = 0; i < 5; i++) {
        list = list.concat(list)
    }
    return list
}
