
const SERVER_ADDRESS = window.location.origin + '/api'

enum UserType {
    Admin,
    Editor,
    Intern,
    Guest,
    None
}

export enum AccessRights {
    CAN_SEE = "CAN_SEE",
    CAN_EDIT = "CAN_EDIT",
    CAN_NOTHING = "CAN_NOTHING"
}

enum AnswerType {
    Number,
    Text,
    Checkbox,
    List,
    User,
    Leader,
    Project,
    Date,
    Location
}

const MENU_WIDTH = 200

export { UserType, MENU_WIDTH, AnswerType, SERVER_ADDRESS }