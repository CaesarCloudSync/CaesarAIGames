/*
  # Create CaesarAI Games Tables

  1. New Tables
    - `settings`
      - `settings_id` (uuid, primary key)
      - `game_name` (text)
      - `game_exec` (text)
      - `install_folder` (text)
      - `saved_games_folder` (text)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)

    - `backup`
      - `backup_id` (uuid, primary key)
      - `game_name` (text)
      - `status` (text)
      - `created_at` (timestamptz)
      - `updated_at` (timestamptz)

  2. Security
    - Enable RLS on both tables
    - Add policies for public access (since this is a local desktop app)
*/

CREATE TABLE IF NOT EXISTS settings (
  settings_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  game_name text NOT NULL,
  game_exec text NOT NULL,
  install_folder text NOT NULL,
  saved_games_folder text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE settings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all operations on settings"
  ON settings
  FOR ALL
  USING (true)
  WITH CHECK (true);

CREATE TABLE IF NOT EXISTS backup (
  backup_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  game_name text NOT NULL,
  status text NOT NULL,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE backup ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all operations on backup"
  ON backup
  FOR ALL
  USING (true)
  WITH CHECK (true);

CREATE INDEX IF NOT EXISTS idx_settings_game_name ON settings(game_name);
CREATE INDEX IF NOT EXISTS idx_backup_game_name ON backup(game_name);
