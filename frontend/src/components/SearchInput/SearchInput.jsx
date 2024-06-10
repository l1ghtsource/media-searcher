import React from 'react'
import search from "../../assets/svgIcons/search.svg"
import cl from "./SearchInput.module.css"

function SearchInput({value, onChange, onKeyDown}) {
  return (
    <div className={cl.search}>
        <img src={search} alt="search" className={cl.searchImg}/>
        <input type='search' className={cl.searchInput} placeholder='Поиск' value={value} onChange={onChange} onKeyDown={onKeyDown}/>
    </div>
  )
}

export default SearchInput