"""
Tests for main_window module
"""

import pytest
import os
from unittest.mock import Mock, MagicMock, patch
from PyQt6.QtWidgets import QApplication, QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from src.main_window import MainWindow
from src.download_item import DownloadItem

@pytest.mark.gui
class TestMainWindow:
    def test_init(self, qt_app):
        """Test MainWindow initialization"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            
            assert window.windowTitle() == "YT Leechr - yt-dlp GUI"
            assert window.download_items == []
            assert window.url_input is not None
            assert window.queue_table is not None
            assert window.settings_widget is not None
            
    def test_paste_from_clipboard(self, qt_app):
        """Test pasting from clipboard"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            
            # Mock clipboard
            mock_clipboard = Mock()
            mock_clipboard.text.return_value = "https://example.com/video"
            
            with patch.object(QApplication, 'clipboard', return_value=mock_clipboard):
                window.paste_from_clipboard()
                
            assert window.url_input.text() == "https://example.com/video"
            
    def test_add_single_download(self, qt_app):
        """Test adding a single download"""
        with patch('src.main_window.DownloadManager') as mock_dm, \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            mock_dm_instance = mock_dm.return_value
            window.download_manager = mock_dm_instance
            
            url = "https://example.com/video"
            initial_rows = window.queue_table.rowCount()
            
            window.add_single_download(url)
            
            # Check that a row was added to the table
            assert window.queue_table.rowCount() == initial_rows + 1
            
            # Check that download item was created
            assert len(window.download_items) == 1
            assert window.download_items[0].url == url
            
            # Check that download manager was called
            mock_dm_instance.add_download.assert_called_once()
            
    def test_add_download_multiple_urls(self, qt_app):
        """Test adding multiple URLs at once"""
        with patch('src.main_window.DownloadManager') as mock_dm, \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            mock_dm_instance = mock_dm.return_value
            window.download_manager = mock_dm_instance
            
            urls = "https://example.com/video1\nhttps://example.com/video2\nhttps://example.com/video3"
            window.url_input.setText(urls)
            
            initial_rows = window.queue_table.rowCount()
            window.add_download()
            
            # Should add 3 rows
            assert window.queue_table.rowCount() == initial_rows + 3
            assert len(window.download_items) == 3
            
            # URL input should be cleared
            assert window.url_input.text() == ""
            
    def test_info_extracted(self, qt_app):
        """Test handling info extraction"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            
            # Add a download item
            item = DownloadItem("https://example.com/video")
            window.download_items.append(item)
            
            # Add corresponding table row
            row = window.queue_table.rowCount()
            window.queue_table.insertRow(row)
            window.queue_table.setItem(row, 0, QTableWidgetItem("Loading..."))
            
            # Test info extraction
            title = "Test Video Title"
            uploader = "Test Channel"
            window.info_extracted(item.id, title, uploader)
            
            # Check that table was updated
            title_item = window.queue_table.item(0, 0)
            assert title_item.text() == title
            
    def test_update_download_progress(self, qt_app, sample_progress_data):
        """Test updating download progress"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            
            # Add a download item and table row
            item = DownloadItem("https://example.com/video")
            window.download_items.append(item)
            
            row = window.queue_table.rowCount()
            window.queue_table.insertRow(row)
            window.queue_table.setItem(row, 0, QTableWidgetItem("Test Video"))
            window.queue_table.setItem(row, 1, QTableWidgetItem(item.url))
            window.queue_table.setItem(row, 2, QTableWidgetItem("Queued"))
            
            # Add progress bar
            from PyQt6.QtWidgets import QProgressBar
            progress_bar = QProgressBar()
            window.queue_table.setCellWidget(row, 3, progress_bar)
            
            window.queue_table.setItem(row, 4, QTableWidgetItem("--"))
            window.queue_table.setItem(row, 5, QTableWidgetItem("--"))
            
            # Update progress
            window.update_download_progress(item.id, sample_progress_data)
            
            # Check updates
            status_item = window.queue_table.item(0, 2)
            assert status_item.text() == sample_progress_data['status']
            
            progress_widget = window.queue_table.cellWidget(0, 3)
            assert progress_widget.value() == int(sample_progress_data['percent'])
            
            speed_item = window.queue_table.item(0, 4)
            assert "MB/s" in speed_item.text()
            
            size_item = window.queue_table.item(0, 5)
            assert "MB" in size_item.text()
            
    def test_download_completed(self, qt_app):
        """Test download completion handling"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            
            # Add a download item and table row
            item = DownloadItem("https://example.com/video")
            window.download_items.append(item)
            
            row = window.queue_table.rowCount()
            window.queue_table.insertRow(row)
            window.queue_table.setItem(row, 2, QTableWidgetItem("Downloading"))
            
            # Add progress bar
            from PyQt6.QtWidgets import QProgressBar
            progress_bar = QProgressBar()
            window.queue_table.setCellWidget(row, 3, progress_bar)
            
            filepath = "/path/to/downloaded/file.mp4"
            window.download_completed(item.id, filepath)
            
            # Check that status was updated
            status_item = window.queue_table.item(0, 2)
            assert status_item.text() == "Completed"
            
            # Check that progress bar is at 100%
            progress_widget = window.queue_table.cellWidget(0, 3)
            assert progress_widget.value() == 100
            
    def test_download_error(self, qt_app):
        """Test download error handling"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            
            # Add a download item and table row
            item = DownloadItem("https://example.com/video")
            window.download_items.append(item)
            
            row = window.queue_table.rowCount()
            window.queue_table.insertRow(row)
            window.queue_table.setItem(row, 2, QTableWidgetItem("Downloading"))
            
            error_msg = "Network error"
            window.download_error(item.id, error_msg)
            
            # Check that error status was set
            status_item = window.queue_table.item(0, 2)
            assert status_item.text() == f"Error: {error_msg}"
            
    def test_clear_completed(self, qt_app):
        """Test clearing completed downloads"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            
            # Add multiple items with different statuses
            items = [
                DownloadItem("https://example.com/video1"),
                DownloadItem("https://example.com/video2"),
                DownloadItem("https://example.com/video3")
            ]
            
            window.download_items.extend(items)
            
            # Add table rows
            for i, item in enumerate(items):
                window.queue_table.insertRow(i)
                window.queue_table.setItem(i, 0, QTableWidgetItem(f"Video {i+1}"))
                window.queue_table.setItem(i, 1, QTableWidgetItem(item.url))
                
            # Set different statuses
            window.queue_table.setItem(0, 2, QTableWidgetItem("Completed"))
            window.queue_table.setItem(1, 2, QTableWidgetItem("Downloading"))
            window.queue_table.setItem(2, 2, QTableWidgetItem("Completed"))
            
            initial_count = len(window.download_items)
            window.clear_completed()
            
            # Should remove 2 completed items
            assert len(window.download_items) == initial_count - 2
            assert window.queue_table.rowCount() == 1
            
            # Remaining item should be the downloading one
            remaining_status = window.queue_table.item(0, 2)
            assert remaining_status.text() == "Downloading"
            
    def test_clear_all(self, qt_app):
        """Test clearing all downloads"""
        with patch('src.main_window.DownloadManager') as mock_dm, \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            mock_dm_instance = mock_dm.return_value
            window.download_manager = mock_dm_instance
            
            # Add some items
            items = [DownloadItem("https://example.com/video1"),
                    DownloadItem("https://example.com/video2")]
            window.download_items.extend(items)
            
            for i, item in enumerate(items):
                window.queue_table.insertRow(i)
                window.queue_table.setItem(i, 0, QTableWidgetItem(f"Video {i+1}"))
                
            window.clear_all()
            
            # Everything should be cleared
            assert len(window.download_items) == 0
            assert window.queue_table.rowCount() == 0
            mock_dm_instance.clear_all.assert_called_once()
            
    def test_update_status(self, qt_app):
        """Test status bar updates"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            
            # Mock download items with different statuses
            items = [
                Mock(status="downloading"),
                Mock(status="completed"),
                Mock(status="processing"),
                Mock(status="queued")
            ]
            window.download_items = items
            
            window.update_status()
            
            # Should count 2 active downloads (downloading + processing)
            assert "Active Downloads: 2" in window.active_downloads_label.text()
            assert "Queue Size: 4" in window.queue_size_label.text()
            
    def test_toggle_settings_panel(self, qt_app):
        """Test toggling settings panel visibility"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            window.show()  # Show the window to make widgets visible
            
            # Mock the setVisible method to track calls
            original_set_visible = window.settings_widget.setVisible
            with patch.object(window.settings_widget, 'setVisible') as mock_set_visible:
                # Mock isVisible to return the opposite of what we set
                visibility_state = [True]  # Use list to make it mutable in nested scope
                
                def mock_is_visible():
                    return visibility_state[0]
                
                def mock_set_visible_impl(visible):
                    visibility_state[0] = visible
                    return original_set_visible(visible)
                
                window.settings_widget.isVisible = mock_is_visible
                mock_set_visible.side_effect = mock_set_visible_impl
                
                # Test toggle from visible to hidden
                visibility_state[0] = True
                window.toggle_settings_panel()
                mock_set_visible.assert_called_with(False)
                
                # Test toggle from hidden to visible
                visibility_state[0] = False
                window.toggle_settings_panel()
                mock_set_visible.assert_called_with(True)
            
    def test_theme_switching(self, qt_app):
        """Test theme switching functionality"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager') as mock_tm:
            
            window = MainWindow()
            mock_tm_instance = mock_tm.return_value
            window.theme_manager = mock_tm_instance
            
            window.set_theme('dark')
            mock_tm_instance.apply_theme.assert_called_with('dark')
            
            window.set_theme('light')
            mock_tm_instance.apply_theme.assert_called_with('light')
            
    def test_copy_selected_urls(self, qt_app):
        """Test copying selected URLs to clipboard"""
        with patch('src.main_window.DownloadManager'), \
             patch('src.main_window.ThemeManager'):
            
            window = MainWindow()
            
            # Add some download items
            items = [
                DownloadItem("https://example.com/video1"),
                DownloadItem("https://example.com/video2")
            ]
            window.download_items.extend(items)
            
            # Mock clipboard
            mock_clipboard = Mock()
            
            with patch.object(QApplication, 'clipboard', return_value=mock_clipboard):
                window.copy_selected_urls({0, 1})  # Copy both URLs
                
            expected_text = "https://example.com/video1\nhttps://example.com/video2"
            mock_clipboard.setText.assert_called_once_with(expected_text)