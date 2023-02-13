import { AnswerType } from "../types/global.d"

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

export interface leaderData {
    id: number,
    name: string,
    city: string,
    category: string,
    projects: {
        id: number,
        name: string
    }[],
    interviewer: string,
    date: string,
    interviewVariant: string,
    interviewComment: string,
    recomendationsOut: number,
    recomendationsIn: number,
    isCheck: boolean,
    isFinish: boolean
}

export function _getLeadersData() : leaderData[] {
    const two = [
        {
            id: 2,
            name: "Pavel Durov",
            city: "Los Angeles",
            category: "clever man",
            projects: [
                {
                    id: 5,
                    name: "VKontakte"
                },
                {
                    id: 4,
                    name: "Telegram"
                },
                {
                    id: 228,
                    name: "Roscomnadzor"
                }
            ],
            interviewer: "Nikita",
            date: "30.02.2023",
            interviewVariant: "in VK call",
            interviewComment: "Very klassny man and very beautiful",
            recomendationsOut: 7,
            recomendationsIn: 100500,
            isCheck: true,
            isFinish: false
        },
        {
            id: 4,
            name: "Elon Musk",
            city: "Voronezh",
            category: "cool man",
            projects: [
                {
                    id: 7,
                    name: "PayPal"
                },
                {
                    id: 9,
                    name: "Tesla"
                },
                {
                    id: 10,
                    name: "SpaceX"
                },
                {
                    id: 11,
                    name: "SocBiz"
                }
            ],
            interviewer: "Nikolay",
            date: "30.02.2022",
            interviewVariant: "in WhatsApp call",
            interviewComment: "Very cool and fun dude",
            recomendationsOut: 1,
            recomendationsIn: 99,
            isCheck: false,
            isFinish: true
        }
    ]
    return two.concat(two).concat(two).concat(two)
}
