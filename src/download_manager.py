"""
Download manager handling yt-dlp integration
"""

import os
import threading
import queue
from typing import Dict, Any, Optional, List, Tuple
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QTimer
import yt_dlp
from .download_item import DownloadItem, DownloadStatus

# Optional imports for muxing functionality
try:
    import subprocess
    import glob
    import shutil
    MUXING_AVAILABLE = True
except ImportError:
    MUXING_AVAILABLE = False

class DownloadWorker(QThread):
    progress_updated = pyqtSignal(str, dict)
    info_extracted = pyqtSignal(str, str, str)
    download_completed = pyqtSignal(str, str)
    download_error = pyqtSignal(str, str)
    muxing_status = pyqtSignal(str, str)  # download_id, status message
    
    def __init__(self, download_item: DownloadItem, settings: Dict[str, Any]):
        super().__init__()
        self.download_item = download_item
        self.settings = settings
        self.is_paused = False
        self.is_cancelled = False
        
    def run(self):
        try:
            # Configure yt-dlp options
            ydl_opts = self.build_ydl_options()
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract info first
                self.progress_updated.emit(self.download_item.id, {'status': 'fetching_info'})
                
                try:
                    info = ydl.extract_info(self.download_item.url, download=False)
                    if info:
                        title = info.get('title', 'Unknown')
                        uploader = info.get('uploader', 'Unknown')
                        thumbnail = info.get('thumbnail', '')
                        
                        self.download_item.update_info(title, uploader, thumbnail)
                        self.info_extracted.emit(self.download_item.id, title, uploader)
                        
                except Exception as e:
                    self.download_error.emit(self.download_item.id, f"Info extraction failed: {str(e)}")
                    return
                
                # Download the video
                if not self.is_cancelled:
                    self.progress_updated.emit(self.download_item.id, {'status': 'downloading'})
                    try:
                        ydl.download([self.download_item.url])
                        
                        if not self.is_cancelled:
                            # If separate files were downloaded, mux them
                            output_path = self.get_output_path(info)
                            final_path = self.mux_if_needed(output_path, info)
                            self.download_completed.emit(self.download_item.id, final_path)
                            
                    except Exception as e:
                        if not self.is_cancelled:
                            self.download_error.emit(self.download_item.id, f"Download failed: {str(e)}")
                            
        except Exception as e:
            self.download_error.emit(self.download_item.id, f"Unexpected error: {str(e)}")
            
    def build_ydl_options(self) -> Dict[str, Any]:
        output_dir = self.settings.get('output_dir', os.path.expanduser('~/Downloads'))
        output_template = self.settings.get('output_template', '%(title)s.%(ext)s')
        format_selector = self.settings.get('format', 'best')
        
        # Get bundled ffmpeg path
        ffmpeg_path = self.get_bundled_ffmpeg_path()
        print(f"DEBUG: ffmpeg_path = {ffmpeg_path}")
        print(f"DEBUG: format_selector = {format_selector}")
        
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, output_template),
            'format': format_selector,
            'progress_hooks': [self.progress_hook],
            'noplaylist': not self.settings.get('download_playlist', False),
            'ignoreerrors': True,
            'no_warnings': False,
            'extractaudio': self.settings.get('extract_audio', False),
            'audioformat': self.settings.get('audio_format', 'mp3'),
            'audioquality': self.settings.get('audio_quality', '192'),
        }
        
        # Force ffmpeg usage and set location
        if ffmpeg_path:
            ydl_opts['ffmpeg_location'] = ffmpeg_path
            # Also add to PATH for yt-dlp to find
            import os
            current_path = os.environ.get('PATH', '')
            tools_dir = os.path.dirname(ffmpeg_path)
            if tools_dir not in current_path:
                os.environ['PATH'] = tools_dir + os.pathsep + current_path
            
        # For video downloads, force merging
        if not self.settings.get('extract_audio', False) and '+' in format_selector:
            ydl_opts['merge_output_format'] = 'mkv'
            ydl_opts['prefer_ffmpeg'] = True
            # Force post-processing to ensure merge happens
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mkv',
            }]
        else:
            # Even for single format, prefer ffmpeg if available
            if ffmpeg_path:
                ydl_opts['prefer_ffmpeg'] = True
        
        # Add subtitle options
        if self.settings.get('download_subtitles', False):
            ydl_opts['writesubtitles'] = True
            ydl_opts['writeautomaticsub'] = True
            subtitle_langs = self.settings.get('subtitle_languages', 'en')
            ydl_opts['subtitleslangs'] = subtitle_langs.split(',')
            
        # Add thumbnail option
        if self.settings.get('write_thumbnail', False):
            ydl_opts['writethumbnail'] = True
            
        # Add metadata options
        if self.settings.get('add_metadata', False):
            ydl_opts['addmetadata'] = True
            
        return ydl_opts
        
    def get_bundled_ffmpeg_path(self) -> Optional[str]:
        """Get the path to bundled ffmpeg executable"""
        import sys
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in PyInstaller bundle
            bundle_dir = sys._MEIPASS
        else:
            # Running from source
            bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        # Check for ffmpeg
        ffmpeg_paths = [
            os.path.join(bundle_dir, 'tools', 'ffmpeg'),
            os.path.join(bundle_dir, 'tools', 'ffmpeg.exe')
        ]
        
        for path in ffmpeg_paths:
            if os.path.exists(path) and os.access(path, os.X_OK):
                return path
                
        return None
        
    def progress_hook(self, d):
        if self.is_cancelled:
            return
            
        progress_data = {
            'status': d.get('status', 'downloading'),
            'downloaded_bytes': d.get('downloaded_bytes', 0),
            'total_bytes': d.get('total_bytes', 0),
            'speed': d.get('speed', 0),
            'eta': d.get('eta', None),
        }
        
        # Calculate percentage
        if d.get('total_bytes'):
            progress_data['percent'] = (d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)) * 100
        elif d.get('downloaded_bytes') and d.get('total_bytes_estimate'):
            progress_data['percent'] = (d.get('downloaded_bytes', 0) / d.get('total_bytes_estimate', 1)) * 100
        else:
            progress_data['percent'] = 0
            
        self.progress_updated.emit(self.download_item.id, progress_data)
        
    def get_output_path(self, info: dict) -> str:
        output_dir = self.settings.get('output_dir', os.path.expanduser('~/Downloads'))
        template = self.settings.get('output_template', '%(title)s.%(ext)s')
        
        # This is a simplified approach - in a real implementation,
        # you'd want to use yt-dlp's filename generation
        title = info.get('title', 'download')
        ext = info.get('ext', 'mp4')
        
        # Clean the title for filename
        import re
        clean_title = re.sub(r'[<>:"/\\|?*]', '_', title)
        filename = f"{clean_title}.{ext}"
        
        return os.path.join(output_dir, filename)
        
    def mux_if_needed(self, expected_path: str, info: dict) -> str:
        """Simple muxing check - look for separate video/audio files and mux them"""
        output_dir = os.path.dirname(expected_path)
        video_title = info.get('title', 'download')
        
        # Clean title for filename matching
        import re
        clean_title = re.sub(r'[<>:"/\\|?*]', '_', video_title)
        
        # Find most recent video and audio files matching the title
        video_file = None
        audio_file = None
        
        try:
            for file in os.listdir(output_dir):
                if clean_title.lower() in file.lower():
                    file_path = os.path.join(output_dir, file)
                    if file.endswith('.mp4') and not video_file:
                        video_file = file_path
                    elif file.endswith('.webm') and not audio_file:
                        audio_file = file_path
        except OSError:
            return expected_path
            
        # If we have both video and audio, mux them
        if video_file and audio_file:
            muxed_path = os.path.join(output_dir, f"{clean_title}.mkv")
            if self.simple_mux(video_file, audio_file, muxed_path):
                # Clean up original files
                try:
                    os.remove(video_file)
                    os.remove(audio_file)
                except OSError:
                    pass
                return muxed_path
            
        return expected_path
        
    def simple_mux(self, video_file: str, audio_file: str, output_file: str) -> bool:
        """Simple muxing using mkvmerge or ffmpeg"""
        import subprocess
        
        # Get muxing tools
        mkvmerge_path = self.get_muxing_tool()
        if not mkvmerge_path:
            return False
            
        try:
            # Use mkvmerge-style command
            cmd = [mkvmerge_path, '-o', output_file, video_file, audio_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.returncode == 0
        except Exception:
            return False
            
    def get_muxing_tool(self) -> Optional[str]:
        """Get path to muxing tool (mkvmerge wrapper or ffmpeg)"""
        import sys
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        # Check for bundled mkvmerge first, platform-specific
        import platform
        if platform.system() == 'Windows':
            muxing_tools = [
                os.path.join(bundle_dir, 'tools', 'mkvmerge.bat'),
                os.path.join(bundle_dir, 'tools', 'ffmpeg.exe')
            ]
        else:
            muxing_tools = [
                os.path.join(bundle_dir, 'tools', 'mkvmerge'),
                os.path.join(bundle_dir, 'tools', 'ffmpeg')
            ]
        
        for tool in muxing_tools:
            if os.path.exists(tool):
                # On Windows, don't check execute permissions for .bat files
                if tool.endswith('.bat') or os.access(tool, os.X_OK):
                    return tool
                
        return None
        
    def pause(self):
        self.is_paused = True
        
    def resume(self):
        self.is_paused = False
        
    def cancel(self):
        self.is_cancelled = True
        self.quit()
        self.wait()

class DownloadManager(QObject):
    download_progress = pyqtSignal(str, dict)
    download_completed = pyqtSignal(str, str)
    download_error = pyqtSignal(str, str)
    info_extracted = pyqtSignal(str, str, str)
    
    def __init__(self):
        super().__init__()
        self.active_downloads: Dict[str, DownloadWorker] = {}
        self.max_concurrent_downloads = 3
        self.download_queue = queue.Queue()
        
    def add_download(self, download_item: DownloadItem, settings: Dict[str, Any]):
        if len(self.active_downloads) < self.max_concurrent_downloads:
            self.start_download(download_item, settings)
        else:
            self.download_queue.put((download_item, settings))
            
    def start_download(self, download_item: DownloadItem, settings: Dict[str, Any]):
        worker = DownloadWorker(download_item, settings)
        
        # Connect signals
        worker.progress_updated.connect(self.on_progress_updated)
        worker.info_extracted.connect(self.on_info_extracted)
        worker.download_completed.connect(self.on_download_completed)
        worker.download_error.connect(self.on_download_error)
        worker.finished.connect(lambda: self.worker_finished(download_item.id))
        
        self.active_downloads[download_item.id] = worker
        worker.start()
        
    def on_progress_updated(self, download_id: str, progress: dict):
        self.download_progress.emit(download_id, progress)
        
    def on_info_extracted(self, download_id: str, title: str, uploader: str):
        self.info_extracted.emit(download_id, title, uploader)
        
    def on_download_completed(self, download_id: str, filepath: str):
        self.download_completed.emit(download_id, filepath)
        
    def on_download_error(self, download_id: str, error: str):
        self.download_error.emit(download_id, error)
        
    def worker_finished(self, download_id: str):
        if download_id in self.active_downloads:
            del self.active_downloads[download_id]
            
        # Start next download from queue
        if not self.download_queue.empty():
            try:
                download_item, settings = self.download_queue.get_nowait()
                self.start_download(download_item, settings)
            except queue.Empty:
                pass
                
    def pause_download(self, download_id: str):
        if download_id in self.active_downloads:
            self.active_downloads[download_id].pause()
            
    def resume_download(self, download_id: str):
        if download_id in self.active_downloads:
            self.active_downloads[download_id].resume()
            
    def cancel_download(self, download_id: str):
        if download_id in self.active_downloads:
            self.active_downloads[download_id].cancel()
            
    def pause_all(self):
        for worker in self.active_downloads.values():
            worker.pause()
            
    def resume_all(self):
        for worker in self.active_downloads.values():
            worker.resume()
            
    def clear_all(self):
        # Cancel all active downloads
        for worker in self.active_downloads.values():
            worker.cancel()
            
        self.active_downloads.clear()
        
        # Clear the queue
        while not self.download_queue.empty():
            try:
                self.download_queue.get_nowait()
            except queue.Empty:
                break
                
    def cleanup(self):
        self.clear_all()