import React from 'react'
import cl from "./NewVideoPage.module.css"
import BackBtn from '../../UI/BackBtn/BackBtn'
import DragVideo from '../../components/DragVideo/DragVideo'
import FormVideo from '../../modules/FormVideo/FormVideo'

function NewVideoPage() {
  return (
    <div className={cl.newVideoPage}>
      <div className={cl.newVideoPage__title}>
        <BackBtn>Назад</BackBtn>
        <div className={cl.newVideoPageTitle}>Новая публикация</div>
      </div>
      <div className={cl.newVideoPage__form}>
        <DragVideo/>
        <FormVideo/>
      </div>
    </div>
  )
}

export default NewVideoPage