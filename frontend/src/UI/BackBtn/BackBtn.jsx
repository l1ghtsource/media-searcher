import React from 'react'
import cl from "./BackBtn.module.css"
import back from "../../assets/svgIcons/back.svg"
import { Link } from "react-router-dom"

function BackBtn({children}) {
  return (
    <Link to="/">
      <div className={cl.backBtn}>  
        <img src={back} alt="backBtn" />
        <div className={cl.backBtn__text}>{children}</div>
      </div>
    </Link>
  )
}

export default BackBtn