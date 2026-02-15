import React from 'react';
import './ContentNav.css';

function ContentNav({ currentView, onNavigate }) {
  const tabs = [
    { id: 'home', label: 'Movies' },
    { id: 'anime', label: 'Anime' },
    { id: 'series', label: 'Series' }
  ];

  return (
    <div className="content-nav">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`content-nav-button ${currentView === tab.id ? 'active' : ''}`}
          onClick={() => onNavigate(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

export default ContentNav;
