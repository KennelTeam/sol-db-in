
enum UserType {
    Admin,
    Editor,
    Junior,
    Guest
}

interface UserTypeProps { // props interface used by NavigationMenu for sending user role
    user: UserType
}

export {UserType, UserTypeProps}