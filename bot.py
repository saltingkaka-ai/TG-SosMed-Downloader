"""
🤖 Social Media Downloader Bot untuk Telegram
Bot canggih untuk mendownload video, audio, dan gambar dari berbagai platform
"""

import os
import asyncio
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

from config import (
    BOT_TOKEN, WELCOME_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE,
    ADMIN_IDS, MAX_FILE_SIZE, SUPPORTED_PLATFORMS
)
from keyboards import (
    get_main_keyboard, get_platform_keyboard, get_download_options_keyboard,
    get_quality_keyboard, get_cancel_keyboard, get_admin_keyboard,
    get_close_keyboard
)
from downloader import MediaDownloader
from utils import (
    ensure_directories, format_size, format_duration, is_valid_url,
    truncate_text, get_platform_icon, StatsManager, logger
)

# Inisialisasi
downloader = MediaDownloader()
stats_manager = StatsManager()

# Banner URL (ganti dengan URL banner Anda atau gunakan local)
BANNER_URL = "https://via.placeholder.com/800x300/0088cc/ffffff?text=📥+MediaDown+Bot"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler command /start"""
    user = update.effective_user
    stats_manager.add_user(user.id)
    
    # Kirim banner
    try:
        await update.message.reply_photo(
            photo=BANNER_URL,
            caption=f"Halo {user.first_name}! 👋\n\n" + WELCOME_MESSAGE,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    except:
        # Fallback jika banner gagal
        await update.message.reply_text(
            f"Halo {user.first_name}! 👋\n\n" + WELCOME_MESSAGE,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler command /help"""
    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler command /about"""
    downloads, users = stats_manager.get_stats()
    
    about_text = ABOUT_MESSAGE.format(
        total_downloads=downloads,
        total_users=users
    )
    
    await update.message.reply_text(
        about_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler command /stats (Admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Anda tidak memiliki akses!")
        return
    
    downloads, users = stats_manager.get_stats()
    
    stats_text = f"""
<b>📊 Statistik Bot</b>

👥 Total Users: {users}
📥 Total Downloads: {downloads}
📱 Platform Aktif: {len(SUPPORTED_PLATFORMS)}

