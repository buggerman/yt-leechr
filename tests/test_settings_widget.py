"""
Tests for settings_widget module
"""

import pytest
import os
from unittest.mock import Mock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings

from src.settings_widget import SettingsWidget

@pytest.mark.gui
class TestSettingsWidget:
    def test_init(self, qt_app):
        """Test SettingsWidget initialization"""
        widget = SettingsWidget()
        
        assert widget.output_dir_edit is not None
        assert widget.output_template_combo is not None
        assert widget.format_combo is not None
        assert widget.extract_audio_checkbox is not None
        assert widget.download_subtitles_checkbox is not None
        assert widget.write_thumbnail_checkbox is not None
        
    def test_get_settings_default(self, qt_app):
        """Test getting default settings"""
        widget = SettingsWidget()
        
        settings = widget.get_settings()
        
        # Test default values
        assert 'Downloads' in settings['output_dir']  # Should use default downloads dir
        assert settings['output_template'] == '%(title)s.%(ext)s'
        assert settings['format'] == 'bestvideo+bestaudio/best'
        assert settings['extract_audio'] is False
        assert settings['audio_format'] == 'mp3'
        assert settings['audio_quality'] == '320'
        assert settings['download_subtitles'] is False
        assert settings['subtitle_languages'] == 'en'
        assert settings['write_thumbnail'] is False
        assert settings['add_metadata'] is False
        assert settings['download_playlist'] is False
        assert settings['max_concurrent'] == 3
        assert settings['custom_args'] == ''
        
    def test_get_settings_custom(self, qt_app):
        """Test getting custom settings"""
        widget = SettingsWidget()
        
        # Set custom values
        widget.output_dir_edit.setText('/custom/downloads')
        widget.output_template_combo.setCurrentText('%(uploader)s - %(title)s.%(ext)s')
        widget.format_combo.setCurrentText('Best Audio Only')
        widget.extract_audio_checkbox.setChecked(True)
        widget.audio_format_combo.setCurrentText('m4a')
        widget.audio_quality_combo.setCurrentText('192')
        widget.download_subtitles_checkbox.setChecked(True)
        widget.subtitle_languages_edit.setText('en,es,fr')
        widget.write_thumbnail_checkbox.setChecked(True)
        widget.add_metadata_checkbox.setChecked(True)
        widget.download_playlist_checkbox.setChecked(True)
        widget.max_concurrent_spinbox.setValue(5)
        widget.custom_args_edit.setPlainText('--user-agent "Custom Agent"')
        
        settings = widget.get_settings()
        
        assert settings['output_dir'] == '/custom/downloads'
        assert settings['output_template'] == '%(uploader)s - %(title)s.%(ext)s'
        assert settings['format'] == 'bestaudio'
        assert settings['extract_audio'] is True
        assert settings['audio_format'] == 'm4a'
        assert settings['audio_quality'] == '192'
        assert settings['download_subtitles'] is True
        assert settings['subtitle_languages'] == 'en,es,fr'
        assert settings['write_thumbnail'] is True
        assert settings['add_metadata'] is True
        assert settings['download_playlist'] is True
        assert settings['max_concurrent'] == 5
        assert settings['custom_args'] == '--user-agent "Custom Agent"'
        
    def test_format_mapping(self, qt_app):
        """Test format selection mapping"""
        widget = SettingsWidget()
        
        format_tests = [
            ('Best (Video + Audio)', 'bestvideo+bestaudio/best'),
            ('4K (if available)', 'bestvideo[height<=2160]+bestaudio/best[height<=2160]'),
            ('1440p (if available)', 'bestvideo[height<=1440]+bestaudio/best[height<=1440]'),
            ('1080p (if available)', 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'),
            ('720p (if available)', 'bestvideo[height<=720]+bestaudio/best[height<=720]'),
            ('480p (if available)', 'bestvideo[height<=480]+bestaudio/best[height<=480]'),
            ('Best Video Only', 'bestvideo'),
            ('Best Audio Only', 'bestaudio'),
            ('Worst (Smallest File)', 'worst'),
        ]
        
        for display_name, expected_format in format_tests:
            widget.format_combo.setCurrentText(display_name)
            settings = widget.get_settings()
            assert settings['format'] == expected_format
            
    def test_custom_format(self, qt_app):
        """Test custom format handling"""
        widget = SettingsWidget()
        
        # Test custom format
        widget.format_combo.setCurrentText('Custom Format')
        widget.custom_format_edit.setText('best[height<=720]')
        
        settings = widget.get_settings()
        assert settings['format'] == 'best[height<=720]'
        
        # Test custom format with empty input (should default to bestvideo+bestaudio/best)
        widget.custom_format_edit.setText('')
        settings = widget.get_settings()
        assert settings['format'] == 'bestvideo+bestaudio/best'
        
    def test_on_format_changed(self, qt_app):
        """Test format change handler"""
        widget = SettingsWidget()
        
        # Initially custom format should be disabled
        assert not widget.custom_format_edit.isEnabled()
        
        # Select custom format
        widget.on_format_changed('Custom Format')
        assert widget.custom_format_edit.isEnabled()
        
        # Select non-custom format
        widget.on_format_changed('Best (Video + Audio)')
        assert not widget.custom_format_edit.isEnabled()
        
    def test_browse_output_dir(self, qt_app):
        """Test browse output directory"""
        widget = SettingsWidget()
        
        with patch('src.settings_widget.QFileDialog.getExistingDirectory') as mock_dialog:
            mock_dialog.return_value = '/new/download/path'
            
            widget.browse_output_dir()
            
            assert widget.output_dir_edit.text() == '/new/download/path'
            mock_dialog.assert_called_once()
            
    def test_browse_output_dir_cancelled(self, qt_app):
        """Test browse output directory when user cancels"""
        widget = SettingsWidget()
        original_text = widget.output_dir_edit.text()
        
        with patch('src.settings_widget.QFileDialog.getExistingDirectory') as mock_dialog:
            mock_dialog.return_value = ''  # User cancelled
            
            widget.browse_output_dir()
            
            # Text should remain unchanged
            assert widget.output_dir_edit.text() == original_text
            
    def test_load_settings(self, qt_app):
        """Test loading settings from QSettings"""
        widget = SettingsWidget()
        
        # Mock QSettings
        with patch.object(widget, 'settings') as mock_settings:
            mock_settings.value.side_effect = lambda key, default, type_=None: {
                'output_dir': '/saved/downloads',
                'output_template': '%(upload_date)s - %(title)s.%(ext)s',
                'format_text': 'Best Video Only',
                'custom_format': 'best[height<=1080]',
                'extract_audio': True,
                'audio_format': 'ogg',
                'audio_quality': '128',
                'download_subtitles': True,
                'embed_subtitles': True,
                'subtitle_languages': 'en,de',
                'write_thumbnail': True,
                'add_metadata': True,
                'download_playlist': True,
                'max_concurrent': 2,
                'custom_args': '--verbose'
            }.get(key, default)
            
            widget.load_settings()
            
            # Verify settings were loaded
            assert widget.output_dir_edit.text() == '/saved/downloads'
            assert widget.output_template_combo.currentText() == '%(upload_date)s - %(title)s.%(ext)s'
            assert widget.format_combo.currentText() == 'Best Video Only'
            assert widget.custom_format_edit.text() == 'best[height<=1080]'
            assert widget.extract_audio_checkbox.isChecked() is True
            assert widget.audio_format_combo.currentText() == 'ogg'
            assert widget.audio_quality_combo.currentText() == '128'
            assert widget.download_subtitles_checkbox.isChecked() is True
            assert widget.embed_subtitles_checkbox.isChecked() is True
            assert widget.subtitle_languages_edit.text() == 'en,de'
            assert widget.write_thumbnail_checkbox.isChecked() is True
            assert widget.add_metadata_checkbox.isChecked() is True
            assert widget.download_playlist_checkbox.isChecked() is True
            assert widget.max_concurrent_spinbox.value() == 2
            assert widget.custom_args_edit.toPlainText() == '--verbose'
            
    def test_save_settings(self, qt_app):
        """Test saving settings to QSettings"""
        widget = SettingsWidget()
        
        # Set some values
        widget.output_dir_edit.setText('/test/path')
        widget.format_combo.setCurrentText('Best Audio Only')
        widget.extract_audio_checkbox.setChecked(True)
        widget.max_concurrent_spinbox.setValue(4)
        
        with patch.object(widget, 'settings') as mock_settings:
            widget.save_settings()
            
            # Verify setValue was called with correct values
            mock_settings.setValue.assert_any_call('output_dir', '/test/path')
            mock_settings.setValue.assert_any_call('format_text', 'Best Audio Only')
            mock_settings.setValue.assert_any_call('extract_audio', True)
            mock_settings.setValue.assert_any_call('max_concurrent', 4)
            
    def test_apply_settings(self, qt_app):
        """Test apply settings button"""
        widget = SettingsWidget()
        
        with patch.object(widget, 'save_settings') as mock_save:
            widget.apply_settings()
            mock_save.assert_called_once()
            
    def test_output_template_presets(self, qt_app):
        """Test output template presets"""
        widget = SettingsWidget()
        
        expected_presets = [
            "%(title)s.%(ext)s",
            "%(uploader)s - %(title)s.%(ext)s",
            "%(playlist_index)02d - %(title)s.%(ext)s",
            "%(upload_date)s - %(title)s.%(ext)s",
            "%(channel)s/%(title)s.%(ext)s"
        ]
        
        # Check that all presets are available
        for i in range(widget.output_template_combo.count()):
            item_text = widget.output_template_combo.itemText(i)
            assert item_text in expected_presets
            
    def test_audio_format_options(self, qt_app):
        """Test audio format options"""
        widget = SettingsWidget()
        
        expected_formats = ["mp3", "m4a", "ogg", "wav", "flac"]
        
        # Check that all audio formats are available
        for i in range(widget.audio_format_combo.count()):
            item_text = widget.audio_format_combo.itemText(i)
            assert item_text in expected_formats
            
    def test_audio_quality_options(self, qt_app):
        """Test audio quality options"""
        widget = SettingsWidget()
        
        expected_qualities = ["320", "256", "192", "128", "96", "64"]
        
        # Check that all quality options are available
        for i in range(widget.audio_quality_combo.count()):
            item_text = widget.audio_quality_combo.itemText(i)
            assert item_text in expected_qualities
            
    def test_max_concurrent_range(self, qt_app):
        """Test max concurrent downloads range"""
        widget = SettingsWidget()
        
        # Check spinbox range
        assert widget.max_concurrent_spinbox.minimum() == 1
        assert widget.max_concurrent_spinbox.maximum() == 10
        assert widget.max_concurrent_spinbox.value() == 3  # Default value