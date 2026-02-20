"""
Custom Keyboards untuk Bot
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    """Keyboard utama"""
    keyboard = [
        [
            InlineKeyboardButton("📥 Download", callback_data='download_menu'),
            InlineKeyboardButton("❓ Bantuan", callback_data='help')
        ],
        [
            InlineKeyboardButton("ℹ️ Tentang", callback_data='about'),
            InlineKeyboardButton("💬 Support", url='https://t.me/your_username')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_platform_keyboard():
    """Keyboard pemilihan platform"""
    keyboard = [
        [
            InlineKeyboardButton("📺 YouTube", callback_data='platform_youtube'),
            InlineKeyboardButton("📸 Instagram", callback_data='platform_instagram')
        ],
        [
            InlineKeyboardButton("🎵 TikTok", callback_data='platform_tiktok'),
            InlineKeyboardButton("🐦 Twitter/X", callback_data='platform_twitter')
        ],
        [
            InlineKeyboardButton("📘 Facebook", callback_data='platform_facebook'),
            InlineKeyboardButton("🔴 Reddit", callback_data='platform_reddit')
        ],
        [
            InlineKeyboardButton("📌 Pinterest", callback_data='platform_pinterest'),
            InlineKeyboardButton("🎧 SoundCloud", callback_data='platform_soundcloud')
        ],
        [
            InlineKeyboardButton("🔙 Kembali", callback_data='back_main')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_download_options_keyboard(url, platform):
    """Keyboard opsi download"""
    keyboard = [
        [
            InlineKeyboardButton("📹 Video", callback_data=f'dl_video|{url}'),
            InlineKeyboardButton("🎵 Audio", callback_data=f'dl_audio|{url}')
        ],
        [
            InlineKeyboardButton("🎬 HD Quality", callback_data=f'dl_hd|{url}'),
            InlineKeyboardButton("ℹ️ Info", callback_data=f'info|{url}')
        ],
        [
            InlineKeyboardButton("❌ Batal", callback_data='cancel')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_quality_keyboard(url):
    """Keyboard pilihan kualitas"""
    keyboard = [
        [
            InlineKeyboardButton("🥇 1080p", callback_data=f'quality_1080|{url}'),
            InlineKeyboardButton("🥈 720p", callback_data=f'quality_720|{url}')
        ],
        [
            InlineKeyboardButton("🥉 480p", callback_data=f'quality_480|{url}'),
            InlineKeyboardButton("📱 360p", callback_data=f'quality_360|{url}')
        ],
        [
            InlineKeyboardButton("🔙 Kembali", callback_data='back_options')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_cancel_keyboard():
    """Keyboard cancel"""
    keyboard = [[InlineKeyboardButton("❌ Batal", callback_data='cancel')]]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard():
    """Keyboard admin panel"""
    keyboard = [
        [
            InlineKeyboardButton("📊 Statistik", callback_data='admin_stats'),
            InlineKeyboardButton("📢 Broadcast", callback_data='admin_broadcast')
        ],
        [
            InlineKeyboardButton("📝 Log", callback_data='admin_logs'),
            InlineKeyboardButton("⚙️ Pengaturan", callback_data='admin_settings')
        ],
        [
            InlineKeyboardButton("❌ Tutup", callback_data='close')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_close_keyboard():
    """Keyboard tutup"""
    keyboard = [[InlineKeyboardButton("❌ Tutup", callback_data='close')]]
    return InlineKeyboardMarkup(keyboard)