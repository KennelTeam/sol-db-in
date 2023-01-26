import React from 'react'
import { List, ListItem, ListItemButton, ListItemText, Box, Drawer } from '@mui/material'
import { UserType, UserTypeProps } from '../types/global.d'
import { useTranslation } from 'react-i18next'

export default function NavigationMenu(props: UserTypeProps) {
    const drawerWidth: number = 200
    const { t } = useTranslation('translation', { keyPrefix: "translation.page_names" })
    // now you can test menu translation by going on /login page and press "Submit" button
    let menu_button = (text: string, path: string) => (
        <ListItem disablePadding>
            <ListItemButton href={path}>
                <ListItemText primary={t(text)} />
            </ListItemButton>
        </ListItem>
    )
    let projects, leaders, statistics, settings, users, tags, handbook
    projects = menu_button('projects', "/projects")
    leaders = menu_button("leaders", "/leaders")
    statistics = menu_button("statistics", "/statistics")
    settings = menu_button("settings", "/settings")
    users = menu_button("users", "/users")
    tags = menu_button("tags", "/tags")
    handbook = menu_button("handbook", "/handbook")

    let options_list
    switch (props.user) { // this switch choices pages that will be shown to user by his role
        case UserType.Admin:
            options_list = [leaders, projects, statistics, handbook, tags, settings, users]
            break
        case UserType.Editor:
            options_list = [leaders, projects, statistics, handbook, tags, settings]
            break
        case UserType.Junior:
            options_list = [leaders, projects, statistics, handbook]
            break
        case UserType.Guest:
            options_list = [leaders, projects, statistics]
            break
    }

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
                {options_list}
            </List>
        </Drawer>
    </Box>
  )
}
