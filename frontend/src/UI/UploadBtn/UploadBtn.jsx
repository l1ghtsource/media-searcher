import React from 'react'
import cl from "./UploadBtn.module.css"

function UploadBtn({children, width, size, onClick, isDisabled}) {
  const rootClasses = [cl.uploadBtn];

  if(isDisabled){
    rootClasses.push(cl.disabled);
  }

  return (
    <div style={{ width: width, fontSize: size }} className={rootClasses.join(' ')} onClick={onClick}>
        {children}
    </div>
  )
}

export default UploadBtn