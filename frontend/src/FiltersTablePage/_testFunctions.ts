import { AnswerType } from "../types/global"

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

export function _getAnswersList(questionId: number) : string[] {
    if (questionId === 6) {
        return ["banana", "carbonara", "smoozi", "porrige", "kinder surprise", "watermelon"]
    } else {
        return ["WRONG QUESTION ID PASSED"]
    }
}

export function _getUsersList() : string[] {
    return ["Andrey", "Maria", "Nikolay", "Nikita", "Lev"]
}

export function _getLeadersList() : string[] {
    return ["Elon Musk", "Tim Cook", "Rayan Gosling", "Geyb Neuell", "Notch", "Sergey Brin", "Bill Gates", "Arkadiy Volosh"]
}

export function _getProjectsList() : string[] {
    return ["Tesla", "Space X", "PayPal", "Google", "Microsoft", "Apple", "Mail.ru"]
}

export function _getLocationsList() : string[] {
    return ["Los-Angeles", "Las-Vegas", "Chelyabinsk", "Himki", "Tokyo", "Berlin"]
}

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

export interface Row {
    id: number,
    name: string,
    link: string
    columns: {
        link?: string,
        data: string
    }[][]
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
