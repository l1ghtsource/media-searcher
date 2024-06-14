import React, { useState } from 'react'
import cl from "./NewVideoPage.module.css"
import BackBtn from '../../UI/BackBtn/BackBtn'
import DragVideo from '../../components/DragVideo/DragVideo'
import FormVideo from '../../modules/FormVideo/FormVideo'
import Service from "../../api/Service"

function NewVideoPage() {
  const [videoFile, setVideoFile] = useState(null);
  const [videoLink, setVideoLink] = useState(null);
  const [description, setDescription] = useState(null);

  function sendVideo(){
    if(videoFile) {
      Service.putVideo(videoFile, description);
      console.log(videoFile, description);
    } else if (videoLink) {
      Service.putVideo(videoLink, description); // Assuming you have a method to handle video links
      console.log(videoLink, description);
    } else {
      console.error("No video file or link to upload!")
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
        <FormVideo 
          videoFile={videoFile} 
          videoLink={videoLink} 
          setVideoLink={setVideoLink} 
          onClick={sendVideo} 
          setDescription={setDescription}
        />
      </div>
    </div>
  )
}

export default NewVideoPage