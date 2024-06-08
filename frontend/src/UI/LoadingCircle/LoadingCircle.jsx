import React from 'react';
import cl from "./LoadingCircle.module.css";

function LoadingCircle() {
  return (
    <div className={cl.loadingCircle}>
        <svg fill="#00E2B8" height="64px" width="64px" version="1.1" id="Capa_1" viewBox="0 0 300.00 300.00" xmlSpace="preserve" stroke="#00E2B8" strokeWidth="0.003">
            <circle cx="150" cy="150" r="140" style={{fill: 'none'}} />
        </svg>
    </div>
  );
}

export default LoadingCircle;
