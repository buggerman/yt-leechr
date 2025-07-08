"""
Tests for theme_manager module
"""

import pytest
from unittest.mock import Mock, patch
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSettings

from src.theme_manager import ThemeManager

@pytest.mark.unit
class TestThemeManager:
    def test_init(self):
        """Test ThemeManager initialization"""
        manager = ThemeManager()
        assert manager.settings is not None
        
    def test_apply_theme_dark(self, qt_app):
        """Test applying dark theme"""
        manager = ThemeManager()
        
        with patch.object(manager, 'apply_dark_theme') as mock_dark:
            manager.apply_theme('dark')
            mock_dark.assert_called_once_with(qt_app)
            
    def test_apply_theme_light(self, qt_app):
        """Test applying light theme"""
        manager = ThemeManager()
        
        with patch.object(manager, 'apply_light_theme') as mock_light:
            manager.apply_theme('light')
            mock_light.assert_called_once_with(qt_app)
            
    def test_apply_theme_system(self, qt_app):
        """Test applying system theme"""
        manager = ThemeManager()
        
        with patch.object(manager, 'apply_system_theme') as mock_system:
            manager.apply_theme('system')
            mock_system.assert_called_once_with(qt_app)
            
    def test_apply_theme_saves_setting(self, qt_app):
        """Test that apply_theme saves the setting"""
        manager = ThemeManager()
        
        with patch.object(manager.settings, 'setValue') as mock_set_value, \
             patch.object(manager, 'apply_dark_theme'):
            
            manager.apply_theme('dark')
            mock_set_value.assert_called_once_with('theme', 'dark')
            
    def test_apply_theme_with_none_uses_saved(self, qt_app):
        """Test applying theme with None uses saved setting"""
        manager = ThemeManager()
        
        with patch.object(manager.settings, 'value', return_value='light') as mock_value, \
             patch.object(manager, 'apply_light_theme') as mock_light:
            
            manager.apply_theme(None)
            mock_value.assert_called_once_with('theme', 'system')
            mock_light.assert_called_once_with(qt_app)
            
    def test_apply_dark_theme(self, qt_app):
        """Test dark theme application"""
        manager = ThemeManager()
        
        # Mock the application
        mock_app = Mock()
        manager.apply_dark_theme(mock_app)
        
        # Verify palette was set
        mock_app.setPalette.assert_called_once()
        
        # Verify stylesheet was set
        mock_app.setStyleSheet.assert_called_once()
        stylesheet = mock_app.setStyleSheet.call_args[0][0]
        assert 'QMenuBar' in stylesheet
        assert 'background-color' in stylesheet
        
    def test_apply_light_theme(self, qt_app):
        """Test light theme application"""
        manager = ThemeManager()
        
        # Mock the application
        mock_app = Mock()
        manager.apply_light_theme(mock_app)
        
        # Verify palette was set
        mock_app.setPalette.assert_called_once()
        
        # Verify stylesheet was cleared
        mock_app.setStyleSheet.assert_called_once_with("")
        
    def test_apply_system_theme(self, qt_app):
        """Test system theme application"""
        manager = ThemeManager()
        
        # Mock the application and style
        mock_style = Mock()
        mock_style.standardPalette.return_value = Mock()
        mock_app = Mock()
        mock_app.style.return_value = mock_style
        
        manager.apply_system_theme(mock_app)
        
        # Verify system palette was used
        mock_app.setPalette.assert_called_once()
        mock_style.standardPalette.assert_called_once()
        
        # Verify stylesheet was cleared
        mock_app.setStyleSheet.assert_called_once_with("")
        
    def test_get_current_theme(self):
        """Test getting current theme"""
        manager = ThemeManager()
        
        with patch.object(manager.settings, 'value', return_value='dark') as mock_value:
            theme = manager.get_current_theme()
            
            assert theme == 'dark'
            mock_value.assert_called_once_with('theme', 'system')
            
    def test_get_current_theme_default(self):
        """Test getting current theme with default"""
        manager = ThemeManager()
        
        with patch.object(manager.settings, 'value', return_value='system') as mock_value:
            theme = manager.get_current_theme()
            
            assert theme == 'system'
            
    def test_dark_theme_palette_colors(self, qt_app):
        """Test that dark theme sets expected palette colors"""
        manager = ThemeManager()
        
        # Mock the application
        mock_app = Mock()
        manager.apply_dark_theme(mock_app)
        
        # Get the palette that was set
        call_args = mock_app.setPalette.call_args[0]
        palette = call_args[0]
        
        # Verify it's a QPalette (or our mock)
        assert palette is not None
        
    def test_light_theme_palette_colors(self, qt_app):
        """Test that light theme sets expected palette colors"""
        manager = ThemeManager()
        
        # Mock the application
        mock_app = Mock()
        manager.apply_light_theme(mock_app)
        
        # Get the palette that was set
        call_args = mock_app.setPalette.call_args[0]
        palette = call_args[0]
        
        # Verify it's a QPalette (or our mock)
        assert palette is not None
        
    def test_dark_theme_stylesheet_content(self, qt_app):
        """Test dark theme stylesheet contains expected elements"""
        manager = ThemeManager()
        
        # Mock the application
        mock_app = Mock()
        manager.apply_dark_theme(mock_app)
        
        # Get the stylesheet that was set
        stylesheet = mock_app.setStyleSheet.call_args[0][0]
        
        # Check for key elements
        assert 'QMenuBar' in stylesheet
        assert 'QTabWidget' in stylesheet
        assert 'QTableWidget' in stylesheet
        assert 'QProgressBar' in stylesheet
        assert 'QScrollBar' in stylesheet
        assert 'background-color' in stylesheet
        assert '#353535' in stylesheet  # Dark background color
        assert '#ffffff' in stylesheet  # White text color
        
    @pytest.mark.integration
    def test_theme_switching_integration(self, qt_app):
        """Integration test for theme switching"""
        manager = ThemeManager()
        
        # Test switching between themes
        themes = ['light', 'dark', 'system']
        
        for theme in themes:
            # This should not raise any exceptions
            manager.apply_theme(theme)
            
            # Verify the theme was saved
            assert manager.get_current_theme() == theme