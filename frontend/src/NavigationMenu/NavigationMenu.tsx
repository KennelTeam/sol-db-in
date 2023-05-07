import { List, ListItem, ListItemButton, ListItemText, Box, Drawer, Collapse } from '@mui/material'
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import { MENU_WIDTH, UserType } from '../types/global'
import { useTranslation } from 'react-i18next'
import { TFunction } from 'i18next'
import React from 'react';
import { Link } from 'react-router-dom';
import { useLocation } from 'react-router-dom';

interface UserTypeProps { // props interface used by NavigationMenu for sending user role
    user: UserType
}

const MenuButton = (text: string, path: string, t : TFunction, padding=2) : JSX.Element => (
    <ListItem component={Link} to={path} target={"_blanc"}
        style={{ color: "inherit", textDecoration: "none" }}
        disablePadding
        >
        <ListItemButton sx={{ pl: padding}} selected={useLocation().pathname.startsWith(path)}>
                <ListItemText primary={t(text)}/>
        </ListItemButton>
    </ListItem>
)

function DropDownList(text: string, itemsNames: string[], itemsPaths: string[]) : JSX.Element {
    const { t } = useTranslation('translation', { keyPrefix: "menu" })

    const [open, setOpen] = React.useState(false)
    let handleClick = () => {
        setOpen(!open)
    }

    let items = []
    for (let i = 0; i < itemsNames.length; i++) {
        items.push(MenuButton(itemsNames[i], itemsPaths[i], t, 4))
    }
    return (
        <div>
            <ListItem disablePadding>
                <ListItemButton onClick={handleClick}>
                    <ListItemText primary={t(text)}/>
                    {open ? <ExpandLess /> : <ExpandMore />}
                </ListItemButton>
            </ListItem>
            <Collapse in={open} unmountOnExit>
                <List disablePadding>
                    {items}
                </List>
            </Collapse>
        </div>
    )
}

function ChoiceOptionsList(user: UserType) : JSX.Element[] {
    // now you can test menu translation by going on /login page and press "Submit" button
    const { t } = useTranslation('translation', { keyPrefix: "menu" })

    const projects: JSX.Element = MenuButton('projects', "/projects", t)
    const leaders: JSX.Element = MenuButton("leaders", "/leaders", t)
    const statistics: JSX.Element = DropDownList(
        "statistics",
        ["fullness-stats", /*"distribution-stats"*/],
        ["/statistics/fullness", /*"/statistics/distribution"*/],
    )
    const export_menu: JSX.Element = DropDownList(
        "export",
        ["main-download"],
        ["/api/export/forms"]
    )
    const settings: JSX.Element = MenuButton("settings", "/settings", t)
    const users: JSX.Element = MenuButton("users", "/users", t)
    const catalog: JSX.Element = DropDownList("catalog", ["tags", "questionnaire", "options"],
                                                        ["/tags", "/questionnaire", "/options"])

    let options_list : JSX.Element[]
    switch (user) { // this switch choices pages that will be shown to user by his role
        case UserType.Admin:
            options_list = [leaders, projects, users, statistics, export_menu/*, catalog, settings*/]
            break
        case UserType.Editor:
            options_list = [leaders, projects, statistics/*, catalog, settings*/]
            break
        case UserType.Intern:
            options_list = [leaders, projects, /*statistics, catalog*/]
            break
        case UserType.Guest:
            options_list = [leaders, projects, /*statistics*/]
            break
        default:
            options_list = []
            throw new Error('Invalid UserType value')
    }

    return options_list
}

export default function NavigationMenu(props: UserTypeProps) : JSX.Element {
    let menu: JSX.Element[] = ChoiceOptionsList(props.user)

    return (
        <Box
            position="fixed">
            <Drawer
                variant="permanent"
                open={true}
                sx={{'& .MuiDrawer-paper': { boxSizing: 'border-box', width: MENU_WIDTH } }}
                >
                <List>
                    {menu}
                </List>
            </Drawer>
        </Box>
    )
}
