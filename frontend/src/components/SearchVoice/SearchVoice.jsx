import React from 'react';
import cl from './SearchVoice.module.css';
import microphone from '../../assets/svgIcons/microphone.svg';
import { useSpeechRecognition } from 'react-speech-recognition';

function SearchVoice({ onStart }) {
  const { listening } = useSpeechRecognition();

  const handleToggleListening = () => {
    onStart(); // Уведомить родительский компонент о начале распознавания
  };

  return (
    <div className={`${cl.searchVoice} ${listening ? cl.pulse : ''}`} onClick={handleToggleListening}>
      <img className={cl.microphoneIcon} src={microphone} alt="микрофон" />
    </div>
  );
}

export default SearchVoice;
