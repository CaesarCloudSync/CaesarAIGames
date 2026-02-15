import React from 'react';
import './TitleBar.css';

function TitleBar() {
  const handleMinimize = () => {
    window.electronAPI?.windowMinimize();
  };

  const handleMaximize = () => {
    window.electronAPI?.windowMaximize();
  };

  const handleClose = () => {
    window.electronAPI?.windowClose();
  };

  return (
    <div className="title-bar">
      <div className="title-bar-content">
        <img src="/imgs/CaesarAIMoviesLogo.png" alt="Logo" className="title-logo" />
        <span className="title-text">CaesarAI Games</span>
        <div className="title-bar-buttons">
          <button className="title-bar-button" onClick={handleMinimize}>
            🗕
          </button>
          <button className="title-bar-button" onClick={handleMaximize}>
            🗖
          </button>
          <button className="title-bar-button close-button" onClick={handleClose}>
            🗙
          </button>
        </div>
      </div>
    </div>
  );
}

export default TitleBar;
