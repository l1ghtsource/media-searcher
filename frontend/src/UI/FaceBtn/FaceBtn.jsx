import React from 'react'
import cl from "./FaceBtn.module.css"

function FaceBtn({face, onClick, isActive}) {
  return (
    <div className={isActive ? `${cl.faceBtn} ${cl.active}` : cl.faceBtn} onClick={onClick}>
        <img src={face} alt="faceBtn" />
    </div>
  )
}

export default FaceBtn