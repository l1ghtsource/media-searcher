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


  const [videos, setVideos] = useState();

  useEffect(() => {
    const fetchFaces = async () => {
      try {
        const facesResponse = await Service.getFaces();
        setFaces(facesResponse); 
      } catch (error){
        console.log(error);
      }
    }

    const fetchFilters = async () => {
      try{
        const filtersResponse = await Service.getClusters();
        setFilters(filtersResponse);
      } catch (error) {
        console.log(error);
      }
    }

    fetchFilters();
    fetchFaces();
  }, [])

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
        <Route path="/" element={<MainPage filters={filters} videos={videos} faces={faces}/>}/>
        <Route path="/addVideo" element={<NewVideoPage/>}/>
      </Routes>
    </div>
  );
}

export default App;
