# 📥 MediaDown Bot

Bot Telegram untuk mendownload video, audio, dan gambar dari berbagai platform sosial media.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Fitur

- 📺 YouTube (Video, Shorts, Audio)
- 📸 Instagram (Reels, Post, Stories)
- 🎵 TikTok (Tanpa Watermark)
- 🐦 Twitter/X (Video & GIF)
- 📘 Facebook Video
- 🔴 Reddit
- 📌 Pinterest
- ☁️ SoundCloud

## 🚀 Cara Install

### 1. Clone Repository

```bash
git clone https://github.com/username/social-media-downloader-bot.git
cd social-media-downloader-bot
```

### 2. Setup Environment

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Install FFmpeg (Wajib):**

| OS | Perintah |
|---|---|
| Windows | Download [ffmpeg.org](https://ffmpeg.org/download.html), extract & tambahkan ke PATH |
| Ubuntu/Debian | `sudo apt-get install ffmpeg` |
| Mac | `brew install ffmpeg` |

### 4. Konfigurasi

Copy file `.env.example` dengan command
```bash
cp .env.example .env
```

Lalu edit file `.env`
```env
BOT_TOKEN=your_bot_token_here
BOT_USERNAME=your_bot_username
ADMIN_IDS=123456789
```

**Dapatkan Bot Token:**
1. Buka Telegram → cari [@BotFather](https://t.me/botfather)
2. Kirim `/newbot` → ikuti instruksi
3. Copy token ke file `.env`

### 5. Jalankan Bot

```bash
python3 bot.py
```

Bot siap digunakan! 🎉

## 📝 Perintah

| Command | Fungsi |
|---------|--------|
| `/start` | Memulai bot |
| `/help` | Bantuan penggunaan |
| `/about` | Tentang bot |
| `/stats` | Statistik (Admin) |

## 🛠️ Struktur File

```
├── bot.py           # File utama
├── config.py        # Konfigurasi
├── downloader.py    # Modul download
├── keyboards.py     # UI Tombol
├── utils.py         # Utility
├── requirements.txt # Dependencies
└── .env            # Environment variables
```

## ⚠️ Catatan

- Maksimal file: 50MB (limit Telegram)
- Durasi video: Maksimal 10 menit
- Pastikan link bersifat publik

## 📄 License

MIT License