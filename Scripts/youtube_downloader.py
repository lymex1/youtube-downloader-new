import yt_dlp
import os
from yt_dlp import YoutubeDL
from django.conf import settings


def download_youtube_video(url: str, output_path: str, cookie_file_path: str):    
    edit_arr = output_path.split('&')
    output_path = edit_arr[0]
    
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]',  # видео 1080p + аудио
        'outtmpl': output_path,
        'cookiefile': cookie_file_path,
        'merge_output_format': 'mp4',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

