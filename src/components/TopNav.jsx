import React, { useState } from 'react';
import './TopNav.css';

function TopNav({ onSearch, showSearch }) {
  const [searchValue, setSearchValue] = useState('');
  const [isFullscreen, setIsFullscreen] = useState(false);

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchValue.trim()) {
      onSearch(searchValue.trim());
    }
  };

  const handleFullscreen = () => {
    window.electronAPI?.windowFullscreen();
    setIsFullscreen(!isFullscreen);
  };

  return (
    <div className="top-nav">
      {showSearch && (
        <div className="search-container">
          <img src="/imgs/search_icon.png" alt="Search" className="search-icon" />
          <form onSubmit={handleSearch}>
            <input
              type="text"
              className="search-input"
              placeholder="Search..."
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
            />
          </form>
        </div>
      )}
      <button className="fullscreen-button" onClick={handleFullscreen}>
        <img
          src={isFullscreen ? '/imgs/fullscreen_exit.png' : '/imgs/fullscreen.png'}
          alt="Fullscreen"
        />
      </button>
    </div>
  );
}

export default TopNav;
