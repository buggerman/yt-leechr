"""
Main window for YT Leechr GUI
"""

import os
from typing import Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QStatusBar, QMenuBar, QSplitter, QFrame, QLabel, QProgressBar,
    QMessageBox, QFileDialog, QTabWidget, QCheckBox, QComboBox,
    QSpinBox, QTextEdit, QGroupBox, QGridLayout, QApplication
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings, QTimer
from PyQt6.QtGui import QAction, QPixmap, QIcon
from PyQt6.QtWidgets import QMenu
from .download_manager import DownloadManager
from .settings_widget import SettingsWidget
from .download_item import DownloadItem
from .theme_manager import ThemeManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.download_manager = DownloadManager()
        self.download_items = []
        self.theme_manager = ThemeManager()
        
        self.init_ui()
        self.setup_connections()
        self.load_settings()
        
    def init_ui(self):
        self.setWindowTitle("YT Leechr - yt-dlp GUI")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create URL input section
        url_layout = QHBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste video URL(s) here...")
        self.url_input.returnPressed.connect(self.add_download)
        
        self.paste_button = QPushButton("Paste")
        self.paste_button.clicked.connect(self.paste_from_clipboard)
        
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.add_download)
        self.download_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        
        url_layout.addWidget(QLabel("URL:"))
        url_layout.addWidget(self.url_input)
        url_layout.addWidget(self.paste_button)
        url_layout.addWidget(self.download_button)
        
        main_layout.addLayout(url_layout)
        
        # Create splitter for main content
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create download queue table
        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(6)
        self.queue_table.setHorizontalHeaderLabels([
            "Title", "URL", "Status", "Progress", "Speed", "Size"
        ])
        
        # Configure table
        header = self.queue_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.queue_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.queue_table.setAlternatingRowColors(True)
        self.queue_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.queue_table.customContextMenuRequested.connect(self.show_context_menu)
        
        # Create settings widget
        self.settings_widget = SettingsWidget()
        
        # Add to splitter
        splitter.addWidget(self.queue_table)
        splitter.addWidget(self.settings_widget)
        splitter.setSizes([800, 400])
        
        main_layout.addWidget(splitter)
        
        # Create queue control buttons
        queue_controls = QHBoxLayout()
        
        self.pause_button = QPushButton("Pause All")
        self.pause_button.clicked.connect(self.pause_all_downloads)
        
        self.resume_button = QPushButton("Resume All")
        self.resume_button.clicked.connect(self.resume_all_downloads)
        
        self.clear_completed_button = QPushButton("Clear Completed")
        self.clear_completed_button.clicked.connect(self.clear_completed)
        
        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clear_all)
        
        queue_controls.addWidget(self.pause_button)
        queue_controls.addWidget(self.resume_button)
        queue_controls.addStretch()
        queue_controls.addWidget(self.clear_completed_button)
        queue_controls.addWidget(self.clear_all_button)
        
        main_layout.addLayout(queue_controls)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.active_downloads_label = QLabel("Active Downloads: 0")
        self.queue_size_label = QLabel("Queue Size: 0")
        
        self.status_bar.addPermanentWidget(self.active_downloads_label)
        self.status_bar.addPermanentWidget(self.queue_size_label)
        
        # Create menu bar
        self.create_menu_bar()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        toggle_settings_action = QAction("Toggle Settings Panel", self)
        toggle_settings_action.triggered.connect(self.toggle_settings_panel)
        view_menu.addAction(toggle_settings_action)
        
        view_menu.addSeparator()
        
        # Theme submenu
        theme_menu = view_menu.addMenu("Theme")
        
        light_theme_action = QAction("Light", self)
        light_theme_action.triggered.connect(lambda: self.set_theme('light'))
        theme_menu.addAction(light_theme_action)
        
        dark_theme_action = QAction("Dark", self)
        dark_theme_action.triggered.connect(lambda: self.set_theme('dark'))
        theme_menu.addAction(dark_theme_action)
        
        system_theme_action = QAction("System", self)
        system_theme_action.triggered.connect(lambda: self.set_theme('system'))
        theme_menu.addAction(system_theme_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_connections(self):
        self.download_manager.download_progress.connect(self.update_download_progress)
        self.download_manager.download_completed.connect(self.download_completed)
        self.download_manager.download_error.connect(self.download_error)
        self.download_manager.info_extracted.connect(self.info_extracted)
        
    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            self.url_input.setText(text)
            
    def add_download(self):
        url = self.url_input.text().strip()
        if not url:
            return
            
        urls = [u.strip() for u in url.split('\n') if u.strip()]
        
        for single_url in urls:
            if single_url:
                self.add_single_download(single_url)
                
        self.url_input.clear()
        self.update_status()
        
    def add_single_download(self, url: str):
        download_item = DownloadItem(url)
        self.download_items.append(download_item)
        
        row = self.queue_table.rowCount()
        self.queue_table.insertRow(row)
        
        self.queue_table.setItem(row, 0, QTableWidgetItem("Fetching info..."))
        self.queue_table.setItem(row, 1, QTableWidgetItem(url))
        self.queue_table.setItem(row, 2, QTableWidgetItem("Queued"))
        
        progress_bar = QProgressBar()
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(100)
        progress_bar.setValue(0)
        self.queue_table.setCellWidget(row, 3, progress_bar)
        
        self.queue_table.setItem(row, 4, QTableWidgetItem("--"))
        self.queue_table.setItem(row, 5, QTableWidgetItem("--"))
        
        # Start download
        self.download_manager.add_download(download_item, self.settings_widget.get_settings())
        
    def info_extracted(self, download_id: str, title: str, uploader: str):
        for i, item in enumerate(self.download_items):
            if item.id == download_id:
                self.queue_table.setItem(i, 0, QTableWidgetItem(title))
                break
                
    def update_download_progress(self, download_id: str, progress: dict):
        for i, item in enumerate(self.download_items):
            if item.id == download_id:
                if 'status' in progress:
                    self.queue_table.setItem(i, 2, QTableWidgetItem(progress['status']))
                    
                if 'percent' in progress:
                    progress_bar = self.queue_table.cellWidget(i, 3)
                    if progress_bar:
                        progress_bar.setValue(int(progress['percent']))
                        
                if 'speed' in progress:
                    speed = progress['speed']
                    if speed:
                        speed_str = f"{speed / 1024 / 1024:.1f} MB/s"
                        self.queue_table.setItem(i, 4, QTableWidgetItem(speed_str))
                        
                if 'total_bytes' in progress:
                    total_bytes = progress['total_bytes']
                    if total_bytes:
                        size_str = f"{total_bytes / 1024 / 1024:.1f} MB"
                        self.queue_table.setItem(i, 5, QTableWidgetItem(size_str))
                        
                break
                
    def download_completed(self, download_id: str, filepath: str):
        for i, item in enumerate(self.download_items):
            if item.id == download_id:
                self.queue_table.setItem(i, 2, QTableWidgetItem("Completed"))
                progress_bar = self.queue_table.cellWidget(i, 3)
                if progress_bar:
                    progress_bar.setValue(100)
                break
                
        self.update_status()
        
    def download_error(self, download_id: str, error: str):
        for i, item in enumerate(self.download_items):
            if item.id == download_id:
                self.queue_table.setItem(i, 2, QTableWidgetItem(f"Error: {error}"))
                break
                
        self.update_status()
        
    def pause_all_downloads(self):
        self.download_manager.pause_all()
        
    def resume_all_downloads(self):
        self.download_manager.resume_all()
        
    def clear_completed(self):
        # Remove completed items from both the table and the list
        i = 0
        while i < len(self.download_items):
            status_item = self.queue_table.item(i, 2)
            if status_item and status_item.text() == "Completed":
                self.queue_table.removeRow(i)
                del self.download_items[i]
            else:
                i += 1
                
        self.update_status()
        
    def clear_all(self):
        self.download_manager.clear_all()
        self.queue_table.setRowCount(0)
        self.download_items.clear()
        self.update_status()
        
    def toggle_settings_panel(self):
        self.settings_widget.setVisible(not self.settings_widget.isVisible())
        
    def set_theme(self, theme_name: str):
        self.theme_manager.apply_theme(theme_name)
        
    def show_about(self):
        QMessageBox.about(self, "About YT Leechr", 
            "YT Leechr v1.0.0\n\n"
            "A feature-rich, cross-platform GUI for yt-dlp.\n\n"
            "Built with PyQt6 and yt-dlp.")
            
    def update_status(self):
        active_count = sum(1 for item in self.download_items if item.status in ["downloading", "processing"])
        total_count = len(self.download_items)
        
        self.active_downloads_label.setText(f"Active Downloads: {active_count}")
        self.queue_size_label.setText(f"Queue Size: {total_count}")
        
    def load_settings(self):
        # Restore window geometry
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
            
        # Load other settings
        self.settings_widget.load_settings()
        
        # Apply saved theme
        self.theme_manager.apply_theme()
        
    def save_settings(self):
        # Save window geometry
        self.settings.setValue("geometry", self.saveGeometry())
        
        # Save other settings
        self.settings_widget.save_settings()
        
    def show_context_menu(self, position):
        if self.queue_table.itemAt(position) is None:
            return
            
        menu = QMenu(self)
        
        selected_rows = set()
        for item in self.queue_table.selectedItems():
            selected_rows.add(item.row())
            
        if not selected_rows:
            return
            
        # Add context menu actions
        pause_action = menu.addAction("Pause Download")
        resume_action = menu.addAction("Resume Download")
        retry_action = menu.addAction("Retry Download")
        menu.addSeparator()
        copy_url_action = menu.addAction("Copy URL")
        open_folder_action = menu.addAction("Open Containing Folder")
        menu.addSeparator()
        remove_action = menu.addAction("Remove from Queue")
        
        # Connect actions
        pause_action.triggered.connect(lambda: self.pause_selected_downloads(selected_rows))
        resume_action.triggered.connect(lambda: self.resume_selected_downloads(selected_rows))
        retry_action.triggered.connect(lambda: self.retry_selected_downloads(selected_rows))
        copy_url_action.triggered.connect(lambda: self.copy_selected_urls(selected_rows))
        open_folder_action.triggered.connect(lambda: self.open_containing_folder(selected_rows))
        remove_action.triggered.connect(lambda: self.remove_selected_downloads(selected_rows))
        
        menu.exec(self.queue_table.mapToGlobal(position))
        
    def pause_selected_downloads(self, rows):
        for row in rows:
            if row < len(self.download_items):
                download_item = self.download_items[row]
                self.download_manager.pause_download(download_item.id)
                
    def resume_selected_downloads(self, rows):
        for row in rows:
            if row < len(self.download_items):
                download_item = self.download_items[row]
                self.download_manager.resume_download(download_item.id)
                
    def retry_selected_downloads(self, rows):
        for row in rows:
            if row < len(self.download_items):
                download_item = self.download_items[row]
                # Restart the download
                self.download_manager.add_download(download_item, self.settings_widget.get_settings())
                
    def copy_selected_urls(self, rows):
        urls = []
        for row in rows:
            if row < len(self.download_items):
                urls.append(self.download_items[row].url)
                
        if urls:
            clipboard = QApplication.clipboard()
            clipboard.setText('\n'.join(urls))
            
    def open_containing_folder(self, rows):
        for row in rows:
            if row < len(self.download_items):
                download_item = self.download_items[row]
                if download_item.filepath and os.path.exists(download_item.filepath):
                    # Open the folder containing the file
                    import subprocess
                    import platform
                    
                    folder_path = os.path.dirname(download_item.filepath)
                    
                    if platform.system() == "Windows":
                        subprocess.run(["explorer", folder_path])
                    elif platform.system() == "Darwin":  # macOS
                        subprocess.run(["open", folder_path])
                    else:  # Linux
                        subprocess.run(["xdg-open", folder_path])
                        
    def remove_selected_downloads(self, rows):
        # Sort rows in descending order to remove from bottom up
        for row in sorted(rows, reverse=True):
            if row < len(self.download_items):
                download_item = self.download_items[row]
                self.download_manager.cancel_download(download_item.id)
                self.queue_table.removeRow(row)
                del self.download_items[row]
                
        self.update_status()

    def closeEvent(self, event):
        self.save_settings()
        self.download_manager.cleanup()
        event.accept()