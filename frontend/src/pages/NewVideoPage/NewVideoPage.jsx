import React, { useState } from 'react'
import cl from "./NewVideoPage.module.css"
import BackBtn from '../../UI/BackBtn/BackBtn'
import DragVideo from '../../components/DragVideo/DragVideo'
import FormVideo from '../../modules/FormVideo/FormVideo'
import Service from "../../api/Service"

function NewVideoPage() {
  const [videoFile, setVideoFile] = useState(null);

  function sendVideo(){
    if(videoFile) {
      Service.postVideo(videoFile);
      console.log(videoFile);
    } else {
      console.error("No video file to upload!")
    }
  }

  return (
    <div className={cl.newVideoPage}>
      <div className={cl.newVideoPage__title}>
        <BackBtn>Назад</BackBtn>
        <div className={cl.newVideoPageTitle}>Новая публикация</div>
      </div>
      <div className={cl.newVideoPage__form}>
        <DragVideo setVideoFile={setVideoFile}/>
        <FormVideo onClick={sendVideo}/>
      </div>
    </div>
  )
}

export default NewVideoPage