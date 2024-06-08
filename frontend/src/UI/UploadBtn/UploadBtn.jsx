import React from 'react'
import cl from "./UploadBtn.module.css"

function UploadBtn({children, width, size, onClick}) {
  return (
    <div style={{ width: width, fontSize: size }} className={cl.uploadBtn} onClick={onClick}>
        {children}
    </div>
  )
}

export default UploadBtn