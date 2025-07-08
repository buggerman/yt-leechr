#!/usr/bin/env python3
"""
YT Leechr - A Feature-Rich, Cross-Platform GUI for yt-dlp
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("YT Leechr")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("YT Leechr")
    
    # Set application icon
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()