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
                            # Find the downloaded file(s) and handle muxing if needed
                            output_path = self.get_output_path(info)
                            final_path = self.handle_post_download_muxing(output_path, info)
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
        
        # For video+audio downloads, let yt-dlp download separate files
        # We'll handle muxing ourselves in post-processing
        if not self.settings.get('extract_audio', False) and '+' in format_selector:
            # Don't merge - we'll handle it ourselves
            ydl_opts['keepvideo'] = True  # Keep both video and audio files
            # Remove any automatic merging to ensure we get separate files
            ydl_opts['postprocessors'] = []
        else:
            # For single format downloads, let yt-dlp handle normally
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
        
    def handle_post_download_muxing(self, expected_path: str, info: dict) -> str:
        """Handle muxing of separate video/audio files after download"""
        if not MUXING_AVAILABLE:
            return expected_path
            
        output_dir = os.path.dirname(expected_path)
        
        # Look for separate video and audio files using video title
        video_title = info.get('title', 'download')
        self.muxing_status.emit(self.download_item.id, "🔍 Checking for separate video/audio files...")
        video_file, audio_file = self.find_separate_files(output_dir, video_title)
        
        if video_file and audio_file:
            # We have separate files - need to mux them
            self.muxing_status.emit(self.download_item.id, f"📁 Found video: {os.path.basename(video_file)}")
            self.muxing_status.emit(self.download_item.id, f"🎵 Found audio: {os.path.basename(audio_file)}")
            
            base_name = os.path.splitext(os.path.basename(video_file))[0]
            # Remove common yt-dlp suffixes like .f137 from the base name
            import re
            base_name = re.sub(r'\.\w+$', '', base_name)
            
            self.muxing_status.emit(self.download_item.id, "🔧 Muxing video and audio files...")
            muxed_file = self.mux_files(video_file, audio_file, output_dir, base_name)
            if muxed_file:
                # Clean up separate files after successful muxing
                try:
                    os.remove(video_file)
                    os.remove(audio_file)
                    self.muxing_status.emit(self.download_item.id, f"✅ Successfully muxed to: {os.path.basename(muxed_file)}")
                except OSError:
                    pass  # Ignore cleanup errors
                return muxed_file
            else:
                # Muxing failed - emit a warning but continue with separate files
                self.muxing_status.emit(self.download_item.id, f"⚠️ Muxing failed - keeping separate files")
                self.muxing_status.emit(self.download_item.id, f"📹 Video: {os.path.basename(video_file)}")
                self.muxing_status.emit(self.download_item.id, f"🎵 Audio: {os.path.basename(audio_file)}")
                return video_file  # Return video file as primary
        else:
            self.muxing_status.emit(self.download_item.id, "ℹ️ Single file download - no muxing needed")
        
        # No separate files found, return expected path
        return expected_path
        
    def find_separate_files(self, output_dir: str, video_title: str) -> Tuple[Optional[str], Optional[str]]:
        """Find separate video and audio files in the output directory based on video title"""
        video_file = None
        audio_file = None
        
        # Clean the title like yt-dlp does for filename generation
        import re
        clean_title = re.sub(r'[<>:"/\\|?*]', '_', video_title)
        
        # Get all files in output directory sorted by modification time (newest first)
        try:
            all_files = []
            for file in os.listdir(output_dir):
                file_path = os.path.join(output_dir, file)
                if os.path.isfile(file_path):
                    mtime = os.path.getmtime(file_path)
                    all_files.append((file_path, file, mtime))
            
            # Sort by modification time, newest first
            all_files.sort(key=lambda x: x[2], reverse=True)
            
            # Look for video and audio files that contain the clean title
            for file_path, filename, _ in all_files:
                # Check if filename contains the clean title (or close match)
                if clean_title.lower() in filename.lower() or any(word in filename.lower() for word in clean_title.lower().split() if len(word) > 3):
                    file_ext = os.path.splitext(filename)[1].lower()
                    
                    # Identify video files (typically .mp4, but could be .webm)
                    if file_ext in ['.mp4', '.mkv', '.mov', '.avi'] and not video_file:
                        video_file = file_path
                    # Identify audio files (typically .webm with opus, .m4a)
                    elif file_ext in ['.webm', '.m4a', '.mp3', '.ogg', '.aac'] and not audio_file:
                        # For .webm files, prefer those that are likely audio-only
                        # (typically smaller than video files)
                        if file_ext == '.webm':
                            try:
                                size = os.path.getsize(file_path)
                                # If it's a small webm file, likely audio
                                if size < 50 * 1024 * 1024:  # Less than 50MB likely audio
                                    audio_file = file_path
                            except OSError:
                                pass
                        else:
                            audio_file = file_path
                
                # Stop searching once we found both
                if video_file and audio_file:
                    break
                    
        except OSError:
            pass
        
        return video_file, audio_file
        
    def mux_files(self, video_file: str, audio_file: str, output_dir: str, base_name: str) -> Optional[str]:
        """Mux video and audio files using available tools"""
        output_file = os.path.join(output_dir, f"{base_name}.mkv")
        
        # Try ffmpeg first (most likely to be available)
        if self.try_ffmpeg_mux(video_file, audio_file, output_file):
            return output_file
            
        # If ffmpeg fails, try mkvmerge (from mkvtoolnix)
        if self.try_mkvmerge_mux(video_file, audio_file, output_file):
            return output_file
            
        # If both fail, return None to indicate muxing failed
        return None
        
    def try_ffmpeg_mux(self, video_file: str, audio_file: str, output_file: str) -> bool:
        """Try to mux using ffmpeg"""
        if not MUXING_AVAILABLE:
            return False
            
        # Try different ffmpeg executable names and locations
        ffmpeg_names = ['ffmpeg', 'ffmpeg.exe']
        
        # Check for bundled ffmpeg first
        # Handle both PyInstaller bundle and source environments
        import sys
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in PyInstaller bundle
            bundle_dir = sys._MEIPASS
        else:
            # Running from source
            bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        bundled_ffmpeg = os.path.join(bundle_dir, 'tools', 'ffmpeg')
        if os.path.exists(bundled_ffmpeg):
            ffmpeg_names.insert(0, bundled_ffmpeg)
        elif os.path.exists(bundled_ffmpeg + '.exe'):
            ffmpeg_names.insert(0, bundled_ffmpeg + '.exe')
            
        for ffmpeg_cmd in ffmpeg_names:
            try:
                cmd = [
                    ffmpeg_cmd, '-i', video_file, '-i', audio_file,
                    '-c', 'copy',  # Copy streams without re-encoding
                    '-y',  # Overwrite output file
                    output_file
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    return True
                    
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
                
        return False
            
    def try_mkvmerge_mux(self, video_file: str, audio_file: str, output_file: str) -> bool:
        """Try to mux using mkvmerge from mkvtoolnix"""
        if not MUXING_AVAILABLE:
            return False
            
        # Try different mkvmerge executable names and locations
        mkvmerge_names = ['mkvmerge', 'mkvmerge.exe']
        
        # Check for bundled mkvmerge first
        # Handle both PyInstaller bundle and source environments
        import sys
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # Running in PyInstaller bundle
            bundle_dir = sys._MEIPASS
        else:
            # Running from source
            bundle_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        bundled_mkvmerge = os.path.join(bundle_dir, 'tools', 'mkvmerge')
        if os.path.exists(bundled_mkvmerge):
            mkvmerge_names.insert(0, bundled_mkvmerge)
        elif os.path.exists(bundled_mkvmerge + '.exe'):
            mkvmerge_names.insert(0, bundled_mkvmerge + '.exe')
            
        for mkvmerge_cmd in mkvmerge_names:
            try:
                cmd = [
                    mkvmerge_cmd, '-o', output_file,
                    video_file,  # Video track
                    audio_file   # Audio track
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    return True
                    
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
                
        return False
        
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