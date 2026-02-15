import React, { useState } from 'react';
import TitleBar from './components/TitleBar';
import LeftNav from './components/LeftNav';
import TopNav from './components/TopNav';
import ContentNav from './components/ContentNav';
import ContentStack from './components/ContentStack';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [searchQuery, setSearchQuery] = useState('');
  const [showNavigation, setShowNavigation] = useState(true);
  const [selectedItem, setSelectedItem] = useState(null);
  const [imageCache, setImageCache] = useState({});

  const handleNavigation = (view) => {
    setCurrentView(view);
    setShowNavigation(true);
    setSelectedItem(null);
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    setCurrentView('search');
    setShowNavigation(false);
  };

  const handleItemClick = (item) => {
    setSelectedItem(item);
    setCurrentView('details');
    setShowNavigation(false);
  };

  const handleBack = () => {
    setCurrentView('home');
    setShowNavigation(true);
    setSelectedItem(null);
  };

  return (
    <div className="app">
      <TitleBar />
      <div className="main-container">
        <LeftNav
          currentView={currentView}
          onNavigate={handleNavigation}
          showButtons={showNavigation}
        />
        <div className="content-area">
          <TopNav
            onSearch={handleSearch}
            showSearch={showNavigation}
          />
          {showNavigation && ['home', 'anime', 'series'].includes(currentView) && (
            <ContentNav
              currentView={currentView}
              onNavigate={handleNavigation}
            />
          )}
          <ContentStack
            currentView={currentView}
            searchQuery={searchQuery}
            selectedItem={selectedItem}
            onItemClick={handleItemClick}
            onBack={handleBack}
            imageCache={imageCache}
            setImageCache={setImageCache}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
