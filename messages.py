"""
Pesan-pesan bot dalam berbagai bahasa (Indonesia default)
"""

MESSAGES = {
    'welcome': {
        'id': """🎉 <b>Selamat Datang!</b>

Saya adalah bot downloader media sosial terbaik.

<b>📱 Didukung:</b> YouTube, Instagram, TikTok, Twitter, Facebook, Reddit, Pinterest

<b>🚀 Cara Pakai:</b>
Kirimkan link URL media yang ingin didownload.""",
        
        'en': """🎉 <b>Welcome!</b>

I'm the best social media downloader bot.

<b>📱 Supported:</b> YouTube, Instagram, TikTok, Twitter, Facebook, Reddit, Pinterest

<b>🚀 How to use:</b>
Send the URL of media you want to download."""
    },
    
    'error': {
        'id': "❌ Terjadi kesalahan. Silakan coba lagi.",
        'en': "❌ An error occurred. Please try again."
    },
    
    'downloading': {
        'id': "⏳ Sedang mendownload...",
        'en': "⏳ Downloading..."
    },
    
    'success': {
        'id': "✅ Berhasil didownload!",
        'en': "✅ Download successful!"
    }
}

def get_message(key: str, lang: str = 'id') -> str:
    """Ambil pesan berdasarkan kunci dan bahasa"""
    return MESSAGES.get(key, {}).get(lang, MESSAGES.get(key, {}).get('id', ''))