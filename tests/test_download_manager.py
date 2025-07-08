"""
Tests for download_manager module
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from PyQt6.QtCore import QObject
from src.download_manager import DownloadManager, DownloadWorker
from src.download_item import DownloadItem, DownloadStatus

@pytest.mark.unit
class TestDownloadWorker:
    def test_init(self):
        """Test DownloadWorker initialization"""
        item = DownloadItem("https://example.com/video")
        settings = {'output_dir': '/tmp', 'format': 'best'}
        
        worker = DownloadWorker(item, settings)
        
        assert worker.download_item == item
        assert worker.settings == settings
        assert worker.is_paused is False
        assert worker.is_cancelled is False
        
    def test_build_ydl_options(self):
        """Test building yt-dlp options"""
        item = DownloadItem("https://example.com/video")
        settings = {
            'output_dir': '/downloads',
            'output_template': '%(title)s.%(ext)s',
            'format': 'best',
            'download_playlist': False,
            'extract_audio': True,
            'audio_format': 'mp3',
            'audio_quality': '192',
            'download_subtitles': True,
            'subtitle_languages': 'en,es',
            'write_thumbnail': True,
            'add_metadata': True
        }
        
        worker = DownloadWorker(item, settings)
        opts = worker.build_ydl_options()
        
        assert '/downloads' in opts['outtmpl']
        assert '%(title)s.%(ext)s' in opts['outtmpl']
        assert opts['format'] == 'best'
        assert opts['noplaylist'] is True  # download_playlist=False
        assert opts['extractaudio'] is True
        assert opts['audioformat'] == 'mp3'
        assert opts['audioquality'] == '192'
        assert opts['writesubtitles'] is True
        assert opts['writeautomaticsub'] is True
        assert opts['subtitleslangs'] == ['en', 'es']
        assert opts['writethumbnail'] is True
        assert opts['addmetadata'] is True
        
    def test_build_ydl_options_defaults(self):
        """Test building yt-dlp options with defaults"""
        item = DownloadItem("https://example.com/video")
        settings = {}  # Empty settings should use defaults
        
        worker = DownloadWorker(item, settings)
        opts = worker.build_ydl_options()
        
        assert 'Downloads' in opts['outtmpl']  # Should use default downloads folder
        assert opts['format'] == 'bestvideo+bestaudio/best'
        assert opts['noplaylist'] is True  # default
        assert opts['extractaudio'] is False  # default
        assert 'writesubtitles' not in opts  # Should not be set when False
        
    def test_progress_hook(self):
        """Test progress hook functionality"""
        item = DownloadItem("https://example.com/video")
        settings = {}
        worker = DownloadWorker(item, settings)
        
        # Mock the signal emission
        worker.progress_updated = Mock()
        
        # Test progress data
        progress_data = {
            'status': 'downloading',
            'downloaded_bytes': 1000,
            'total_bytes': 10000,
            'speed': 5000,
            'eta': 18
        }
        
        worker.progress_hook(progress_data)
        
        # Verify signal was emitted with correct data
        worker.progress_updated.emit.assert_called_once()
        call_args = worker.progress_updated.emit.call_args[0]
        
        assert call_args[0] == item.id
        emitted_data = call_args[1]
        assert emitted_data['status'] == 'downloading'
        assert emitted_data['downloaded_bytes'] == 1000
        assert emitted_data['total_bytes'] == 10000
        assert emitted_data['speed'] == 5000
        assert emitted_data['eta'] == 18
        assert emitted_data['percent'] == 10.0  # 1000/10000 * 100
        
    def test_progress_hook_with_estimate(self):
        """Test progress hook with total_bytes_estimate"""
        item = DownloadItem("https://example.com/video")
        settings = {}
        worker = DownloadWorker(item, settings)
        worker.progress_updated = Mock()
        
        # Test with total_bytes_estimate instead of total_bytes
        progress_data = {
            'status': 'downloading',
            'downloaded_bytes': 2000,
            'total_bytes_estimate': 8000,
            'speed': 3000
        }
        
        worker.progress_hook(progress_data)
        
        call_args = worker.progress_updated.emit.call_args[0]
        emitted_data = call_args[1]
        assert emitted_data['percent'] == 25.0  # 2000/8000 * 100
        
    def test_progress_hook_cancelled(self):
        """Test progress hook when cancelled"""
        item = DownloadItem("https://example.com/video")
        settings = {}
        worker = DownloadWorker(item, settings)
        worker.progress_updated = Mock()
        worker.is_cancelled = True
        
        progress_data = {'status': 'downloading'}
        worker.progress_hook(progress_data)
        
        # Should not emit signal when cancelled
        worker.progress_updated.emit.assert_not_called()
        
    def test_pause_resume_cancel(self):
        """Test pause, resume, and cancel functionality"""
        item = DownloadItem("https://example.com/video")
        settings = {}
        worker = DownloadWorker(item, settings)
        
        # Test pause
        worker.pause()
        assert worker.is_paused is True
        
        # Test resume
        worker.resume()
        assert worker.is_paused is False
        
        # Test cancel
        worker.cancel()
        assert worker.is_cancelled is True

@pytest.mark.unit
class TestDownloadManager:
    def test_init(self):
        """Test DownloadManager initialization"""
        manager = DownloadManager()
        
        assert manager.active_downloads == {}
        assert manager.max_concurrent_downloads == 3
        assert manager.download_queue.empty()
        
    @patch('src.download_manager.DownloadWorker')
    def test_add_download_immediate(self, mock_worker_class):
        """Test adding download when under concurrent limit"""
        manager = DownloadManager()
        item = DownloadItem("https://example.com/video")
        settings = {'format': 'best'}
        
        # Mock worker instance
        mock_worker = Mock()
        mock_worker_class.return_value = mock_worker
        
        manager.add_download(item, settings)
        
        # Should start download immediately
        mock_worker_class.assert_called_once_with(item, settings)
        mock_worker.start.assert_called_once()
        assert item.id in manager.active_downloads
        
    @patch('src.download_manager.DownloadWorker')
    def test_add_download_queue(self, mock_worker_class):
        """Test adding download when at concurrent limit"""
        manager = DownloadManager()
        manager.max_concurrent_downloads = 1
        
        # Add first download (should start immediately)
        item1 = DownloadItem("https://example.com/video1")
        settings = {'format': 'best'}
        
        mock_worker1 = Mock()
        mock_worker_class.return_value = mock_worker1
        
        manager.add_download(item1, settings)
        assert len(manager.active_downloads) == 1
        
        # Add second download (should be queued)
        item2 = DownloadItem("https://example.com/video2")
        mock_worker_class.reset_mock()
        
        manager.add_download(item2, settings)
        
        # Second worker should not be created yet
        assert len(manager.active_downloads) == 1
        assert not manager.download_queue.empty()
        
    def test_signal_forwarding(self):
        """Test that manager forwards signals correctly"""
        manager = DownloadManager()
        
        # Mock the signals
        manager.download_progress = Mock()
        manager.info_extracted = Mock()
        manager.download_completed = Mock()
        manager.download_error = Mock()
        
        # Test signal forwarding
        manager.on_progress_updated("test_id", {"progress": 50})
        manager.on_info_extracted("test_id", "Test Title", "Test Channel")
        manager.on_download_completed("test_id", "/path/to/file.mp4")
        manager.on_download_error("test_id", "Test error")
        
        manager.download_progress.emit.assert_called_once_with("test_id", {"progress": 50})
        manager.info_extracted.emit.assert_called_once_with("test_id", "Test Title", "Test Channel")
        manager.download_completed.emit.assert_called_once_with("test_id", "/path/to/file.mp4")
        manager.download_error.emit.assert_called_once_with("test_id", "Test error")
        
    @patch('src.download_manager.DownloadWorker')
    def test_worker_finished_starts_next(self, mock_worker_class):
        """Test that finishing a worker starts the next queued download"""
        manager = DownloadManager()
        manager.max_concurrent_downloads = 1
        
        # Add two downloads
        item1 = DownloadItem("https://example.com/video1")
        item2 = DownloadItem("https://example.com/video2")
        settings = {'format': 'best'}
        
        mock_worker1 = Mock()
        mock_worker2 = Mock()
        mock_worker_class.side_effect = [mock_worker1, mock_worker2]
        
        manager.add_download(item1, settings)
        manager.add_download(item2, settings)  # This should be queued
        
        assert len(manager.active_downloads) == 1
        assert not manager.download_queue.empty()
        
        # Simulate first worker finishing
        manager.worker_finished(item1.id)
        
        # Should start second worker
        assert len(manager.active_downloads) == 1
        assert manager.download_queue.empty()
        mock_worker2.start.assert_called_once()
        
    def test_pause_resume_cancel_operations(self):
        """Test pause, resume, and cancel operations"""
        manager = DownloadManager()
        
        # Mock active downloads
        mock_worker1 = Mock()
        mock_worker2 = Mock()
        manager.active_downloads = {
            "id1": mock_worker1,
            "id2": mock_worker2
        }
        
        # Test pause_all
        manager.pause_all()
        mock_worker1.pause.assert_called_once()
        mock_worker2.pause.assert_called_once()
        
        # Test resume_all
        manager.resume_all()
        mock_worker1.resume.assert_called_once()
        mock_worker2.resume.assert_called_once()
        
        # Test individual operations
        manager.pause_download("id1")
        assert mock_worker1.pause.call_count == 2  # Called twice now
        
        manager.resume_download("id2")
        assert mock_worker2.resume.call_count == 2  # Called twice now
        
        manager.cancel_download("id1")
        mock_worker1.cancel.assert_called_once()
        
    def test_clear_all(self):
        """Test clearing all downloads"""
        manager = DownloadManager()
        
        # Mock active downloads
        mock_worker1 = Mock()
        mock_worker2 = Mock()
        manager.active_downloads = {
            "id1": mock_worker1,
            "id2": mock_worker2
        }
        
        # Add items to queue
        item = DownloadItem("https://example.com/video")
        manager.download_queue.put((item, {}))
        
        manager.clear_all()
        
        # All workers should be cancelled
        mock_worker1.cancel.assert_called_once()
        mock_worker2.cancel.assert_called_once()
        
        # Active downloads should be cleared
        assert manager.active_downloads == {}
        
        # Queue should be empty
        assert manager.download_queue.empty()