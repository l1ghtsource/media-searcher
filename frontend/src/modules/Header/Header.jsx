import React, { useEffect, useRef, useState } from 'react'
import SpeechRecognition, {useSpeechRecognition} from 'react-speech-recognition'
import cl from "./Header.module.css"
import logo from "../../assets/svgIcons/logo.svg"
import SearchInput from '../../components/SearchInput/SearchInput'
import SearchVoice from '../../components/SearchVoice/SearchVoice'
import AddVideoBtn from '../../components/AddVideoBtn/AddVideoBtn'
import ProfileBtn from '../../components/ProfileBtn/ProfileBtn'
import Service from "../../api/Service"
import { useNavigate } from 'react-router-dom'
import { Link } from 'react-router-dom'
import AutoComplete from '../../components/AutoComplete/AutoComplete'

function Header({setVideos}) {
  const [searchText, setSearchText] = useState('');
  const [typoText] = useState('');
  const [autoCompleteList, setAutoCompleteList] = useState([]);
  const { transcript, listening, resetTranscript } = useSpeechRecognition();
  const autoCompleteRef = useRef();
  let navigate = useNavigate();

  const handleVoiceInput = () => {
    resetTranscript();
    SpeechRecognition.startListening({
      continuous: false,
      language: 'ru-RU'
    })
  } 

  const searchVideo = async () => {
    console.log('Отправка текста:', searchText);
    const response = await Service.getVideos(searchText);
    setVideos(response);
    navigate('/');
  }

  const handleSearchInputKeyDown = async (e) => {
    if(e.key === "Enter" && searchText.length > 0){
      searchVideo();
    }
  }

  const choiceWord = (text) => {
    setSearchText(text);
    setAutoCompleteList([]);
    searchVideo();
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
        <div className={cl.logo}>
          <Link to="/"><img src={logo} alt="Logo" /></Link>
        </div>
        <div className={cl.searchDiv}>
            <div className={cl.searchBox}>
              <SearchInput 
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)} 
              onKeyDown={handleSearchInputKeyDown}
              />
              {
                autoCompleteList.length > 0 && (
                  <div className={cl.autoComplete__container}>
                    <AutoComplete  ref={autoCompleteRef} autoCompleteList={autoCompleteList} onClick={choiceWord}/>
                  </div>
                )
              }
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