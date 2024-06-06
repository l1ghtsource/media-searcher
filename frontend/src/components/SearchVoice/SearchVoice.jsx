import React from 'react'
import cl from "./SearchVoice.module.css"
import microphone from "../../assets/svgIcons/microphone.svg"

function SearchVoice() {
  return (
    <div className={cl.searchVoice}>
        <img src={microphone} alt="microphone" />
    </div>
  )
}

export default SearchVoice