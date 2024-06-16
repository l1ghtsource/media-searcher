import { useEffect, useState } from 'react';
import Header from '../modules/Header/Header';
import MainPage from '../pages/MainPage/MainPage';
import './styles/main.css'
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import NewVideoPage from '../pages/NewVideoPage/NewVideoPage';
import useWindowWidth from '../hooks/useWindowWidth';
import Service from "../api/Service"

function App() {

  const [isHeader, setIsHeader] = useState(true);
  const location = useLocation();
  const windowWidth = useWindowWidth();

  const [filters, setFilters] = useState([])
  const [faces, setFaces] = useState([])
  const [videos, setVideos] = useState([{
    url: "https://cdn-st.rutubelist.ru/media/e9/e0/b47a9df14a5e97942715e5e705c0/fhd.mp4",
    description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
    user: "@kto-to_tam",
    clusters: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
    faces: [""],
  }, ]);

  useEffect(() => {

    // Получение лиц
    const fetchFaces = async () => {
      try {
        const facesResponse = await Service.getFaces();
        setFaces([facesResponse]);
        console.log([facesResponse]); 
      } catch (error){
        console.log(error);
      }
    }

    // Получение фильтров
    const fetchFilters = async () => {
      try{
        const filtersResponse = await Service.getClusters();
        setFilters([filtersResponse]);
        console.log([filtersResponse]);
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
