"""
pytest configuration and fixtures
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

@pytest.fixture
def qt_app():
    """Create QApplication instance for tests"""
    from PyQt6.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Don't quit app as other tests might need it

@pytest.fixture
def mock_yt_dlp():
    """Mock yt-dlp module for testing"""
    mock = MagicMock()
    mock.YoutubeDL = MagicMock()
    return mock

@pytest.fixture
def sample_video_info():
    """Sample video info data for testing"""
    return {
        'id': 'test_video_id',
        'title': 'Test Video Title',
        'uploader': 'Test Channel',
        'duration': 300,
        'ext': 'mp4',
        'thumbnail': 'https://example.com/thumb.jpg',
        'url': 'https://example.com/video.mp4',
        'formats': [
            {
                'format_id': 'best',
                'ext': 'mp4',
                'resolution': '1920x1080',
                'url': 'https://example.com/video.mp4'
            }
        ]
    }

@pytest.fixture
def sample_progress_data():
    """Sample progress data for testing"""
    return {
        'status': 'downloading',
        'downloaded_bytes': 1024000,
        'total_bytes': 10240000,
        'speed': 512000,
        'eta': 18,
        'percent': 10.0
    }