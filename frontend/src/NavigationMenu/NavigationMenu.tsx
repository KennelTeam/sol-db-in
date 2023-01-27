import { List, ListItem, ListItemButton, ListItemText, Box, Drawer, Collapse } from '@mui/material'
import { ExpandLess, ExpandMore } from '@mui/icons-material';
import { UserType, UserTypeProps } from '../types/global.d'
import { useTranslation } from 'react-i18next'
import { TFunction } from 'i18next'
import React, { useEffect } from 'react'

const menu_button = (text: string, path: string, t : TFunction, padding=2) : JSX.Element => (
    <ListItem disablePadding>
        <ListItemButton href={path} sx={{ pl: padding}}>
            <ListItemText primary={t(text)} />
        </ListItemButton>
    </ListItem>
)

function make_catalog_element(openCatalog: boolean, 
        setOpen: React.Dispatch<React.SetStateAction<boolean>>, t : TFunction) : JSX.Element {

    // PROBLEM with this architecture: after clicking on any button and going to another page Catalog's menu is closing
    let handleClick = () => {
        setOpen(!openCatalog)
    }

    const tags : JSX.Element = menu_button("tags", "/tags", t, 4)
    const questionary : JSX.Element = menu_button("questionary", "/", t, 4)
    const answers : JSX.Element = menu_button("answers", "/", t, 4)
    return (
        <div>
            <ListItem disablePadding>
                <ListItemButton onClick={handleClick}>
                    <ListItemText primary={t("catalog")}/>
                    {openCatalog ? <ExpandLess /> : <ExpandMore />}
                </ListItemButton>
            </ListItem>
            <Collapse in={openCatalog} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                    {[tags, questionary, answers]}
                </List>
            </Collapse>
        </div>
    )
}

function choice_options_list(user: UserType, openCatalog: boolean, 
        setOpen: React.Dispatch<React.SetStateAction<boolean>>, t : TFunction) : JSX.Element[] {
    // now you can test menu translation by going on /login page and press "Submit" button

    const projects: JSX.Element = menu_button('projects', "/projects", t)
    const leaders: JSX.Element = menu_button("leaders", "/leaders", t)
    const statistics: JSX.Element = menu_button("statistics", "/statistics", t)
    const settings: JSX.Element = menu_button("settings", "/settings", t)
    const users: JSX.Element = menu_button("users", "/users", t)
    const catalog: JSX.Element = make_catalog_element(openCatalog, setOpen, t)

    let options_list : JSX.Element[]
    switch (user) { // this switch choices pages that will be shown to user by his role
        case UserType.Admin:
            options_list = [leaders, projects, statistics, catalog, settings, users]
            break
        case UserType.Editor:
            options_list = [leaders, projects, statistics, catalog, settings]
            break
        case UserType.Junior:
            options_list = [leaders, projects, statistics, catalog]
            break
        case UserType.Guest:
            options_list = [leaders, projects, statistics]
            break
        default:
            options_list = []
            throw new Error('Invalid UserType value')
    }

    return options_list
}

export default function NavigationMenu(props: UserTypeProps) : JSX.Element {
    const drawerWidth: number = 200
    const { t } = useTranslation('translation', { keyPrefix: "translation.page_names" })
    const [open, setOpen] = React.useState(false)
    let menu: JSX.Element[] = choice_options_list(props.user, open, setOpen, t)

    return (
        <Box
            sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
            >
            <Drawer
                variant="permanent"
                open={true}
                sx={{'& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth } }}
                >
                <List>
                    {menu}
                </List>
            </Drawer>
        </Box>
    )
}
