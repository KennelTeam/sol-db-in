import { BrowserRouter, Route, Routes } from "react-router-dom";
import Handbook from "./Handbook";
import Leader from "./Leader";
import LeadersList from "./LeadersList";
import Login from "./Login";
import Project from "./Project";
import ProjectsList from "./ProjectsList";
import Settings from "./Settings";
import Statistics from "./Statistics";
import Tags from "./Tags";
import Users from "./Users";

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path='/handbook' element={<Handbook />}/>
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
    </div>
  );
}

export default App;
