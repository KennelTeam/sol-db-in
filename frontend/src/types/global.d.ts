
enum UserType {
    Admin,
    Editor,
    Intern,
    Guest,
    None
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

export { UserType, MENU_WIDTH, AnswerType }