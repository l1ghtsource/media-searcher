import React from 'react'
import cl from "./DescriptionMobile.module.css"
import FaceBtn from '../../UI/FaceBtn/FaceBtn'

function DescriptionMobile({description, cluster, faces}) {
  return (
    <div className={cl.descriptionMobileComponent}>
        <div className={cl.description}>
            <div className={cl.description__title}>Описание</div>
            <div className={cl.description__text}>{description}</div>
        </div>
        
        {cluster && cluster.length > 0 && (
          <div className={cl.cluster}>
            <div className={cl.cluster__title}>Подборки</div>
            <div className={cl.cluster__text}>
              { 
                cluster.map((c, index) => (
                  <div key={index}>{c.name}</div>
                ))                    
              }
            </div>
          </div>
        )}
        {
          faces && faces.length > 0 && (
            <div className={cl.faces}>
              <div className={cl.faces__title}>Блогеры на видео</div>
              <div className={cl.faces__text}>
                {
                  faces.map((face, index) => (
                    <FaceBtn key={index} face={face.url}/>
                  ))
                }
              </div>
            </div>
          )
        }
    </div>
  )
}

export default DescriptionMobile