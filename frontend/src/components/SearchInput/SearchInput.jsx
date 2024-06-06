import React from 'react'
import search from "../../assets/svgIcons/search.svg"
import cl from "./SearchInput.module.css"

function SearchInput({value, onChange}) {
  return (
    <div className={cl.search}>
        <img src={search} alt="search" className={cl.searchImg}/>
        <input className={cl.searchInput} placeholder='Поиск' value={value} onChange={onChange}/>
    </div>
  )
}

export default SearchInput