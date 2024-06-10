import React from 'react'
import cl from "./FormInput.module.css"

function FormInput({placeholder}) {
  return (
    <div className={cl.formInput}>
        <input type="search" className={cl.formInput__input} placeholder={placeholder}/>
    </div>
  )
}

export default FormInput