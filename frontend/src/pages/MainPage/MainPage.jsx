import React from 'react'
import cl from "./MainPage.module.css"
import FiltersComponent from '../../components/FiltersComponent/FiltersComponent'
import VideoComponent from '../../components/VideoComponent/VideoComponent'
import ProfileBtn from '../../components/ProfileBtn/ProfileBtn'

function MainPage({filters, videos, languages}) {
  return (
    <div className={cl.mainPage}>

      <div className={cl.mainPage__filters}>
        <FiltersComponent filters={filters}/>
      </div>

      <div className={cl.mainPage__videos}>
        {
          videos && videos.map((video, index) => (
            <div className={cl.video}>
              <VideoComponent key={index} url={video.url}/>
              <div className={cl.video__info}> 
                <div className={cl.videoInfo__profile}>
                  <ProfileBtn/>
                  <div>{video.user}</div>
                </div>
                <div className={cl.videoInfo__description}>
                  <div className={cl.description__title}>Описание</div>
                  <div className={cl.description__text}>{video.description}</div>
                </div>
                <div className={cl.videoInfo__tags}>
                  {
                    video.tags && video.tags.map((tag) => (
                      <div>{tag}</div>
                    ))
                  }
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