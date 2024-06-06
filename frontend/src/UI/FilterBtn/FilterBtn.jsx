import React from 'react'
import cl from "./FilterBtn.module.css"

function FilterBtn({children}) {
  return (
    <div className={cl.filterBtn}>{children}</div>
  )
}

export default FilterBtn