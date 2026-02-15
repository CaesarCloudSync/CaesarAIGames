import React from 'react';
import './LeftNav.css';

function LeftNav({ currentView, onNavigate, showButtons }) {
  const navItems = [
    { id: 'home', icon: '/imgs/home.png', label: 'Home' },
    { id: 'discover', icon: '/imgs/discover.png', label: 'Discover' },
    { id: 'library', icon: '/imgs/gallery.png', label: 'Library' },
    { id: 'calendar', icon: '/imgs/calendar.png', label: 'Calendar' }
  ];

  return (
    <div className="left-nav">
      <img src="/imgs/CaesarAIMoviesLogo.png" alt="Logo" className="nav-logo" />
      {showButtons && (
        <div className="nav-buttons">
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`nav-button ${currentView === item.id ? 'active' : ''}`}
              onClick={() => onNavigate(item.id)}
              title={item.label}
            >
              <img src={item.icon} alt={item.label} />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default LeftNav;
