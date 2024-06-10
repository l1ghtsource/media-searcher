import { useState } from 'react';
import Header from '../modules/Header/Header';
import MainPage from '../pages/MainPage/MainPage';
import './styles/main.css'
import { Navigate, Route, Routes } from 'react-router-dom';
import NewVideoPage from '../pages/NewVideoPage/NewVideoPage';

function App() {

  const [filters] = useState([
    {title: "Подборки", options: ["аниме", "баскетбол", "творчество", "мир видеоигр", "roblox", "мода"]},
    {title: "Лица", options: ["Райан Гослинг", "Марго Робби", "Влад А4", "Дима Масленников", "UtopiaShow", "Дубровский"]},
    // {title: "Язык", options: ["русский", "english"]},
  ])

  const [languages] = useState([
    {title: "Язык", options: ["русский", "english"]},
  ])

  const [videos, setVideos] = useState();

  return (
    <div className="App">
      <Header setVideos={setVideos}/>
      <Routes>
        <Route path='*' element={<Navigate to="/" replace/>}/>
        <Route path="/" element={<MainPage filters={filters} videos={videos} languages={languages}/>}/>
        <Route path="/addVideo" element={<NewVideoPage/>}/>
      </Routes>
    </div>
  );
}

export default App;
