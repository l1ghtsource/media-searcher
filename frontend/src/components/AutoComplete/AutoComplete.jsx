import React from 'react'
import cl from "./AutoComplete.module.css"

function AutoComplete({autoCompleteList, onClick}) {
  return (
    <div className={cl.autoComplete}>
        <ul className={cl.autoComplete__list}>
            {
                autoCompleteList.map((text, index) => (
                    <li 
                      key={index} 
                      className={cl.autoComplete__option}
                      onClick={() => onClick(text)} 
                    >{text}</li>
                ))
            }
        </ul>
    </div>
  )
}

export default AutoComplete