import React from 'react'
import cl from "./FilterBtn.module.css"

function FilterBtn({children, isActive, onClick}) {
  return (
    <div className={isActive ? `${cl.filterBtn} ${cl.active}` : cl.filterBtn} onClick={onClick}>{children}</div>
  )
}

export default FilterBtn