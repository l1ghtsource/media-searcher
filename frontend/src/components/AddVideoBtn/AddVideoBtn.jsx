import React from 'react'
import cl from "./AddVideoBtn.module.css"
import plus from "../../assets/svgIcons/plus.svg"
import { Link } from 'react-router-dom'
function AddVideoBtn() {
  return (
    <div className={cl.addVideoBtn}>
      <Link to="/newVideo">
        <img src={plus} alt="addVideo" />
      </Link>
    </div>
  )
}

export default AddVideoBtn