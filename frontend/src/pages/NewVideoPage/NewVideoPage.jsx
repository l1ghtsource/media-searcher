import React, { useState } from 'react'
import cl from "./NewVideoPage.module.css"
import BackBtn from '../../UI/BackBtn/BackBtn'
import DragVideo from '../../components/DragVideo/DragVideo'
import FormVideo from '../../modules/FormVideo/FormVideo'
import Service from "../../api/Service"

function NewVideoPage() {
  const [videoFile, setVideoFile] = useState(null);
  const [videoLink, setVideoLink] = useState('');
  const [description, setDescription] = useState('');
  const [isError, setIsError] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [idVideo, setIdVideo] = useState(null);

  function sendVideo(){
    if(videoFile) {
      const [status, id] = Service.putVideo(videoFile, description);
      if (status === 200 || status === 204) {
        setIsError(true);
      } else {
        console.log(id)
        setIsSuccess(true);
        setIdVideo(id);
      }
      setVideoLink('');
      setDescription('');
      setVideoFile(null);
    } else if (videoLink) {
      const response = Service.postVideoLink(videoLink, description); 
      if(response.status === 200 || response.status === 204){
        setIsError(true);
      } else {
        console.log(response);
        setIdVideo(response.id);
        setIsSuccess(true);
      }
      setVideoLink('');
      setDescription('');
      setVideoFile(null);
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
        <DragVideo setVideoFile={setVideoFile} isError={isError} isSuccess={isSuccess} videoFile={videoFile}/>
        <FormVideo 
          videoFile={videoFile} 
          videoLink={videoLink} 
          setVideoLink={setVideoLink} 
          onClick={sendVideo} 
          setDescription={setDescription}
          isError={isError}
          isSuccess={isSuccess}
          idVideo={idVideo}
          description={description}
        />
      </div>
    </div>
  )
}

export default NewVideoPage