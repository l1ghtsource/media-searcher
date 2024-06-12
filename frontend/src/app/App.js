import { useEffect, useState } from 'react';
import Header from '../modules/Header/Header';
import MainPage from '../pages/MainPage/MainPage';
import './styles/main.css'
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import NewVideoPage from '../pages/NewVideoPage/NewVideoPage';
import useWindowWidth from '../hooks/useWindowWidth';

function App() {

  const [isHeader, setIsHeader] = useState(true);
  const location = useLocation();
  const windowWidth = useWindowWidth();

  const [filters] = useState([
    {title: "Подборки", options: ["аниме", "баскетбол", "творчество", "мир видеоигр", "roblox", "мода"]},
    {title: "Лица", options: ["Райан Гослинг", "Марго Робби", "Влад А4", "Дима Масленников", "UtopiaShow", "Дубровский"]},
    {title: "Лица", options: ["Райан Гослинг", "Марго Робби", "Влад А4", "Дима Масленников", "UtopiaShow", "Дубровский"]},
    {title: "Лица", options: ["Райан Гослинг", "Марго Робби", "Влад А4", "Дима Масленников", "UtopiaShow", "Дубровский"]},
    // {title: "Язык", options: ["русский", "english"]},
  ])

  const [languages] = useState([
    {title: "Язык", options: ["русский", "english"]},
  ])

  const [videos, setVideos] = useState();

  useEffect(() => {
    if (location.pathname === "/addVideo") {
      setIsHeader(false);
      document.body.classList.add('scrollable');
    } else {
      setIsHeader(true);
      document.body.classList.remove('scrollable');
    }
  }, [location]);

  return (
    <div className="App">
      {
        (isHeader || windowWidth > 992) && (
          <Header setVideos={setVideos}/>
        )
      }
      <Routes>
        <Route path='*' element={<Navigate to="/" replace/>}/>
        <Route path="/" element={<MainPage filters={filters} videos={videos} languages={languages}/>}/>
        <Route path="/addVideo" element={<NewVideoPage/>}/>
      </Routes>
    </div>
  );
}

export default App;
