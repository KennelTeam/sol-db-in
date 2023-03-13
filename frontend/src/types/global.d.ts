
enum UserType {
    Admin,
    Editor,
    Intern,
    Guest,
    None
}

enum AccessRights {
    CAN_NOTHING,
    CAN_SEE,
    CAN_EDIT
}

const MENU_WIDTH = 200

export { UserType, AccessRights, MENU_WIDTH }