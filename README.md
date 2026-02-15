# CaesarAI Games

A modern desktop game management application built with React, Electron, and Supabase.

## Features

- Browse and search games from the CaesarAI Games API
- View detailed game information
- Launch games directly from the app
- Manage game settings (install folder, saved games folder)
- Backup saved games to the cloud
- Stream game content via torrents/magnets
- Beautiful dark-themed UI

## Tech Stack

- **Frontend**: React 19
- **Desktop Framework**: Electron
- **Database**: Supabase
- **Build Tool**: Vite
- **Styling**: CSS

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure Supabase:
   - Create a Supabase project at https://supabase.com
   - The database tables have been created automatically
   - Copy `.env.example` to `.env` and add your Supabase credentials:
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

3. Run in development mode:
```bash
npm run electron:dev
```

4. Build for production:
```bash
npm run electron:build
```

## Development

- `npm run dev` - Run Vite dev server only
- `npm run electron:dev` - Run full Electron app in dev mode
- `npm run build` - Build React app
- `npm run electron:build` - Build Electron app for distribution

## Project Structure

```
├── electron/           # Electron main process files
│   ├── main.js        # Main Electron process
│   └── preload.js     # Preload script for IPC
├── src/
│   ├── components/    # React components
│   ├── services/      # Supabase and API services
│   ├── App.jsx        # Main App component
│   └── main.jsx       # React entry point
└── imgs/              # Application icons and images
```

## Features in Detail

### Game Management
- View popular games, anime, and series
- Search for games by name
- View detailed information including cover art, description, and metadata

### Settings
- Configure game executable path
- Set install folder location
- Set saved games folder for backups

### Backup System
- Automatic cloud backup of saved games
- Backup status indicator
- Easy restore functionality

### Streaming
- Real-time WebSocket connection for torrent/magnet links
- View seeders and download status
- One-click access to streaming options

## License

ISC