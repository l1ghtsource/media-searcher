import React from 'react'
import cl from "./FormInput.module.css"

function FormInput({placeholder, onChange, value}) {
  return (
    <div className={cl.formInput}>
        <input type="search" className={cl.formInput__input} placeholder={placeholder} onChange={onChange} value={value}/>
    </div>
  )
}

export default FormInput