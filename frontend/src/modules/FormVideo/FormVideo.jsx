import React from 'react'
import cl from "./FormVideo.module.css"
import FormInput from '../../components/FormInput/FormInput'
import UploadBtn from '../../UI/UploadBtn/UploadBtn'

function FormVideo({videoFile, videoLink, setVideoLink, onClick, setDescription, isError, isSuccess, idVideo, description}) {
  
  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleVideoLinkChange = (e) => {
    setVideoLink(e.target.value);
  };

  const isDisabled = !(videoFile || videoLink)

  return (
    <div className={cl.formVideo}>
        <FormInput placeholder="Добавить видео по ссылке" onChange={handleVideoLinkChange} value={videoLink}/>
        <FormInput placeholder="Описание" onChange={handleDescriptionChange} value={description}/>
        <UploadBtn isDisabled={isDisabled} size="18px" onClick={onClick}>Загрузить</UploadBtn>
        {
          isError && (
            <div className={cl.errorBlock}>
              ❌error
            </div>
          )
        }
        {
          isSuccess && (
            <div className={cl.successBlock}>
              ✅success
              {
                idVideo && (
                  <div>Ваши видео доступно по <a href={`https://itut.itatmisis.ru/api/video?video_id=${idVideo}`}>ссылке</a></div>
                )
              }
            </div>
          )
        }
    </div>
  )
}

export default FormVideo