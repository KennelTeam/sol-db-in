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

function App() {
  return (
    <div>
      <BrowserRouter>
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
      </BrowserRouter>
      <NavigationMenu user={UserType.Editor}/> {/* side navigation menu. Later it may be moved to more correct place */}
    </div>
  );
}

export default App;
