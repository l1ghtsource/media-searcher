import React, { useState } from 'react'
import cl from "./TranscriptionInput.module.css"
import UploadBtn from '../../UI/UploadBtn/UploadBtn'
import LoadingCircle from '../../UI/LoadingCircle/LoadingCircle'
import Service from "../../api/Service"

function TranscriptionInput({url}) {
    const [isLoading, setIsLoading] = useState(false);
    const [text, setText] = useState("");

    async function startLoading(){
        setIsLoading(true);
        const response = await Service.getTranscription(url);
        setText(response);
        setIsLoading(false);
    }

    const rootClasses = [cl.textarea]
    if(isLoading){
        rootClasses.push(cl.textarea__loading)
    }

  return (
    <div className={cl.transcriptionInput}>
        <div className={cl.transcriptionInput__textarea}>
            <textarea 
            className={rootClasses.join(' ')} 
            readOnly 
            placeholder='Чтобы получить текст из видео нажмите кнопку “Transcription”'
            value={text}
            />
            {
                isLoading && (
                    <div className={cl.loading}>
                        <LoadingCircle/>
                    </div>
                )
            }
        </div>
        <div className={cl.transcriptionInput__btn}>
            <UploadBtn onClick={() => startLoading()} size="18px">Transcription</UploadBtn>
        </div>
    </div>
  )
}

export default TranscriptionInput