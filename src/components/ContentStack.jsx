import React from 'react';
import ContentWidget from './ContentWidget';
import DetailsWidget from './DetailsWidget';
import './ContentStack.css';

function ContentStack({ currentView, searchQuery, selectedItem, onItemClick, onBack, imageCache, setImageCache }) {
  const renderView = () => {
    switch (currentView) {
      case 'home':
        return (
          <ContentWidget
            endpoint="api/v1/popular_games"
            onItemClick={onItemClick}
            imageCache={imageCache}
            setImageCache={setImageCache}
          />
        );
      case 'anime':
        return (
          <ContentWidget
            endpoint="discover/tv?with_genres=16&with_keywords=210024|287501&first_air_date.gte=2015-03-10"
            onItemClick={onItemClick}
            imageCache={imageCache}
            setImageCache={setImageCache}
          />
        );
      case 'series':
        return (
          <ContentWidget
            endpoint="tv/top_rated"
            onItemClick={onItemClick}
            imageCache={imageCache}
            setImageCache={setImageCache}
          />
        );
      case 'search':
        return (
          <ContentWidget
            endpoint="api/v1/search_game"
            searchQuery={searchQuery}
            onItemClick={onItemClick}
            onBack={onBack}
            imageCache={imageCache}
            setImageCache={setImageCache}
          />
        );
      case 'details':
        return (
          <DetailsWidget
            item={selectedItem}
            imageCache={imageCache}
            onBack={onBack}
          />
        );
      case 'discover':
        return <PlaceholderView title="Discover" />;
      case 'library':
        return <PlaceholderView title="Library" />;
      case 'calendar':
        return <PlaceholderView title="Calendar" />;
      default:
        return <PlaceholderView title="Home" />;
    }
  };

  return <div className="content-stack">{renderView()}</div>;
}

function PlaceholderView({ title }) {
  return (
    <div className="placeholder-view">
      <h1>{title} Widget</h1>
    </div>
  );
}

export default ContentStack;
