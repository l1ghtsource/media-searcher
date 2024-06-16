import React, { useState, useEffect, useRef } from 'react';
import cl from "./MainPage.module.css";
import FiltersComponent from '../../components/FiltersComponent/FiltersComponent';
import VideoComponent from '../../components/VideoComponent/VideoComponent';
import ProfileBtn from '../../components/ProfileBtn/ProfileBtn';
// import TranscriptionInput from '../../components/TranscriptionInput/TranscriptionInput';
import FacesComponent from '../../components/FacesComponent/FacesComponent';
import AddVideoBtn from '../../components/AddVideoBtn/AddVideoBtn';
import filter from "../../assets/svgIcons/filter.svg"
import FiltersMobileComponent from '../../components/FiltersMobileComponent/FiltersMobileComponent';
import Service from '../../api/Service';
import FaceBtn from '../../UI/FaceBtn/FaceBtn';

function MainPage({ filters, videos, setVideos, faces }) {
  const [playingVideoIndex, setPlayingVideoIndex] = useState(null);
  const videoRefs = useRef([]);
  const [selectedOptions, setSelectedOptions] = useState({});
  const [isFilters, setIsFilters] = useState(false);
  const [isTranscription, setIsTranscription] = useState(false);
  const [isDescription, setIsDescription] = useState(false);
  const [loadedVideosCount, setLoadedVideosCount] = useState(10);
  
  const toggleDescription = () => {
    setIsFilters(false);
    setIsTranscription(false);
    setIsDescription(prevState => !prevState);
  }

  const toggleFilters = () => {
    setIsDescription(false);
    setIsTranscription(false);
    setIsFilters(prevState => !prevState);
  }

  const toggleTranscription = () => {
    setIsDescription(false);
    setIsFilters(false);
    setIsTranscription(prevState => !prevState);
  }

  const handlePlay = (index) => {
    if (playingVideoIndex !== null && playingVideoIndex !== index) {
      const previousVideo = document.getElementById(`video-${playingVideoIndex}`);
      if (previousVideo) {
        previousVideo.pause();
      }
    }
    setPlayingVideoIndex(index);
  };

  //Функция для выбора опций
  const toggleOption = (filterTitle, optionId) => {
    setSelectedOptions(prevState => {
        const newState = { ...prevState };
        if (!newState[filterTitle]) {
            newState[filterTitle] = new Set();
        }
        if (newState[filterTitle].has(optionId)) {
            newState[filterTitle].delete(optionId);
        } else {
            newState[filterTitle].add(optionId);
        }
        return newState;
    });
  };  

  // Поиск видео по кластерам
  useEffect(() => {  
    const fetchFilteredVideos = async (selectedOptions) => {
      const fil = {};
      for (const [key, value] of Object.entries(selectedOptions)) {
        fil[key] = Array.from(value);
      }
      let clusters = [];
  
      // Определение метода API в зависимости от выбранной опции
      if (fil["Подборки"] && fil["Подборки"].length > 0) {
        // Выбраны подборки, вызываем метод getVideoSelectedClusters
        clusters = await Service.getVideoSelectedClusters(fil["Подборки"]);
      } else if (fil["Блогеры"] && fil["Блогеры"].length > 0) {
        // Выбраны блогеры, вызываем метод getVideoSelectedFaces
        clusters = await Service.getVideoSelectedFaces(fil["Блогеры"]);
      }
  
      setVideos(clusters);
      setPlayingVideoIndex(0);
    };
  
    if (Object.keys(selectedOptions).length > 0) {
      fetchFilteredVideos(selectedOptions);
    }
  }, [selectedOptions, setVideos]);
  

  useEffect(() => {
    // Отменяем скролл при размонтировании компонента
    return () => {
      window.scrollTo(0, 0);
    };
  }, []);

  //Изменения видео по стрелочкам
  useEffect(() => {
    let timerId;
    const handleKeyPress = (e) => {
      if (!isTranscription && !isFilters && videos && videos.length > 0){
        if (e.key === 'ArrowUp' || e.key === 'ArrowDown'){
          e.preventDefault(); // предотвращаем стандартное действие клавиш
          if (e.key === 'ArrowUp') {
            setPlayingVideoIndex((prevIndex) => (prevIndex === null ? 0 : Math.max(prevIndex - 1, 0)));
          } else if (e.key === 'ArrowDown') {
            setPlayingVideoIndex((prevIndex) => (prevIndex === null ? 0 : Math.min(prevIndex + 1, videos.length - 1)));
          }
        }   
      }
      
    };

    document.addEventListener('keydown', handleKeyPress);
  
    if (!isTranscription && !isFilters && playingVideoIndex !== null && videoRefs.current[playingVideoIndex]) {
      const element = videoRefs.current[playingVideoIndex];
      const offset = window.innerWidth < 992 ? 0 : 120;; // Здесь можно задать желаемое смещение от верха блока
      const topPosition = element.offsetTop - offset;
      window.scrollTo({
        top: topPosition,
        behavior: 'smooth',
      });
    }
  
    return () => {
      document.removeEventListener('keydown', handleKeyPress);
      clearTimeout(timerId);
    };
  }, [playingVideoIndex, videos, isFilters, isTranscription]);

  //Изменения видео по скроллу
  useEffect(() => {
    let timerId;
    let startY = 0;
    
    if (videos && videos.length > 0 && playingVideoIndex !== null) {
      // Останавливаем предыдущее видео при смене индекса
      const previousIndex = playingVideoIndex === 0 ? null : playingVideoIndex - 1;
      const nextIndex = playingVideoIndex === videos.length - 1 ? null : playingVideoIndex + 1;
      
      const previousVideo = document.getElementById(`video-${previousIndex}`);
      if (previousVideo) {
        previousVideo.pause();
      }
      
      const nextVideo = document.getElementById(`video-${nextIndex}`);
      if (nextVideo) {
        nextVideo.pause();
      }
  
      // Автоматически запускаем новое видео при смене индекса
      const videoToPlay = document.getElementById(`video-${playingVideoIndex}`);
      if (videoToPlay) {
        videoToPlay.play();
      }

      // Автоматически получаем новые видео при прохождение предпоследнего видео в списке
      if(videos.length - 2 > 0 && playingVideoIndex === videos.length - 2){
        console.log('Получить новые видео');
        setLoadedVideosCount(prevCount => prevCount + 10);
      }
    }

    const handleScroll = (e) => {
      if (!isTranscription && !isFilters && videos && videos.length > 0) {
        if (e.deltaY !== undefined) { // Обработка скролла на компьютерах
          if (e.deltaY < 0) {
            clearTimeout(timerId);
            timerId = setTimeout(() => {
              setPlayingVideoIndex((prevIndex) => (prevIndex === null ? 0 : Math.max(prevIndex - 1, 0)));
            }, 100); 
          } else if (e.deltaY > 0) {
            clearTimeout(timerId);
            timerId = setTimeout(() => {
              setPlayingVideoIndex((prevIndex) => (prevIndex === null ? 0 : Math.min(prevIndex + 1, videos.length - 1)));
            }, 100); 
          }
        } else if (e.touches !== undefined) { // Обработка скролла на мобильных устройствах
          const deltaY = e.touches[0].clientY - startY;
          if (deltaY > 50) { // задаем минимальное смещение, чтобы считать это скроллом вверх
            clearTimeout(timerId);
            timerId = setTimeout(() => {
              setPlayingVideoIndex((prevIndex) => (prevIndex === null ? 0 : Math.max(prevIndex - 1, 0)));
            }, 150); 
          } else if (deltaY < -50) { // задаем минимальное смещение, чтобы считать это скроллом вниз
            clearTimeout(timerId);
            timerId = setTimeout(() => {
              setPlayingVideoIndex((prevIndex) => (prevIndex === null ? 0 : Math.min(prevIndex + 1, videos.length - 1)));
            }, 150); 
          }
        }
      }
    };
  
    const handleTouchStart = (e) => {
      startY = e.touches[0].clientY;
    };
  
    document.addEventListener('wheel', handleScroll);
    document.addEventListener('touchmove', handleScroll);
    document.addEventListener('touchstart', handleTouchStart);
  
    return () => {
      document.removeEventListener('wheel', handleScroll);
      document.removeEventListener('touchmove', handleScroll);
      document.removeEventListener('touchstart', handleTouchStart);
      clearTimeout(timerId);
    };
  }, [videos, playingVideoIndex, isFilters, isTranscription]);

  // // Эффект для прокрутки к первому видео при изменении списка видео
  // useEffect(() => {
  //   if (videos && videos.length > 0) {
  //     // Останавливаем текущее воспроизводимое видео
  //     if (playingVideoIndex !== null) {
  //       const currentVideo = document.getElementById(`video-${playingVideoIndex}`);
  //       if (currentVideo) {
  //         currentVideo.pause();
  //       }
  //     }
  //     setPlayingVideoIndex(0);
  //     window.scrollTo({
  //       top: 0,
  //       behavior: 'auto',
  //     });
  //   }
  // }, [videos, playingVideoIndex]);

  return (
    <div className={cl.mainPage}>
      <div className={cl.mainPage__filters}>
        <FiltersComponent filters={filters} selectedOptions={selectedOptions} toggleOption={toggleOption}/>
      </div>   
      <div className={cl.mainPage__faces}>
        <FacesComponent faces={faces} selectedOptions={selectedOptions} toggleOption={toggleOption}/>
      </div>
      <div className={cl.mainPage__videos}>
        {videos &&
          videos.slice(0, loadedVideosCount).map((video, index) => (
            <div ref={(el) => (videoRefs.current[index] = el)} className={cl.video} key={index}>
              <VideoComponent 
              videoInfo={{url: video.url, description: video.description, facesVideo: video.faces, cluster: video.cluster}}
              id={`video-${index}`} 
              onPlay={() => handlePlay(index)}
              selectedOptions={selectedOptions}
              toggleOption={toggleOption}
              faces={faces}
              filters={filters}
              isFilters={isFilters}
              isTranscription={isTranscription}
              onToggleFilters={toggleFilters}
              onToggleTranscription={toggleTranscription}
              isDescription={isDescription}
              onToggleDescription={toggleDescription}
              />
              <div className={cl.video__info}>
                <div className={cl.videoInfo__profile}>
                  <ProfileBtn />
                  <div>{video.user}</div>
                </div>
                <div className={cl.videoInfo__description}>
                  <div className={cl.description__title}>Описание</div>
                  <div className={cl.description__text}>{video.description}</div>
                </div>
                {video.cluster && video.cluster.length > 0 && (
                  <div className={cl.videoInfo__cluster}>
                    <div className={cl.cluster__title}>Подборки</div>
                    <div className={cl.cluster__text}>
                      { 
                        video.cluster.map((cluster, index) => (
                          <div key={index}>{cluster.name}</div>
                        ))                    
                      }
                    </div>
                  </div>
                )}
                {
                  video.faces && video.faces.length > 0 && (
                    <div className={cl.videoInfo__faces}>
                      <div className={cl.faces__title}>Блогеры на видео</div>
                      <div className={cl.faces__text}>
                        {
                          video.faces.map((face, index) => (
                            <FaceBtn key={index} face={face.url}/>
                          ))
                        }
                      </div>
                    </div>
                  )
                }
                
                {/* <div className={cl.videoInfo__transcription}>
                  <TranscriptionInput url={video.url} />
                </div> */}
              </div>
            </div>
          ))}
      </div>
      {
        videos && videos.length === 0 && (
          <div>
            <div className={cl.mainPage__addVideo}>
                <AddVideoBtn/>
            </div>
            <div className={cl.mainPage__btn}>
                <div className={isFilters ? `${cl.filterBtn} ${cl.active}` : cl.filterBtn}>
                  <img src={filter} alt="filter" onClick={toggleFilters} />
                </div>
            </div>
            {
              isFilters && (
                <div className={cl.filtersMobile}>
                  <FiltersMobileComponent filters={filters} selectedOptions={selectedOptions} toggleOption={toggleOption} faces={faces}/>
                </div>
              )
            }
          </div>
        )
      }
      
    </div>
  );
}

export default MainPage;
