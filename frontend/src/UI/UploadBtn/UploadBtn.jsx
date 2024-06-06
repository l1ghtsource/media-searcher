import React from 'react'
import cl from "./UploadBtn.module.css"

function UploadBtn({children, width, onClick}) {
  return (
    <div style={{ width: width }} className={cl.uploadBtn} onClick={onClick}>
        {children}
    </div>
  )
}

export default UploadBtn