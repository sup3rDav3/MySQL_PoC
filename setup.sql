-- Run this as MySQL root to set up the PoC database and user
CREATE DATABASE IF NOT EXISTS poc_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'poc_user'@'localhost' IDENTIFIED BY 'poc_password';
GRANT ALL PRIVILEGES ON poc_db.* TO 'poc_user'@'localhost';
FLUSH PRIVILEGES;

-- The `entries` table is created automatically by app.py on startup,
-- but you can also create it manually:
USE poc_db;
CREATE TABLE IF NOT EXISTS entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
