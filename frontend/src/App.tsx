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
import {useTranslation} from "react-i18next";
import ErrorPage from "./ErrorPage";
import FullnessStatistics from "./Statistics/Fullness";
import DistributionStatistics from "./Statistics/Distribution";
import TagsStats from "./Statistics/TagsStats";
import TagsUsage from "./Statistics/TagsUsage";

function App() {
  const {t} = useTranslation('translation', { keyPrefix: 'main' });
  const [user, setUser] = React.useState(UserType.Admin)
  // setUser later will be passed with props to the Login component for changing the user
  // at first when the site is loaded user must be UserType.None, and then it will be saved in cookies
  document.title = t('title')

  const changeUser = (user: UserType) => {
    console.log(user)
    setUser(user)
  }

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
          <Route path='/login' element={<Login changeUser={changeUser}/>}/>
          <Route path='/project/:id' element={<Project />}/>
          <Route path='/projects' element={<ProjectsList />}/>
          <Route path='/settings' element={<Settings />}/>
          <Route path='/statistics/fullness' element={<FullnessStatistics />}/>
          <Route path='/statistics/distribution' element={<DistributionStatistics />}/>
          <Route path='/statistics/tags' element={<TagsStats />}/>
            <Route path='/statistics/tags_usage' element={<TagsUsage />}/>
          <Route path='/tags' element={<Tags />}/>
          <Route path='/questionnaire' element={<Questionnaire />}/>
          <Route path='/options' element={<Options />}/>
          <Route path='/users' element={<Users />}/>
          <Route path='/filters' element={<FilterTablePage formType="LEADER"/>}/> {/* route for testing FilterTablePage component */}
          <Route path='/error/:code' element={<ErrorPage/>}/>
          <Route path='*' element={<Navigate to='/error/404_client'/>}/>
          </Routes>
        </Container>
      </Stack>
    </BrowserRouter>
  );
}

export default App;
