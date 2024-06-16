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
  const [isError, setIsError] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  function sendVideo(){
    if(videoFile) {
      const response = Service.putVideo(videoFile, description);
      if (response.status >= 400 && response.status < 600) {
        setIsError(true);
      } else {
        setVideoLink(null);
        setDescription(null);
        setIsSuccess(true);
      }
      console.log(videoFile, description);
    } else if (videoLink) {
      const response = Service.postVideoLink(videoLink, description); 
      if(response.status >= 400 && response.status < 600){
        setIsError(true);
      } else {
        setDescription(null);
        setVideoFile(null);
        setIsSuccess(true);
      }
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
        <DragVideo setVideoFile={setVideoFile} isError={isError} isSuccess={isSuccess}/>
        <FormVideo 
          videoFile={videoFile} 
          videoLink={videoLink} 
          setVideoLink={setVideoLink} 
          onClick={sendVideo} 
          setDescription={setDescription}
          isError={isError}
          isSuccess={isSuccess}
        />
      </div>
    </div>
  )
}

export default NewVideoPage