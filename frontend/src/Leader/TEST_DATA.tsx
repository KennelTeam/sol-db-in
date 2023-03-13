import { ResponseDataInterface } from "../Response/ResponseData";
import { SimpleQuestionType } from "../Response/SimpleQuestions/SimpleQuestion";
import { TableType } from "../Response/Table/BaseTable";

const TEST_DATA: ResponseDataInterface = {
    title: "Super mega anketa",
    blocks: [
        {
            title: "General person info",
            items: [
                {
                    questionType: SimpleQuestionType.TEXT,
                    questionData: {
                        initialValue: "Nikolay",
                        label: "Name",
                    },
                    inputInfo: {
                        title: "Name",
                        description: "The name of an interviewee"
                    },
                },
                {
                    questionType: SimpleQuestionType.NUMBER,
                    questionData: {
                        initialValue: 19,
                        label: "Age",
                    },
                    inputInfo: {
                        title: "Age",
                        description: "The age of an interviewee that would show whether this dude is a dude or a dude"
                    }
                },
            ]
        },
        {
            title: "Main project info",
            items: [
                {
                    questionType: SimpleQuestionType.SELECT,
                    questionData: {
                        initialValue: 1,
                        label: "Select main project",
                        dataToChooseFrom: [
                            {
                                id: 1,
                                name: "School project"
                            },
                            {
                                id: 2,
                                name: "Personal project"
                            },
                            {
                                id: 3,
                                name: "Work project"
                            },
                        ]
                    },
                    inputInfo: {
                        title: "Main project",
                        description: "The main project of an interviewee"
                    }
                },
                {
                    questionType: SimpleQuestionType.TEXT,
                    questionData: {
                        initialValue: "Because I fucking love it",
                        label: "Why this project?",
                    },
                    inputInfo: {
                        title: "x",
                        description: "What motivataes you to work on this project?"
                    }
                },
                {
                    questionType: TableType.FIXED_TABLE,
                    questionData: {
                        label: "How good do participants interact with each other",
                        inputInfoOnLeft: [
                            {
                                title: "Lukashenko",
                                description: null,
                            },
                            {
                                title: "Nexta",
                                description: null,
                            }
                        ],
                        inputInfoOnTop: [
                            {
                                title: "Mike",
                                description: null,
                            },
                            {
                                title: "Nick",
                                description: null
                            },
                        ],
                        questionType: SimpleQuestionType.NUMBER,
                        questionData: [
                            [{label: null, initialValue: 10}, {label: null, initialValue: 20}],
                            [{label: null, initialValue: 30}, {label: null, initialValue: 40}],
                        ]
                    },
                    inputInfo: {
                        title: "How good do participants interact with each other",
                        description: "How good do participants interact with each other"
                    },
                },
                {
                    questionType: SimpleQuestionType.CHECKBOX,
                    questionData: {
                        questions: [
                            {
                                initialValue: true,
                                label: "Do you like this project?",
                            },
                            {
                                initialValue: false,
                                label: "Does your mom like this project?",
                            },
                            {
                                initialValue: false,
                                label: "Does your dad like this project?",
                            },
                            {
                                initialValue: false,
                                label: "Does your dog like this project?",
                            },
                            {
                                initialValue: true,
                                label: "Does your cat like this project?",
                            },
                            {
                                initialValue: true,
                                label: "Does your grandma like this project?",
                            }
                        ]
                    },
                    inputInfo: {
                        title: "Do you like this project?",
                        description: "Do you like this project?"
                    }
                },
                {
                    questionType: TableType.DYNAMIC_TABLE,
                    questionData: {
                        inputInfos: [
                            {
                                title: "Contributor name",
                                description: null,
                            },
                            {
                                title: "Contribution impact",
                                description: null,
                            },
                            {
                                title: "Contribution type",
                                description: "Does this contribution affect the project in any way?",
                            },
                            {
                                title: "Contribution description",
                                description: "What does this contribution do?",
                            },
                            {
                                title: "Contribution time",
                                description: null,
                            },
                            {
                                title: "Contribution cost",
                                description: null,
                            },
                        ],
                        questions: [
                            [
                                {
                                    questionType: SimpleQuestionType.TEXT,
                                    questionData: {
                                        initialValue: "Mike",
                                        label: null,
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.NUMBER,
                                    questionData: {
                                        initialValue: 10,
                                        label: "Impact",
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.SELECT,
                                    questionData: {
                                        initialValue: 1,
                                        label: "Type",
                                        dataToChooseFrom: [
                                            {
                                                id: 1,
                                                name: "Code"
                                            },
                                            {
                                                id: 2,
                                                name: "Design"
                                            },
                                            {
                                                id: 3,
                                                name: "Marketing"
                                            },
                                        ],
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.TEXT,
                                    questionData: {
                                        initialValue: "I made a logo",
                                        label: "Description",
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.NUMBER,
                                    questionData: {
                                        initialValue: 10,
                                        label: "Time",
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.NUMBER,
                                    questionData: {
                                        initialValue: 25,
                                        label: "Cost",
                                    },
                                },
                            ],
                            [
                                {
                                    questionType: SimpleQuestionType.TEXT,
                                    questionData: {
                                        initialValue: "Nick",
                                        label: null,
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.NUMBER,
                                    questionData: {
                                        initialValue: 10,
                                        label: "Impact",
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.SELECT,
                                    questionData: {
                                        initialValue: 1,
                                        label: "Type",
                                        dataToChooseFrom: [
                                            {
                                                id: 1,
                                                name: "Code"
                                            },
                                            {
                                                id: 2,
                                                name: "Design"
                                            },
                                            {
                                                id: 3,
                                                name: "Marketing"
                                            },
                                        ],
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.TEXT,
                                    questionData: {
                                        initialValue: "I made a logo",
                                        label: "Description",
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.NUMBER,
                                    questionData: {
                                        initialValue: 10,
                                        label: "Time",
                                    },
                                },
                                {
                                    questionType: SimpleQuestionType.NUMBER,
                                    questionData: {
                                        initialValue: 25,
                                        label: "Cost",
                                    },
                                },
                            ]
                        ],
                    },
                    inputInfo: {
                        title: "External contributions to the project",
                        description: "External contributions to the project"
                    },
                }
            ]
        },
    ]
};

export default TEST_DATA;