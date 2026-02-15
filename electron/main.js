const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { exec } = require('child_process');
const fs = require('fs');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1900,
    height: 1080,
    minWidth: 1280,
    minHeight: 720,
    frame: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
    icon: path.join(__dirname, '../imgs/CaesarAIMoviesLogo.png')
  });

  const isDev = !app.isPackaged;

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../build/index.html'));
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

ipcMain.handle('window-minimize', () => {
  mainWindow.minimize();
});

ipcMain.handle('window-maximize', () => {
  if (mainWindow.isMaximized()) {
    mainWindow.unmaximize();
  } else {
    mainWindow.maximize();
  }
});

ipcMain.handle('window-close', () => {
  mainWindow.close();
});

ipcMain.handle('window-fullscreen', () => {
  mainWindow.setFullScreen(!mainWindow.isFullScreen());
});

ipcMain.handle('select-folder', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory']
  });
  return result.filePaths[0] || null;
});

ipcMain.handle('select-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    filters: [
      { name: 'Executables', extensions: ['exe'] }
    ]
  });
  return result.filePaths[0] || null;
});

ipcMain.handle('launch-game', async (event, execPath) => {
  return new Promise((resolve, reject) => {
    if (!fs.existsSync(execPath)) {
      reject(new Error('Executable not found'));
      return;
    }

    exec(`"${execPath}"`, (error) => {
      if (error) {
        reject(error);
      } else {
        resolve({ success: true });
      }
    });
  });
});

ipcMain.handle('get-process-info', async (event, execPath) => {
  const basename = path.basename(execPath);
  return new Promise((resolve) => {
    const isWindows = process.platform === 'win32';
    const command = isWindows
      ? `tasklist /FI "IMAGENAME eq ${basename}" /FO CSV /NH`
      : `ps aux | grep "${basename}"`;

    exec(command, (error, stdout) => {
      if (error || !stdout) {
        resolve({ running: false });
      } else {
        resolve({ running: true, output: stdout });
      }
    });
  });
});