<b>🖥️ Server Status:</b>
✅ Bot Online
✅ Download Service: Active
✅ Database: Connected
    """
    
    await update.message.reply_text(
        stats_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_admin_keyboard()
    )

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk URL yang dikirim user"""
    url = update.message.text.strip()
    user = update.effective_user
    
    # Validasi URL
    if not is_valid_url(url):
        await update.message.reply_text(
            "❌ <b>URL tidak valid!</b>\n\n"
            "Pastikan Anda mengirimkan link yang benar.\n"
            "Contoh: https://youtube.com/watch?v=...",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Deteksi platform
    platform = downloader.detect_platform(url)
    
    if not platform:
        await update.message.reply_text(
            "❌ <b>Platform tidak didukung!</b>\n\n"
            "Bot mendukung: YouTube, Instagram, TikTok, Twitter, Facebook, Reddit, Pinterest, SoundCloud",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Kirim pesan processing
    processing_msg = await update.message.reply_text(
        f"{get_platform_icon(platform)} <b>Mendeteksi link {platform.title()}...</b>\n"
        "⏳ Mohon tunggu sebentar...",
        parse_mode=ParseMode.HTML
    )
    
    try:
        # Ambil info media
        info = await downloader.get_info(url)
        
        if 'error' in info:
            await processing_msg.edit_text(
                f"❌ <b>Error:</b> {info['error']}",
                parse_mode=ParseMode.HTML
            )
            return
        
        # Format pesan info
        info_text = f"""
<b>{get_platform_icon(platform)} {platform.title()} Media Detected</b>

📝 <b>Judul:</b> {truncate_text(info['title'], 50)}
👤 <b>Uploader:</b> {info['uploader']}
⏱ <b>Durasi:</b> {format_duration(info['duration'])}
📦 <b>Ukuran:</b> {format_size(info['filesize']) if info['filesize'] else 'Unknown'}

<b>Pilih opsi download:</b>
        """
        
        await processing_msg.edit_text(
            info_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_download_options_keyboard(url, platform)
        )
        
    except Exception as e:
        logger.error(f"Error processing URL: {e}")
        await processing_msg.edit_text(
            f"❌ <b>Terjadi kesalahan:</b>\n<code>{str(e)}</code>",
            parse_mode=ParseMode.HTML
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk callback buttons"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == 'download_menu':
        await query.edit_message_text(
            "<b>📱 Pilih Platform:</b>\n\n"
            "Pilih platform sosial media yang ingin Anda download:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_platform_keyboard()
        )
    
    elif data == 'help':
        await query.edit_message_text(
            HELP_MESSAGE,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    
    elif data == 'about':
        downloads, users = stats_manager.get_stats()
        await query.edit_message_text(
            ABOUT_MESSAGE.format(total_downloads=downloads, total_users=users),
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    
    elif data == 'back_main':
        await query.edit_message_text(
            WELCOME_MESSAGE,
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    
    elif data.startswith('platform_'):
        platform = data.replace('platform_', '')
        await query.edit_message_text(
            f"<b>{get_platform_icon(platform)} {platform.title()}</b>\n\n"
            f"Kirimkan link {platform.title()} yang ingin didownload.\n\n"
            f"Contoh format URL yang didukung...",
            parse_mode=ParseMode.HTML,
            reply_markup=get_cancel_keyboard()
        )
    
    elif data.startswith('dl_video|'):
        url = data.split('|', 1)[1]
        await process_download(query, context, url, 'video')
    
    elif data.startswith('dl_audio|'):
        url = data.split('|', 1)[1]
        await process_download(query, context, url, 'audio')
    
    elif data.startswith('dl_hd|'):
        url = data.split('|', 1)[1]
        await process_download(query, context, url, 'hd')
    
    elif data.startswith('info|'):
        url = data.split('|', 1)[1]
        await show_media_info(query, url)
    
    elif data == 'cancel':
        await query.edit_message_text(
            "❌ <b>Dibatalkan</b>\n\n"
            "Kirimkan URL baru untuk memulai download.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )
    
    elif data == 'close':
        await query.delete_message()

async def process_download(query, context, url: str, download_type: str):
    """Proses download dan kirim file"""
    platform = downloader.detect_platform(url)
    
    # Update pesan
    await query.edit_message_text(
        f"⏳ <b>Sedang mendownload...</b>\n\n"
        f"📱 Platform: {platform.title()}\n"
        f"📦 Tipe: {download_type.upper()}\n\n"
        f"Mohon tunggu, ini mungkin memerlukan waktu beberapa menit...",
        parse_mode=ParseMode.HTML
    )
    
    try:
        # Download berdasarkan tipe
        if platform == 'instagram':
            file_path, metadata = await downloader.download_instagram(url)
        elif platform == 'tiktok':
            file_path, metadata = await downloader.download_tiktok(url)
        else:
            if download_type == 'audio':
                file_path, metadata = await downloader.download_video(url, audio_only=True)
            elif download_type == 'hd':
                file_path, metadata = await downloader.download_video(url, quality='hd')
            else:
                file_path, metadata = await downloader.download_video(url)
        
        # Cek ukuran file
        file_size = os.path.getsize(file_path)
        
        if file_size > MAX_FILE_SIZE:
            await query.edit_message_text(
                f"❌ <b>File terlalu besar!</b>\n\n"
                f"Ukuran: {format_size(file_size)}\n"
                f"Maksimal: {format_size(MAX_FILE_SIZE)}\n\n"
                f"Coba download versi dengan kualitas lebih rendah.",
                parse_mode=ParseMode.HTML
            )
            downloader.cleanup(file_path)
            return
        
        # Update status
        await query.edit_message_text(
            f"📤 <b>Mengupload file...</b>\n\n"
            f"📁 {truncate_text(metadata['title'], 30)}\n"
            f"📦 {format_size(file_size)}",
            parse_mode=ParseMode.HTML
        )
        
        # Kirim file
        chat_id = query.message.chat_id
        
        caption = f"""
<b>✅ Download Berhasil!</b>

📝 {truncate_text(metadata['title'], 100)}
👤 {metadata['uploader']}
📱 {platform.title()}
📦 {format_size(file_size)}

<b>🤖 @{(await context.bot.get_me()).username}</b>
        """
        
        if download_type == 'audio' or file_path.endswith('.mp3'):
            with open(file_path, 'rb') as audio:
                await context.bot.send_audio(
                    chat_id=chat_id,
                    audio=audio,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    title=metadata['title'],
                    performer=metadata['uploader']
                )
        else:
            with open(file_path, 'rb') as video:
                await context.bot.send_video(
                    chat_id=chat_id,
                    video=video,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    supports_streaming=True
                )
        
        # Hapus pesan processing
        await query.delete_message()
        
        # Update statistik
        stats_manager.add_download()
        
        # Cleanup
        downloader.cleanup(file_path)
        
    except Exception as e:
        logger.error(f"Download error: {e}")
        await query.edit_message_text(
            f"❌ <b>Gagal mendownload!</b>\n\n"
            f"<code>{str(e)}</code>\n\n"
            f"Coba lagi atau hubungi support.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_main_keyboard()
        )

async def show_media_info(query, url: str):
    """Tampilkan informasi detail media"""
    try:
        info = await downloader.get_info(url)
        platform = downloader.detect_platform(url)
        
        info_text = f"""
<b>{get_platform_icon(platform)} Informasi Media</b>

📝 <b>Judul:</b> 
{info['title']}

👤 <b>Channel/Uploader:</b> {info['uploader']}
⏱ <b>Durasi:</b> {format_duration(info['duration'])}
📦 <b>Ukuran Perkiraan:</b> {format_size(info['filesize']) if info['filesize'] else 'Unknown'}
🎬 <b>Format Tersedia:</b> {info['formats']} format

📝 <b>Deskripsi:</b>
{info.get('description', 'Tidak ada deskripsi')[:300]}...
        """
        
        await query.edit_message_text(
            info_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_download_options_keyboard(url, platform)
        )
        
    except Exception as e:
        await query.edit_message_text(
            f"❌ Error: {str(e)}",
            parse_mode=ParseMode.HTML
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk error"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ <b>Terjadi kesalahan!</b>\n\n"
            "Silakan coba lagi atau hubungi admin.",
            parse_mode=ParseMode.HTML
        )

def main():
    """Fungsi utama untuk menjalankan bot"""
    # Setup direktori
    ensure_directories()
    
    # Buat application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Tambah handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Handler untuk URL
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))
    
    # Handler untuk buttons
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Jalankan bot
    print("🤖 Bot sedang berjalan...")
    print("Tekan Ctrl+C untuk menghentikan")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()