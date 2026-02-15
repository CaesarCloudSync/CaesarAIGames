import React, { useState, useEffect } from 'react';
import './ItemCard.css';

function ItemCard({ item, imageCache, setImageCache, onClick }) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageUrl, setImageUrl] = useState(null);

  useEffect(() => {
    const cover = item.cover;
    if (cover?.image_id) {
      const posterPath = `/${cover.image_id}.jpg`;
      if (imageCache[posterPath]) {
        setImageUrl(imageCache[posterPath]);
        setImageLoaded(true);
      } else {
        const url = `https://images.igdb.com/igdb/image/upload/t_cover_big${posterPath}`;
        setImageUrl(url);
        setImageCache((prev) => ({ ...prev, [posterPath]: url }));
        setImageLoaded(true);
      }
    }
  }, [item, imageCache, setImageCache]);

  const title = item.name || 'Unknown';

  return (
    <div className="item-card" onClick={onClick}>
      <div className="poster-frame">
        {imageLoaded && imageUrl ? (
          <img src={imageUrl} alt={title} className="poster-image" />
        ) : (
          <div className="poster-placeholder">No Image</div>
        )}
      </div>
      <div className="item-title">{title}</div>
    </div>
  );
}

export default ItemCard;
