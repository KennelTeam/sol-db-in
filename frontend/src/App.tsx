import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";
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
import Questionnaire from "./Questionnaire";
import Options from "./Options";
import { UserType } from "./types/global";
import Users from "./Users";
import { Box, Container } from "@mui/material";
import { Stack } from "@mui/system";
import React from "react";
import { MENU_WIDTH } from "./types/global";
import FilterTablePage from "./FiltersTablePage";
import ErrorPage from "./ErrorPage";

function App() {

  const [user, setUser] = React.useState(UserType.None)
  // setUser later will be passed with props to the Login component for changing the user
  // at first when the site is loaded user must be UserType.None, and then it will be saved in cookies

  return (
    <BrowserRouter>
      <Stack direction="row" alignItems="stretch" spacing={0} sx={{maxWidth: "unset"}}>
        { user !== UserType.None && // it makes NavigationMenu shown only when user isn't None
        <Box  sx={{ width: MENU_WIDTH}} visibility="visible">
          <NavigationMenu user={user}/>
        </Box> }
        <Container sx={{ width: '100%', overflowX: "auto", margin: "0", maxWidth: "unset"}}  maxWidth={false}>
          <Routes >
            <Route path='/' element={<Navigate to={'/login'}/>}/>
          <Route path='/catalog' element={<Catalog />}/>
          <Route path='/leader/:id' element={<Leader />}/>
          <Route path='/leaders' element={<LeadersList />}/>
          <Route path='/login' element={<Login changeUser={setUser}/>}/>
          <Route path='/project/:id' element={<Project />}/>
          <Route path='/projects' element={<ProjectsList />}/>
          <Route path='/settings' element={<Settings />}/>
          <Route path='/statistics' element={<Statistics />}/>
          <Route path='/tags' element={<Tags />}/>
          <Route path='/questionnaire' element={<Questionnaire />}/>
          <Route path='/options' element={<Options />}/>
          <Route path='/users' element={<Users />}/>
          <Route path='/filters' element={<FilterTablePage formType="LEADER"/>}/> {/* route for testing FilterTablePage component */}
          <Route path='/error/:code' element={<ErrorPage/>}/>
          </Routes>
        </Container>
      </Stack>
    </BrowserRouter>
  );
}

export default App;
