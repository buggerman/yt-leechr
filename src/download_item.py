"""
Download item model
"""

import uuid
from typing import Optional
from enum import Enum

class DownloadStatus(Enum):
    QUEUED = "queued"
    FETCHING_INFO = "fetching_info"
    DOWNLOADING = "downloading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    PAUSED = "paused"

class DownloadItem:
    def __init__(self, url: str):
        self.id = str(uuid.uuid4())
        self.url = url
        self.title = ""
        self.uploader = ""
        self.status = DownloadStatus.QUEUED
        self.progress = 0.0
        self.speed = 0
        self.total_bytes = 0
        self.downloaded_bytes = 0
        self.eta = None
        self.filepath = ""
        self.error_message = ""
        self.thumbnail_url = ""
        
    def update_info(self, title: str, uploader: str = "", thumbnail_url: str = ""):
        self.title = title
        self.uploader = uploader
        self.thumbnail_url = thumbnail_url
        
    def update_progress(self, progress_data: dict):
        if 'status' in progress_data:
            status_map = {
                'downloading': DownloadStatus.DOWNLOADING,
                'finished': DownloadStatus.COMPLETED,
                'error': DownloadStatus.ERROR,
                'paused': DownloadStatus.PAUSED
            }
            self.status = status_map.get(progress_data['status'], DownloadStatus.QUEUED)
            
        if 'downloaded_bytes' in progress_data:
            self.downloaded_bytes = progress_data['downloaded_bytes']
            
        if 'total_bytes' in progress_data:
            self.total_bytes = progress_data['total_bytes']
            
        if 'speed' in progress_data:
            self.speed = progress_data['speed'] or 0
            
        if 'eta' in progress_data:
            self.eta = progress_data['eta']
            
        # Calculate progress percentage
        if self.total_bytes > 0:
            self.progress = (self.downloaded_bytes / self.total_bytes) * 100
            
    def set_error(self, error_message: str):
        self.status = DownloadStatus.ERROR
        self.error_message = error_message
        
    def set_completed(self, filepath: str):
        self.status = DownloadStatus.COMPLETED
        self.filepath = filepath
        self.progress = 100.0