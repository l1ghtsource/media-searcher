import React from 'react'
import cl from "./Header.module.css"
import logo from "../../assets/svgIcons/logo.svg"
import SearchInput from '../../components/SearchInput/SearchInput'
import SearchVoice from '../../components/SearchVoice/SearchVoice'
import AddVideoBtn from '../../components/AddVideoBtn/AddVideoBtn'
import ProfileBtn from '../../components/ProfileBtn/ProfileBtn'

function Header() {
  return (
    <div className={cl.header}>
        <img src={logo} alt="Logo" />
        <div className={cl.searchDiv}>
            <SearchInput/>
            <SearchVoice/>
        </div>
        <div className={cl.rightHeader}>
            <AddVideoBtn/>
            <ProfileBtn/>
        </div>
    </div>
  )
}

export default Header