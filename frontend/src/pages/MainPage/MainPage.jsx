import React, { useState } from 'react'
import cl from "./MainPage.module.css"
import FiltersComponent from '../../components/FiltersComponent/FiltersComponent'
import VideoComponent from '../../components/VideoComponent/VideoComponent'
import ProfileBtn from '../../components/ProfileBtn/ProfileBtn'
import TranscriptionInput from '../../components/TranscriptionInput/TranscriptionInput'

function MainPage({filters, videos, languages}) {

  const [playingVideoIndex, setPlayingVideoIndex] = useState(null);

  const handlePlay = (index) => {
    if (playingVideoIndex !== null && playingVideoIndex !== index){
      const previousVideo = document.getElementById(`video-${playingVideoIndex}`);
      if(previousVideo){
        previousVideo.pause();
      }
    }
    setPlayingVideoIndex(index);
  }


  return (
    <div className={cl.mainPage}>

      <div className={cl.mainPage__filters}>
        <FiltersComponent filters={filters}/>
      </div>

      <div className={cl.mainPage__videos}> 
        {
          videos && videos.map((video, index) => (
            <div className={cl.video} key={index}>
              <VideoComponent url={video.url} id={`video-${index}`} onPlay={() => handlePlay(index)} />
              <div className={cl.video__info}> 
                <div className={cl.videoInfo__profile}>
                  <ProfileBtn/>
                  <div>{video.user}</div>
                </div>
                {/* // TODO: ПОКА УБИРАЕМ ЭТО  */}
                {/* <div className={cl.videoInfo__description}>
                  <div className={cl.description__title}>Описание</div>
                  <div className={cl.description__text}>{video.description}</div>
                </div>
                <div className={cl.videoInfo__tags}>
                  {
                    video.tags && video.tags.map((tag, index) => (
                      <div key={index}>{tag}</div>
                    ))
                  }
                </div> */}
                <div className={cl.videoInfo__transcription}>
                  <TranscriptionInput url={video.url}/>
                </div>
              </div>
            </div>
          ))
        }
      </div>

      <div className={cl.mainPage__language}>
        <FiltersComponent filters={languages}/>
      </div>

    </div>
  )
}

export default MainPage