import { useEffect, useState } from 'react';
import Header from '../modules/Header/Header';
import MainPage from '../pages/MainPage/MainPage';
import './styles/main.css'
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import NewVideoPage from '../pages/NewVideoPage/NewVideoPage';
import useWindowWidth from '../hooks/useWindowWidth';
import Service from "../api/Service"
import a4 from "../assets/svgIcons/a4.jpg"
import egorik from "../assets/svgIcons/egorik.jpg"
import durov from "../assets/svgIcons/durov.png"
import tinkoff from "../assets/svgIcons/tinkoff.jpg"
import maslennikov from "../assets/svgIcons/maslennikov.jpg"

function App() {

  const [isHeader, setIsHeader] = useState(true);
  const location = useLocation();
  const windowWidth = useWindowWidth();

  const [filters, setFilters] = useState([
    {title: "Подборки", options: [
      {id: 0, name: "Баскетбол"},
      {id: 1, name: "Машины"},
      {id: 2, name: "Roblox"},
      {id: 3, name: "Аниме"},
      {id: 4, name: "Мир видеоигр"},
    ]}
  ])
  const [faces, setFaces] = useState([
    {title: "Блогеры", options: [
      {id: 0, name: "Баскетбол", url: a4},
      {id: 1, name: "Машины", url: egorik},
      {id: 2, name: "Roblox", url: maslennikov},
      {id: 3, name: "Аниме", url: tinkoff},
      {id: 4, name: "Мир видеоигр", url: durov},
    ]}
  ])
  const [videos, setVideos] = useState([]);

  useEffect(() => {

    // Получение лиц
    const fetchFaces = async () => {
      try {
        const facesResponse = await Service.getFaces();
        if (facesResponse.status === 200){
          setFaces([facesResponse.data]);
        console.log([facesResponse.data]);
        }
         
      } catch (error){
        console.log(error);
      }
    }

    // Получение фильтров
    const fetchFilters = async () => {
      try{
        const filtersResponse = await Service.getClusters();
        if (filtersResponse.status === 200){
          setFilters([filtersResponse.data]);
          console.log([filtersResponse.data]);
        }
      } catch (error) {
        console.log(error);
      }
    }

    fetchFilters();
    fetchFaces();
  }, [])

  // UseEffect, который следит за путем
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
        <Route path="/" element={<MainPage filters={filters} videos={videos} setVideos={setVideos} faces={faces}/>}/>
        <Route path="/addVideo" element={<NewVideoPage/>}/>
      </Routes>
    </div>
  );
}

export default App;
