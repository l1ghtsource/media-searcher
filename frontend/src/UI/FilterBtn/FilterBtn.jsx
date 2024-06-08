import React, { useState } from 'react'
import cl from "./FilterBtn.module.css"

function FilterBtn({children}) {
  const [isActive, setIsActive] = useState(false);

  return (
    <div className={isActive ? `${cl.filterBtn} ${cl.active}` : cl.filterBtn} onClick={() => setIsActive(!isActive)}>{children}</div>
  )
}

export default FilterBtn