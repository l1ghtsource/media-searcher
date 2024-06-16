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
import BackBtn from "../../UI/BackBtn/BackBtn"

function Header({setVideos}) {
  const [searchText, setSearchText] = useState('');
  const [typoText] = useState('');
  const [autoCompleteList, setAutoCompleteList] = useState(['машина', 'машина xiaomi', 'маша и медведь']);
  const { transcript, resetTranscript } = useSpeechRecognition();
  const autoCompleteRef = useRef();
  const searchInputRef = useRef();
  const [isFocus, setIsFocus] = useState(false);
  const [isListening, setIsListening] = useState(false);

  let navigate = useNavigate();

  const handleVoiceInput = () => {
    if (isListening) {
      SpeechRecognition.stopListening(); // Остановка прослушивания
      setIsListening(false);
      resetTranscript(); // Сброс распознанного текста
    } else {
      resetTranscript();
      SpeechRecognition.startListening({
        continuous: false,
        language: 'ru-RU',
      });
      setIsListening(true);
    }
  } 

  const searchVideo = async (text) => {
    const response = await Service.getVideos(text);
    setVideos(response);
    navigate('/');
  }

  const handleSearchInputKeyDown = async (e) => {
    if(e.key === "Enter" && searchText.length > 0){
      searchVideo(searchText);
      searchInputRef.current.blur();
    }
  }

  const choiceWord = async (text) => {
    searchVideo(text);
    setSearchText(text);
    setAutoCompleteList([]);
  }

  useEffect(() => {
    if(transcript !== undefined){
      setSearchText(transcript);
    }
  }, [transcript]);

  return (
    <div className={isFocus ? `${cl.header} ${cl.focus}` : cl.header}>
        <div className={cl.logo}>
          <Link to="/"><img src={logo} alt="Logo" /></Link>
        </div>
        <div className={cl.searchDiv}>
            <div className={cl.searchBox}>
              <SearchInput 
              ref={searchInputRef}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)} 
              onKeyDown={handleSearchInputKeyDown}
              onFocus={() => setIsFocus(true)}
              onBlur={() => setIsFocus(false)}
              />
              {
                autoCompleteList.length > 0 && isFocus && (
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
            <div className={cl.searchVoice}>
              <SearchVoice onStart={handleVoiceInput}/>
            </div>
        </div>
        <div className={cl.rightHeader}>
            <AddVideoBtn/>
            <ProfileBtn/>
        </div>
        {/* {
          typoText && (
            <div className={cl.typo__mobile}>
              <div className={cl.typoMobile__text}>Показаны результаты по запросу <span>{typoText}</span></div>
              <div className={cl.typoMobile__btn}>Отмена</div>
            </div>
          )
        } */}
        {
          isFocus && (
            <div className={cl.backBtn}>
              <BackBtn>Назад</BackBtn>
            </div>
          )
        }
    </div>
  )
}

export default Header