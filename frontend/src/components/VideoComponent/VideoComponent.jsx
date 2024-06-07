import React from 'react'
import cl from './VideoComponent.module.css'

function VideoComponent({url}) {
  return (
    <video className={cl.video} controls loop preload='metadata' src={url}>
        Простите, но ваш браузер не поддерживает встроенные видео.
        Попробуйте скачать видео <a href={url}>по этой ссылке</a>
        и открыть его на своём устройстве.
    </video>
  )
}

export default VideoComponent