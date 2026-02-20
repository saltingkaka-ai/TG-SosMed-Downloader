"""
Modul Downloader untuk berbagai platform sosial media
"""

import os
import re
import yt_dlp
import aiohttp
import aiofiles
from typing import Dict, Optional, Tuple
import instaloader
import requests
from urllib.parse import urlparse

class MediaDownloader:
    def __init__(self):
        self.download_path = "downloads/"
        self.ensure_download_path()
        
    def ensure_download_path(self):
        """Memastikan folder download ada"""
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
    
    def detect_platform(self, url: str) -> Optional[str]:
        """Deteksi platform dari URL"""
        platforms = {
            'youtube': ['youtube.com', 'youtu.be'],
            'instagram': ['instagram.com', 'instagr.am'],
            'tiktok': ['tiktok.com', 'vt.tiktok.com'],
            'twitter': ['twitter.com', 'x.com', 't.co'],
            'facebook': ['facebook.com', 'fb.watch', 'fb.com'],
            'reddit': ['reddit.com', 'redd.it'],
            'pinterest': ['pinterest.com', 'pin.it'],
            'soundcloud': ['soundcloud.com'],
        }
        
        url_lower = url.lower()
        for platform, domains in platforms.items():
            if any(domain in url_lower for domain in domains):
                return platform
        return None
    
    async def get_info(self, url: str) -> Dict:
        """Mendapatkan informasi media"""
        platform = self.detect_platform(url)
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'platform': platform or 'unknown',
                    'thumbnail': info.get('thumbnail', ''),
                    'formats': len(info.get('formats', [])),
                    'filesize': info.get('filesize_approx', 0),
                    'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
                }
        except Exception as e:
            return {'error': str(e), 'platform': platform}
    
    async def download_video(self, url: str, quality: str = 'best', audio_only: bool = False) -> Tuple[str, Dict]:
        """
        Download video/audio dari URL
        
        Args:
            url: URL media
            quality: 'best', 'worst', atau resolusi spesifik
            audio_only: True untuk download audio saja
        
        Returns:
            Tuple (file_path, metadata)
        """
        platform = self.detect_platform(url)
        filename = f"{platform}_{hash(url) % 10000000}"
        
        if audio_only:
            filename += ".mp3"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{self.download_path}{filename}',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
            }
        else:
            if quality == 'hd':
                format_spec = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            elif quality == '720':
                format_spec = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            elif quality == '480':
                format_spec = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
            else:
                format_spec = 'best'
            
            filename += ".mp4"
            ydl_opts = {
                'format': format_spec,
                'outtmpl': f'{self.download_path}{filename}',
                'quiet': True,
                'no_warnings': True,
                'merge_output_format': 'mp4',
            }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = f"{self.download_path}{filename}"
                
                # Cek ukuran file
                file_size = os.path.getsize(file_path)
                
                metadata = {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'platform': platform,
                    'file_size': file_size,
                    'local_path': file_path,
                }
                
                return file_path, metadata
                
        except Exception as e:
            raise Exception(f"Download error: {str(e)}")
    
    async def download_instagram(self, url: str) -> Tuple[str, Dict]:
        """Download khusus Instagram menggunakan instaloader"""
        try:
            L = instaloader.Instaloader(
                dirname_pattern=self.download_path,
                filename_pattern=f'ig_{hash(url) % 10000000}',
                download_videos=True,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False,
                post_metadata_txt_pattern='',
            )
            
            # Extract shortcode dari URL
            shortcode = url.split('/p/')[-1].split('/')[0]
            if 'reel' in url:
                shortcode = url.split('/reel/')[-1].split('/')[0]
            
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            
            # Download
            L.download_post(post, target=self.download_path)
            
            # Cari file yang didownload
            files = os.listdir(self.download_path)
            target_file = None
            
            for file in files:
                if file.startswith(f'ig_{hash(url) % 10000000}') and (file.endswith('.mp4') or file.endswith('.jpg')):
                    target_file = os.path.join(self.download_path, file)
                    break
            
            if not target_file:
                raise Exception("File tidak ditemukan setelah download")
            
            metadata = {
                'title': post.caption[:100] if post.caption else 'Instagram Post',
                'uploader': post.owner_username,
                'platform': 'instagram',
                'likes': post.likes,
                'file_size': os.path.getsize(target_file),
                'local_path': target_file,
            }
            
            return target_file, metadata
            
        except Exception as e:
            # Fallback ke yt-dlp jika instaloader gagal
            return await self.download_video(url)
    
    async def download_tiktok(self, url: str, watermark: bool = False) -> Tuple[str, Dict]:
        """Download TikTok (tanpa watermark jika memungkinkan)"""
        # Gunakan yt-dlp dengan opsi khusus TikTok
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{self.download_path}tiktok_{hash(url) % 10000000}.%(ext)s',
            'quiet': True,
            'no_warnings': True,
            'cookiesfrombrowser': None,  # Bisa ditambahkan cookies jika perlu
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
                
                metadata = {
                    'title': info.get('description', 'TikTok Video')[:100],
                    'uploader': info.get('uploader', 'Unknown'),
                    'platform': 'tiktok',
                    'views': info.get('view_count', 0),
                    'likes': info.get('like_count', 0),
                    'file_size': os.path.getsize(file_path),
                    'local_path': file_path,
                }
                
                return file_path, metadata
                
        except Exception as e:
            raise Exception(f"TikTok download error: {str(e)}")
    
    def cleanup(self, file_path: str):
        """Membersihkan file setelah dikirim"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleanup: {e}")