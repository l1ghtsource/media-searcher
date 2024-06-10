import React, { useState, useEffect, useRef } from 'react';
import cl from "./MainPage.module.css";
import FiltersComponent from '../../components/FiltersComponent/FiltersComponent';
import VideoComponent from '../../components/VideoComponent/VideoComponent';
import ProfileBtn from '../../components/ProfileBtn/ProfileBtn';
import TranscriptionInput from '../../components/TranscriptionInput/TranscriptionInput';

function MainPage({ filters, videos, languages }) {
  const [playingVideoIndex, setPlayingVideoIndex] = useState(null);
  const videoRefs = useRef([]);

  const handlePlay = (index) => {
    if (playingVideoIndex !== null && playingVideoIndex !== index) {
      const previousVideo = document.getElementById(`video-${playingVideoIndex}`);
      if (previousVideo) {
        previousVideo.pause();
      }
    }
    setPlayingVideoIndex(index);
  };

  useEffect(() => {
    // Отменяем скролл при размонтировании компонента
    return () => {
      window.scrollTo(0, 0);
    };
  }, []);

  useEffect(() => {
    let timerId;
    const handleKeyPress = (e) => {
      if (videos && videos.length > 0){
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

    // console.log(playingVideoIndex);
    document.addEventListener('keydown', handleKeyPress);
  
    if (playingVideoIndex !== null && videoRefs.current[playingVideoIndex]) {
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
  }, [playingVideoIndex, videos]);

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
      }
    }

    const handleScroll = (e) => {
      if (videos && videos.length > 0) {
        if (e.deltaY !== undefined) { // Обработка скролла на компьютерах
          if (e.deltaY < 0) {
            clearTimeout(timerId);
            timerId = setTimeout(() => {
              setPlayingVideoIndex((prevIndex) => (prevIndex === null ? 0 : Math.max(prevIndex - 1, 0)));
            }, 150); 
          } else if (e.deltaY > 0) {
            clearTimeout(timerId);
            timerId = setTimeout(() => {
              setPlayingVideoIndex((prevIndex) => (prevIndex === null ? 0 : Math.min(prevIndex + 1, videos.length - 1)));
            }, 150); 
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
  }, [videos, playingVideoIndex]);

  return (
    <div className={cl.mainPage}>
      <div className={cl.mainPage__filters}>
        <FiltersComponent filters={filters} />
      </div>

      <div className={cl.mainPage__videos}>
        {videos &&
          videos.map((video, index) => (
            <div ref={(el) => (videoRefs.current[index] = el)} className={cl.video} key={index}>
              <VideoComponent url={video.url} id={`video-${index}`} onPlay={() => handlePlay(index)} />
              <div className={cl.video__info}>
                <div className={cl.videoInfo__profile}>
                  <ProfileBtn />
                  <div>{video.user}</div>
                </div>
                <div className={cl.videoInfo__transcription}>
                  <TranscriptionInput url={video.url} />
                </div>
              </div>
            </div>
          ))}
      </div>

      <div className={cl.mainPage__language}>
        <FiltersComponent filters={languages} />
      </div>
    </div>
  );
}

export default MainPage;
