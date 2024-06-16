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

  async function sendVideo() {
    if (videoFile) {
      try {
        const [status, id] = await Service.putVideo(videoFile, description);
        if (status >= 400 && status < 600) {
          setIsError(true);
        } else {
          console.log(id);
          setIsSuccess(true);
          setIdVideo(id);
        }
      } catch (error) {
        setIsError(true);
      }
    } else if (videoLink) {
      try {
        const response = await Service.postVideoLink(videoLink, description);
        if (response.status >= 400 && response.status < 600) {
          setIsError(true);
        } else {
          console.log(response);
          setIdVideo(response.id);
          setIsSuccess(true);
        }
      } catch (error) {
        setIsError(true);
      }
    } else {
      console.error("No video file or link to upload!");
    }

    // Очистка полей после обработки
    setVideoLink('');
    setDescription('');
    setVideoFile(null);
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

export default NewVideoPage;
