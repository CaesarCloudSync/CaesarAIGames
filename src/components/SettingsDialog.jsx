import React, { useState, useEffect } from 'react';
import { supabase } from '../services/supabase';
import './SettingsDialog.css';

function SettingsDialog({ item, onClose }) {
  const [gameExec, setGameExec] = useState('Not set');
  const [installFolder, setInstallFolder] = useState('Not set');
  const [savedGamesFolder, setSavedGamesFolder] = useState('Not set');

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const { data } = await supabase
        .from('settings')
        .select('*')
        .eq('game_name', item.name)
        .maybeSingle();

      if (data) {
        setGameExec(data.game_exec || 'Not set');
        setInstallFolder(data.install_folder || 'Not set');
        setSavedGamesFolder(data.saved_games_folder || 'Not set');
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  };

  const saveSettings = async () => {
    try {
      await supabase.from('settings').upsert({
        game_name: item.name,
        game_exec: gameExec,
        install_folder: installFolder,
        saved_games_folder: savedGamesFolder
      });
      alert('Settings saved successfully!');
    } catch (error) {
      console.error('Error saving settings:', error);
      alert('Failed to save settings');
    }
  };

  const handleSelectGameExec = async () => {
    const path = await window.electronAPI.selectFile();
    if (path) {
      setGameExec(path);
    }
  };

  const handleSelectInstallFolder = async () => {
    const path = await window.electronAPI.selectFolder();
    if (path) {
      setInstallFolder(path);
    }
  };

  const handleSelectSavedGamesFolder = async () => {
    const path = await window.electronAPI.selectFolder();
    if (path) {
      setSavedGamesFolder(path);
    }
  };

  return (
    <div className="settings-dialog-overlay" onClick={onClose}>
      <div className="settings-dialog" onClick={(e) => e.stopPropagation()}>
        <h2>Settings - {item.name}</h2>

        <div className="settings-row">
          <label>Game Executable:</label>
          <div className="settings-value">{gameExec}</div>
          <button onClick={handleSelectGameExec}>Select File</button>
        </div>

        <div className="settings-row">
          <label>Install Folder:</label>
          <div className="settings-value">{installFolder}</div>
          <button onClick={handleSelectInstallFolder}>Select Folder</button>
        </div>

        <div className="settings-row">
          <label>Saved Games Folder:</label>
          <div className="settings-value">{savedGamesFolder}</div>
          <button onClick={handleSelectSavedGamesFolder}>Select Folder</button>
        </div>

        <div className="settings-actions">
          <button className="save-button" onClick={saveSettings}>
            Save
          </button>
          <button className="cancel-button" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

export default SettingsDialog;
