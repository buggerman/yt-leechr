"""
Theme manager for dark/light mode support
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QSettings
from PyQt6.QtGui import QPalette, QColor

class ThemeManager:
    def __init__(self):
        self.settings = QSettings()
        
    def apply_theme(self, theme_name: str = None):
        if theme_name is None:
            theme_name = self.settings.value('theme', 'system')
            
        app = QApplication.instance()
        if not app:
            return
            
        if theme_name == 'dark':
            self.apply_dark_theme(app)
        elif theme_name == 'light':
            self.apply_light_theme(app)
        else:  # system
            self.apply_system_theme(app)
            
        self.settings.setValue('theme', theme_name)
        
    def apply_dark_theme(self, app):
        dark_palette = QPalette()
        
        # Window colors
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        
        # Base colors (input fields, etc.)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        
        # Tooltip colors
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        
        # Text colors
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        
        # Button colors
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        
        # Highlight colors
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        
        app.setPalette(dark_palette)
        
        # Set additional stylesheet for better dark mode appearance
        dark_stylesheet = """
        QMenuBar {
            background-color: #353535;
            color: #ffffff;
        }
        
        QMenuBar::item {
            background: transparent;
        }
        
        QMenuBar::item:selected {
            background-color: #2a82da;
        }
        
        QMenu {
            background-color: #353535;
            color: #ffffff;
            border: 1px solid #555555;
        }
        
        QMenu::item:selected {
            background-color: #2a82da;
        }
        
        QTabWidget::pane {
            border: 1px solid #555555;
            background-color: #353535;
        }
        
        QTabBar::tab {
            background-color: #404040;
            color: #ffffff;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #2a82da;
        }
        
        QTableWidget {
            gridline-color: #555555;
            selection-background-color: #2a82da;
        }
        
        QHeaderView::section {
            background-color: #404040;
            color: #ffffff;
            padding: 4px;
            border: 1px solid #555555;
        }
        
        QScrollBar:vertical {
            background-color: #404040;
            width: 15px;
            border-radius: 7px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #606060;
            border-radius: 7px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #707070;
        }
        
        QProgressBar {
            border: 1px solid #555555;
            border-radius: 5px;
            text-align: center;
            background-color: #404040;
        }
        
        QProgressBar::chunk {
            background-color: #2a82da;
            border-radius: 4px;
        }
        """
        
        app.setStyleSheet(dark_stylesheet)
        
    def apply_light_theme(self, app):
        light_palette = QPalette()
        
        # Reset to default light theme
        light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        light_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        light_palette.setColor(QPalette.ColorRole.Highlight, QColor(76, 163, 224))
        light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        app.setPalette(light_palette)
        app.setStyleSheet("")  # Clear any custom stylesheet
        
    def apply_system_theme(self, app):
        # Use system default theme
        app.setPalette(app.style().standardPalette())
        app.setStyleSheet("")
        
    def get_current_theme(self) -> str:
        return self.settings.value('theme', 'system')