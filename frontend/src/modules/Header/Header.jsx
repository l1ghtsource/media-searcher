import React, { useEffect, useState } from 'react'
import SpeechRecognition, {useSpeechRecognition} from 'react-speech-recognition'
import cl from "./Header.module.css"
import logo from "../../assets/svgIcons/logo.svg"
import SearchInput from '../../components/SearchInput/SearchInput'
import SearchVoice from '../../components/SearchVoice/SearchVoice'
import AddVideoBtn from '../../components/AddVideoBtn/AddVideoBtn'
import ProfileBtn from '../../components/ProfileBtn/ProfileBtn'

function Header() {
  const [searchText, setSearchText] = useState('');
  const { transcript, listening, resetTranscript } = useSpeechRecognition();

  const handleVoiceInput = () => {
    resetTranscript();
    SpeechRecognition.startListening({
      continuous: false,
      language: 'ru-RU'
    })
  }

  useEffect(() => {
    console.log('Распознанный текст:', transcript);
    setSearchText(transcript);
  }, [transcript]);

  useEffect(() => {
    console.log('Listening status:', listening);
  }, [listening]);

  return (
    <div className={cl.header}>
        <img src={logo} alt="Logo" />
        <div className={cl.searchDiv}>
            <SearchInput value={searchText} onChange={(e) => setSearchText(e.target.value)}/>
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