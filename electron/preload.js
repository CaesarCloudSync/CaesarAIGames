const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  windowMinimize: () => ipcRenderer.invoke('window-minimize'),
  windowMaximize: () => ipcRenderer.invoke('window-maximize'),
  windowClose: () => ipcRenderer.invoke('window-close'),
  windowFullscreen: () => ipcRenderer.invoke('window-fullscreen'),
  selectFolder: () => ipcRenderer.invoke('select-folder'),
  selectFile: () => ipcRenderer.invoke('select-file'),
  launchGame: (execPath) => ipcRenderer.invoke('launch-game', execPath),
  getProcessInfo: (execPath) => ipcRenderer.invoke('get-process-info', execPath)
});
