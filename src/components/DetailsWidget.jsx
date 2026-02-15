import React, { useState, useEffect } from 'react';
import SettingsDialog from './SettingsDialog';
import { supabase } from '../services/supabase';
import './DetailsWidget.css';

function DetailsWidget({ item, imageCache, onBack }) {
  const [imageUrl, setImageUrl] = useState(null);
  const [streams, setStreams] = useState([]);
  const [showSettings, setShowSettings] = useState(false);
  const [isBackedUp, setIsBackedUp] = useState(false);
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const cover = item.cover;
    if (cover?.image_id) {
      const posterPath = `/${cover.image_id}.jpg`;
      if (imageCache[posterPath]) {
        setImageUrl(imageCache[posterPath]);
      } else {
        const url = `https://images.igdb.com/igdb/image/upload/t_cover_big${posterPath}`;
        setImageUrl(url);
      }
    }

    checkBackupStatus();
    startStreaming();

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [item]);

  const checkBackupStatus = async () => {
    try {
      const { data } = await supabase
        .from('backup')
        .select('*')
        .eq('game_name', item.name)
        .maybeSingle();

      setIsBackedUp(!!data);
    } catch (error) {
      console.error('Error checking backup status:', error);
    }
  };

  const startStreaming = () => {
    const websocket = new WebSocket('wss://movies.caesaraihub.org/api/v1/stream_get_gamews');

    websocket.onopen = () => {
      websocket.send(JSON.stringify({ title: item.name }));
    };

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const gamesData = data?.event?.games?.data?.games || [];
        if (gamesData.length > 0) {
          setStreams((prev) => [...prev, ...gamesData]);
        }
      } catch (error) {
        console.error('WebSocket message error:', error);
      }
    };

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    setWs(websocket);
  };

  const handlePlayGame = async () => {
    try {
      const { data } = await supabase
        .from('settings')
        .select('*')
        .eq('game_name', item.name)
        .maybeSingle();

      if (data?.game_exec) {
        await window.electronAPI.launchGame(data.game_exec);
      } else {
        alert('Please configure game settings first');
        setShowSettings(true);
      }
    } catch (error) {
      console.error('Error launching game:', error);
      alert('Failed to launch game');
    }
  };

  const handleBackup = async () => {
    try {
      const { data: settings } = await supabase
        .from('settings')
        .select('*')
        .eq('game_name', item.name)
        .maybeSingle();

      if (!settings?.saved_games_folder) {
        alert('Please configure saved games folder first');
        setShowSettings(true);
        return;
      }

      await supabase.from('backup').upsert({
        game_name: item.name,
        status: 'success'
      });

      setIsBackedUp(true);
      alert('Backup completed successfully!');
    } catch (error) {
      console.error('Error backing up:', error);
      alert('Backup failed');
    }
  };

  const handleStreamClick = (stream) => {
    if (stream.magnet_link) {
      window.open(stream.magnet_link, '_blank');
    } else if (stream.guid) {
      window.open(stream.guid, '_blank');
    }
  };

  return (
    <div className="details-widget">
      <button className="back-button" onClick={onBack}>
        Back
      </button>

      <div className="details-scroll">
        <div className="details-content">
          <h1 className="details-title">{item.name}</h1>

          {imageUrl && (
            <div className="details-poster">
              <img src={imageUrl} alt={item.name} />
            </div>
          )}

          {item.summary && (
            <p className="details-description">{item.summary}</p>
          )}

          <div className="details-actions">
            <button className="play-button" onClick={handlePlayGame}>
              <img src="/imgs/play.png" alt="Play" />
              Play
            </button>

            <button className="icon-button" onClick={handleBackup}>
              <img
                src={isBackedUp ? '/imgs/cloud.png' : '/imgs/cloud_backup.png'}
                alt="Backup"
              />
            </button>

            <button className="icon-button">
              <img src="/imgs/not_saved.png" alt="Library" />
            </button>

            <div style={{ flex: 1 }} />

            <button className="icon-button" onClick={() => setShowSettings(true)}>
              <img src="/imgs/settings.png" alt="Settings" />
            </button>
          </div>

          {streams.length > 0 && (
            <div className="streams-section">
              <h2>Streaming Options</h2>
              <div className="streams-list">
                {streams.slice(0, 60).map((stream, idx) => (
                  <div
                    key={idx}
                    className="stream-item"
                    onClick={() => handleStreamClick(stream)}
                  >
                    <span>{stream.title || 'Unknown'}</span>
                    {stream.seeders && <span className="seeders">Seeders: {stream.seeders}</span>}
                    <img src="/imgs/world-wide-web.png" alt="Open" className="stream-icon" />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {showSettings && (
        <SettingsDialog
          item={item}
          onClose={() => setShowSettings(false)}
        />
      )}
    </div>
  );
}

export default DetailsWidget;
