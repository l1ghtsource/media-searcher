import React from 'react'
import search from "../../assets/svgIcons/search.svg"
import cl from "./SearchInput.module.css"

function SearchInput({value, onChange, onKeyDown, onFocus, onBlur}) {
  return (
    <div className={cl.search}>
        <img src={search} alt="search" className={cl.searchImg}/>
        <input 
        type='search'
        className={cl.searchInput} 
        placeholder='Поиск' 
        value={value} 
        onChange={onChange} 
        onKeyDown={onKeyDown}
        onFocus={onFocus}
        onBlur={onBlur}/>
    </div>
  )
}

export default SearchInput