"""
Utility functions
"""

import os
import logging
from datetime import datetime
from typing import Optional
import humanize

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def ensure_directories():
    """Memastikan semua direktori penting ada"""
    dirs = ['downloads', 'logs', 'assets']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

def format_size(size_bytes: int) -> str:
    """Format ukuran file menjadi human readable"""
    return humanize.naturalsize(size_bytes)

def format_duration(seconds: int) -> str:
    """Format durasi detik menjadi mm:ss atau hh:mm:ss"""
    if seconds < 3600:
        return f"{seconds // 60}:{seconds % 60:02d}"
    else:
        return f"{seconds // 3600}:{(seconds % 3600) // 60:02d}:{seconds % 60:02d}"

def is_valid_url(url: str) -> bool:
    """Validasi apakah string adalah URL"""
    import re
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return bool(url_pattern.match(url))

def truncate_text(text: str, max_length: int = 100) -> str:
    """Memotong teks jika terlalu panjang"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_platform_icon(platform: str) -> str:
    """Mendapatkan icon untuk platform"""
    icons = {
        'youtube': '📺',
        'instagram': '📸',
        'tiktok': '🎵',
        'twitter': '🐦',
        'facebook': '📘',
        'reddit': '🔴',
        'pinterest': '📌',
        'soundcloud': '☁️',
        'spotify': '🎧',
    }
    return icons.get(platform, '🔗')

class StatsManager:
    """Manajemen statistik bot"""
    
    def __init__(self):
        self.stats_file = 'logs/stats.txt'
        self.ensure_file()
    
    def ensure_file(self):
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w') as f:
                f.write("0\n0")  # total_downloads, total_users
    
    def add_download(self):
        """Menambah counter download"""
        downloads, users = self.get_stats()
        with open(self.stats_file, 'w') as f:
            f.write(f"{downloads + 1}\n{users}")
    
    def add_user(self, user_id: int):
        """Menambah user unik"""
        # Simpan user ID di file terpisah
        users_file = 'logs/users.txt'
        users = set()
        
        if os.path.exists(users_file):
            with open(users_file, 'r') as f:
                users = set(f.read().splitlines())
        
        if str(user_id) not in users:
            users.add(str(user_id))
            with open(users_file, 'w') as f:
                f.write('\n'.join(users))
            
            downloads, _ = self.get_stats()
            with open(self.stats_file, 'w') as f:
                f.write(f"{downloads}\n{len(users)}")
    
    def get_stats(self) -> tuple:
        """Mendapatkan statistik"""
        try:
            with open(self.stats_file, 'r') as f:
                lines = f.read().splitlines()
                return int(lines[0]), int(lines[1])
        except:
            return 0, 0