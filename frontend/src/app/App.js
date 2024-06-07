import { useState } from 'react';
import Header from '../modules/Header/Header';
import MainPage from '../pages/MainPage/MainPage';
import './styles/main.css'
import { Navigate, Route, Routes } from 'react-router-dom';
import NewVideoPage from '../pages/NewVideoPage/NewVideoPage';

function App() {

  const [filters] = useState([
    {title: "Подборки", options: ["аниме", "баскетбол", "творчество", "мир видеоигр", "roblox", "мода"]},
    // {title: "Язык", options: ["русский", "english"]},
  ])

  const [languages] = useState([
    {title: "Язык", options: ["русский", "english"]},
  ])

  const [videos] = useState([
    {
      url: "https://cdn-st.rutubelist.ru/media/e9/e0/b47a9df14a5e97942715e5e705c0/fhd.mp4",
      description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
      user: "@kto-to_tam",
      tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
    }, 
    {
      url: "https://cdn-st.rutubelist.ru/media/ac/08/3604604b4b8b89e34db1e0e91863/fhd.mp4",
      description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
      user: "@kto-to_tam",
      tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
    }, 
    {
      url: "https://cdn-st.rutubelist.ru/media/bf/6a/f040f0dd4afc90b8eb12c8d76571/fhd.mp4",
      description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
      user: "@kto-to_tam",
      tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
    }, 
    {
      url: "https://cdn-st.rutubelist.ru/media/22/78/acbe27254e819403d46eda7b3171/fhd.mp4",
      description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
      user: "@kto-to_tam",
      tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
    },
    {
      url: "https://cdn-st.rutubelist.ru/media/b9/7a/44c1ef97401abbaaf58511b039c9/fhd.mp4",
      description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
      user: "@kto-to_tam",
      tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
    }, 
    {
      url: "https://cdn-st.rutubelist.ru/media/16/f1/4ba070134b96a979888ba7ce95b7/fhd.mp4",
      description: "Какая-то инфа, которая была дана + которую мы выявили отдельно",
      user: "@kto-to_tam",
      tags: ["#такие_теги", "#ещё_теги", "#и_ещё_теги"],
    },  
  ])

  return (
    <div className="App">
      <Header/>
      <Routes>
        <Route path='*' element={<Navigate to="/" replace/>}/>
        <Route path="/" element={<MainPage filters={filters} videos={videos} languages={languages}/>}/>
        <Route path="/addVideo" element={<NewVideoPage/>}/>
      </Routes>
    </div>
  );
}

export default App;
