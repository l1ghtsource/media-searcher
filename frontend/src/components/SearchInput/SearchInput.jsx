import React from 'react'
import search from "../../assets/svgIcons/search.svg"
import cl from "./SearchInput.module.css"

function SearchInput() {
  return (
    <div className={cl.search}>
        <img src={search} alt="search" className={cl.searchImg}/>
        <input className={cl.searchInput} placeholder='Поиск'/>
    </div>
  )
}

export default SearchInput