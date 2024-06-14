import React from 'react'
import cl from "./FormVideo.module.css"
import FormInput from '../../components/FormInput/FormInput'
import UploadBtn from '../../UI/UploadBtn/UploadBtn'

function FormVideo({videoFile, videoLink, setVideoLink, onClick, setDescription}) {
  const handleDescriptionChange = (e) => {
    setDescription(e.target.value);
  };

  const handleVideoLinkChange = (e) => {
    setVideoLink(e.target.value);
  };

  const isDisabled = !(videoFile || videoLink)

  return (
    <div className={cl.formVideo}>
        <FormInput placeholder="Добавить видео по ссылке" onChange={handleVideoLinkChange}/>
        <FormInput placeholder="Описание" onChange={handleDescriptionChange}/>
        <UploadBtn isDisabled={isDisabled} size="18px" onClick={onClick}>Загрузить</UploadBtn>
    </div>
  )
}

export default FormVideo