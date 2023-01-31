import { BrowserRouter, Route, Routes } from "react-router-dom";
import Catalog from "./Catalog";
import Leader from "./Leader";
import LeadersList from "./LeadersList";
import Login from "./Login";
import NavigationMenu from "./NavigationMenu";
import Project from "./Project";
import ProjectsList from "./ProjectsList";
import Settings from "./Settings";
import Statistics from "./Statistics";
import Tags from "./Tags";
import { UserType } from "./types/global.d";
import Users from "./Users";
import { Box } from "@mui/material";
import { Stack } from "@mui/system";
import React from "react";

function App() {

  const [user, setUser] = React.useState(UserType.Editor)
  // setUser later will be passed with props to the Login component for changing the user
  // at first when site loaded user must be UserType.None, and then it will save via cookies
  const menuWidth = 200

  return (
    <BrowserRouter>
      <Stack direction="row" alignItems="stretch" spacing={0}>
        { user !== UserType.None && // it makes NavigationMenu shown only when user isn't None
          <Box  sx={{ width: { sm: menuWidth }, flexShrink: { sm: 0 } }}>
            <NavigationMenu user={user} width={menuWidth}/>
          </Box>
        }
        <Box>
          <Routes>
          <Route path='/catalog' element={<Catalog />}/>
          <Route path='/leader/:id' element={<Leader />}/>
          <Route path='/leaders' element={<LeadersList />}/>
          <Route path='/login' element={<Login />}/>
          <Route path='/project/:id' element={<Project />}/>
          <Route path='/projects' element={<ProjectsList />}/>
          <Route path='/settings' element={<Settings />}/>
          <Route path='/statistics' element={<Statistics />}/>
          <Route path='/tags' element={<Tags />}/>
          <Route path='/users' element={<Users />}/>
          </Routes>
        </Box>
      </Stack>
    </BrowserRouter>
  );
}

export default App;
