import React, { useEffect, useState } from 'react'
import SpeechRecognition, {useSpeechRecognition} from 'react-speech-recognition'
import cl from "./Header.module.css"
import logo from "../../assets/svgIcons/logo.svg"
import SearchInput from '../../components/SearchInput/SearchInput'
import SearchVoice from '../../components/SearchVoice/SearchVoice'
import AddVideoBtn from '../../components/AddVideoBtn/AddVideoBtn'
import ProfileBtn from '../../components/ProfileBtn/ProfileBtn'
import Service from "../../api/Service"
import { useNavigate } from 'react-router-dom'

function Header({setVideos}) {
  const [searchText, setSearchText] = useState('');
  const [typoText] = useState('');
  const { transcript, listening, resetTranscript } = useSpeechRecognition();
  let navigate = useNavigate();

  const handleVoiceInput = () => {
    resetTranscript();
    SpeechRecognition.startListening({
      continuous: false,
      language: 'ru-RU'
    })
  }

  const handleSearchInputKeyDown = async (e) => {
    if(e.key === "Enter" && searchText.length > 0){
      console.log('Отправка текста:', searchText);
      const response = await Service.getVideos(searchText);
      setVideos(response);
      navigate('/');
    }
  }

  useEffect(() => {
    // console.log('Распознанный текст:', transcript);
    setSearchText(transcript);
  }, [transcript]);

  useEffect(() => {
    console.log('Listening status:', listening);
  }, [listening]);

  return (
    <div className={cl.header}>
        <img src={logo} alt="Logo" />
        <div className={cl.searchDiv}>
            <div>
              <SearchInput 
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)} 
              onKeyDown={handleSearchInputKeyDown}
              />
              {
                typoText && (
                  <div className={cl.searchText__typo}>
                    <div className={cl.typo__text}>Показаны результаты по запросу <span>{typoText}</span></div>
                    <div className={cl.typo__btn}>Отмена</div>
                  </div>
                )
              }
            </div>
            <SearchVoice onClick={handleVoiceInput}/>
        </div>
        <div className={cl.rightHeader}>
            <AddVideoBtn/>
            <ProfileBtn/>
        </div>
    </div>
  )
}

export default Header