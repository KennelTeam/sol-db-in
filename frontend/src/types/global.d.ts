
enum UserType {
    Admin,
    Editor,
    Intern,
    Guest,
    None
}

interface UserTypeProps { // props interface used by NavigationMenu for sending user role
    user: UserType
    width: number
}

export {UserType, UserTypeProps}