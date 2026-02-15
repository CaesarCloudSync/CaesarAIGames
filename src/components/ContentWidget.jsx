import React, { useState, useEffect, useRef, useCallback } from 'react';
import ItemCard from './ItemCard';
import './ContentWidget.css';

function ContentWidget({ endpoint, searchQuery = '', onItemClick, onBack, imageCache, setImageCache }) {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const scrollRef = useRef(null);

  const loadItems = useCallback(async () => {
    if (loading || !hasMore) return;

    setLoading(true);
    try {
      const url = `https://games.caesaraihub.org/${endpoint}?offset=${page * 20}&limit=20${searchQuery ? `&game=${searchQuery}` : ''}`;
      const response = await fetch(url);
      const data = await response.json();
      const newItems = data.games || [];

      if (newItems.length === 0) {
        setHasMore(false);
      } else {
        setItems((prev) => [...prev, ...newItems]);
        setPage((prev) => prev + 1);
      }
    } catch (error) {
      console.error('Failed to load items:', error);
    } finally {
      setLoading(false);
    }
  }, [endpoint, searchQuery, page, loading, hasMore]);

  useEffect(() => {
    setItems([]);
    setPage(0);
    setHasMore(true);
    loadItems();
  }, [endpoint, searchQuery]);

  const handleScroll = (e) => {
    const { scrollTop, scrollHeight, clientHeight } = e.target;
    if (scrollHeight - scrollTop <= clientHeight + 200 && !loading && hasMore) {
      loadItems();
    }
  };

  const renderRows = () => {
    const rows = [];
    for (let i = 0; i < items.length; i += 5) {
      const rowItems = items.slice(i, i + 5);
      rows.push(
        <div key={i} className="item-row">
          {rowItems.map((item, idx) => (
            <ItemCard
              key={`${item.id}-${idx}`}
              item={item}
              imageCache={imageCache}
              setImageCache={setImageCache}
              onClick={() => onItemClick(item)}
            />
          ))}
        </div>
      );
    }
    return rows;
  };

  return (
    <div className="content-widget">
      {onBack && (
        <button className="back-button" onClick={onBack}>
          Back
        </button>
      )}
      <div className="scroll-area" ref={scrollRef} onScroll={handleScroll}>
        <div className="items-container">
          {renderRows()}
          {loading && <div className="loading">Loading...</div>}
        </div>
      </div>
    </div>
  );
}

export default ContentWidget;
