"""
Tests for download_item module
"""

import pytest
from src.download_item import DownloadItem, DownloadStatus

@pytest.mark.unit
class TestDownloadItem:
    def test_init(self):
        """Test DownloadItem initialization"""
        url = "https://www.youtube.com/watch?v=test"
        item = DownloadItem(url)
        
        assert item.url == url
        assert item.title == ""
        assert item.uploader == ""
        assert item.status == DownloadStatus.QUEUED
        assert item.progress == 0.0
        assert item.speed == 0
        assert item.total_bytes == 0
        assert item.downloaded_bytes == 0
        assert item.eta is None
        assert item.filepath == ""
        assert item.error_message == ""
        assert item.thumbnail_url == ""
        assert item.id is not None
        assert len(item.id) > 0
        
    def test_update_info(self):
        """Test updating video info"""
        item = DownloadItem("https://example.com/video")
        
        title = "Test Video"
        uploader = "Test Channel"
        thumbnail = "https://example.com/thumb.jpg"
        
        item.update_info(title, uploader, thumbnail)
        
        assert item.title == title
        assert item.uploader == uploader
        assert item.thumbnail_url == thumbnail
        
    def test_update_progress(self, sample_progress_data):
        """Test updating download progress"""
        item = DownloadItem("https://example.com/video")
        
        item.update_progress(sample_progress_data)
        
        assert item.status == DownloadStatus.DOWNLOADING
        assert item.downloaded_bytes == sample_progress_data['downloaded_bytes']
        assert item.total_bytes == sample_progress_data['total_bytes']
        assert item.speed == sample_progress_data['speed']
        assert item.eta == sample_progress_data['eta']
        assert item.progress == 10.0  # (1024000 / 10240000) * 100
        
    def test_update_progress_status_mapping(self):
        """Test status mapping in progress updates"""
        item = DownloadItem("https://example.com/video")
        
        # Test different status mappings
        test_cases = [
            ('downloading', DownloadStatus.DOWNLOADING),
            ('finished', DownloadStatus.COMPLETED),
            ('error', DownloadStatus.ERROR),
            ('paused', DownloadStatus.PAUSED),
            ('unknown', DownloadStatus.QUEUED)  # Unknown status should default to queued
        ]
        
        for status_str, expected_status in test_cases:
            item.update_progress({'status': status_str})
            assert item.status == expected_status
            
    def test_update_progress_calculates_percentage(self):
        """Test progress percentage calculation"""
        item = DownloadItem("https://example.com/video")
        
        # Test with total_bytes
        item.update_progress({
            'downloaded_bytes': 500,
            'total_bytes': 1000
        })
        assert item.progress == 50.0
        
        # Test with zero total_bytes (should not crash)
        item.update_progress({
            'downloaded_bytes': 500,
            'total_bytes': 0
        })
        # Progress should remain at previous value since we can't calculate
        assert item.progress == 50.0
        
    def test_set_error(self):
        """Test setting error status"""
        item = DownloadItem("https://example.com/video")
        error_msg = "Download failed: Network error"
        
        item.set_error(error_msg)
        
        assert item.status == DownloadStatus.ERROR
        assert item.error_message == error_msg
        
    def test_set_completed(self):
        """Test setting completed status"""
        item = DownloadItem("https://example.com/video")
        filepath = "/path/to/downloaded/file.mp4"
        
        item.set_completed(filepath)
        
        assert item.status == DownloadStatus.COMPLETED
        assert item.filepath == filepath
        assert item.progress == 100.0
        
    def test_unique_ids(self):
        """Test that each item gets a unique ID"""
        item1 = DownloadItem("https://example.com/video1")
        item2 = DownloadItem("https://example.com/video2")
        
        assert item1.id != item2.id
        
    def test_progress_update_with_missing_fields(self):
        """Test progress update with partial data"""
        item = DownloadItem("https://example.com/video")
        
        # Update with only some fields
        item.update_progress({
            'downloaded_bytes': 1000,
            'speed': 5000
        })
        
        assert item.downloaded_bytes == 1000
        assert item.speed == 5000
        # Other fields should remain at default values
        assert item.total_bytes == 0
        assert item.eta is None
        
    def test_progress_update_with_none_speed(self):
        """Test progress update with None speed"""
        item = DownloadItem("https://example.com/video")
        
        item.update_progress({
            'speed': None
        })
        
        assert item.speed == 0  # None speed should be converted to 0