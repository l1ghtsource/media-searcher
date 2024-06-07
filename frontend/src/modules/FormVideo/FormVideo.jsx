import React from 'react'
import cl from "./FormVideo.module.css"
import FormInput from '../../components/FormInput/FormInput'
import UploadBtn from '../../UI/UploadBtn/UploadBtn'

function FormVideo() {
  return (
    <div className={cl.formVideo}>
        <FormInput placeholder="Добавить видео по ссылке"/>
        <FormInput placeholder="Описание"/>
        <UploadBtn>Загрузить</UploadBtn>
    </div>
  )
}

export default FormVideo