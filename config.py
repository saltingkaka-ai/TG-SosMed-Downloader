"""
Konfigurasi Bot Telegram Downloader
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
BOT_USERNAME = os.getenv('BOT_USERNAME', 'your_bot_username')

# Admin Configuration
ADMIN_IDS = list(map(int, os.getenv('ADMIN_IDS', '123456789').split(',')))

# Download Configuration
DOWNLOAD_PATH = "downloads/"
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (Telegram limit)
MAX_VIDEO_DURATION = 600  # 10 menit

# Supported Platforms
SUPPORTED_PLATFORMS = {
    'youtube': ['youtube.com', 'youtu.be'],
    'instagram': ['instagram.com', 'instagr.am'],
    'tiktok': ['tiktok.com', 'vt.tiktok.com'],
    'twitter': ['twitter.com', 'x.com', 't.co'],
    'facebook': ['facebook.com', 'fb.watch', 'fb.com'],
    'reddit': ['reddit.com', 'redd.it'],
    'pinterest': ['pinterest.com', 'pin.it'],
    'soundcloud': ['soundcloud.com'],
    'spotify': ['spotify.com', 'open.spotify.com'],
}

# Messages
WELCOME_MESSAGE = """
🎉 <b>Selamat Datang di MediaDown Bot!</b>

Saya adalah bot canggih untuk mendownload media dari berbagai platform sosial media.

<b>📱 Platform yang Didukung:</b>
• YouTube (Video & Shorts)
• Instagram (Reels, Post, Stories)
• TikTok (Video & Slide)
• Twitter/X (Video & GIF)
• Facebook (Video)
• Reddit (Video & GIF)
• Pinterest (Video & Gambar)
• SoundCloud (Audio)
• Spotify (Track info)

<b>🚀 Cara Penggunaan:</b>
1. Kirimkan link URL media yang ingin didownload
2. Tunggu proses download
3. Bot akan mengirimkan media ke chat Anda

<b>⚡ Fitur:</b>
✅ Kualitas HD
✅ Audio terpisah (opsional)
✅ Metadata lengkap
✅ Cepat & Mudah

Ketik /help untuk bantuan lebih lanjut.
"""

HELP_MESSAGE = """
<b>📖 Panduan Penggunaan</b>

<b>🎯 Perintah Dasar:</b>
/start - Memulai bot
/help - Bantuan penggunaan
/about - Tentang bot
/stats - Statistik bot (Admin)
/broadcast - Broadcast pesan (Admin)

<b>🔗 Format URL yang Didukung:</b>
• YouTube: youtube.com/watch?v=... atau youtu.be/...
• Instagram: instagram.com/p/... atau instagram.com/reel/...
• TikTok: tiktok.com/@user/video/... atau vt.tiktok.com/...
• Twitter: twitter.com/username/status/... atau x.com/...
• Facebook: facebook.com/watch?v=... atau fb.watch/...
• Reddit: reddit.com/r/.../comments/...
• Pinterest: pinterest.com/pin/... atau pin.it/...

<b>💡 Tips:</b>
• Pastikan link URL valid dan publik
• Untuk Instagram, gunakan link post/reel publik
• Video private tidak dapat didownload
• Maksimal ukuran file: 50MB

<b>⚠️ Batasan:</b>
• Durasi video maksimal: 10 menit
• Ukuran file maksimal: 50MB
• Beberapa konten premium mungkin tidak tersedia

Jika ada masalah, hubungi admin.
"""

ABOUT_MESSAGE = """
<b>ℹ️ Tentang MediaDown Bot</b>

<b>🤖 Versi:</b> 2.0.0
<b>👨‍💻 Developer:</b> @your_username
<b>📅 Update:</b> 2024

<b>🛠️ Teknologi:</b>
• Python 3.11
• python-telegram-bot
• yt-dlp
• aiohttp

<b>📊 Statistik:</b>
• Platform: 8+
• Total Download: {total_downloads}
• Users: {total_users}

<b>📞 Support:</b>
Hubungi @your_username untuk bantuan

<b>⭐ Rate Bot:</b>
Jika suka dengan bot ini, bagikan ke temanmu!
"""

# Keyboard Buttons
BUTTONS = {
    'download_video': '📹 Download Video',
    'download_audio': '🎵 Download Audio',
    'download_hd': '🎬 Download HD',
    'info': 'ℹ️ Info Media',
    'back': '🔙 Kembali',
    'cancel': '❌ Batal',
    'help': '❓ Bantuan',
    'about': 'ℹ️ Tentang',
    'stats': '📊 Statistik',
    'support': '💬 Support',
    'close': '❌ Tutup',
}