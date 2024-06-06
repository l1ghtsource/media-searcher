import React from 'react'
import cl from "./ProfileBtn.module.css"
import profile from "../../assets/svgIcons/profileIcon.svg"

function ProfileBtn() {
  return (
    <div className={cl.profileBtn}>
        <img src={profile} alt="profileIcon" />
    </div>
  )
}

export default ProfileBtn