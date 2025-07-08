"""
Settings widget for configuring download options
"""

import os
from typing import Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QLineEdit, QPushButton, QComboBox, QCheckBox, QSpinBox,
    QFileDialog, QTabWidget, QTextEdit, QGridLayout, QFrame
)
from PyQt6.QtCore import QSettings, Qt

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Create tabs
        tab_widget = QTabWidget()
        
        # Output tab
        output_tab = self.create_output_tab()
        tab_widget.addTab(output_tab, "Output")
        
        # Format tab
        format_tab = self.create_format_tab()
        tab_widget.addTab(format_tab, "Format")
        
        # Subtitles tab
        subtitles_tab = self.create_subtitles_tab()
        tab_widget.addTab(subtitles_tab, "Subtitles")
        
        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        tab_widget.addTab(advanced_tab, "Advanced")
        
        layout.addWidget(tab_widget)
        
        # Add apply button
        apply_button = QPushButton("Apply Settings")
        apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(apply_button)
        
    def create_output_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Download directory
        dir_group = QGroupBox("Download Directory")
        dir_layout = QVBoxLayout(dir_group)
        
        dir_row = QHBoxLayout()
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("Select download directory...")
        
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_output_dir)
        
        dir_row.addWidget(self.output_dir_edit)
        dir_row.addWidget(browse_button)
        dir_layout.addLayout(dir_row)
        
        layout.addWidget(dir_group)
        
        # Output template
        template_group = QGroupBox("File Naming")
        template_layout = QVBoxLayout(template_group)
        
        template_layout.addWidget(QLabel("Output Template:"))
        self.output_template_combo = QComboBox()
        self.output_template_combo.setEditable(True)
        self.output_template_combo.addItems([
            "%(title)s.%(ext)s",
            "%(uploader)s - %(title)s.%(ext)s",
            "%(playlist_index)02d - %(title)s.%(ext)s",
            "%(upload_date)s - %(title)s.%(ext)s",
            "%(channel)s/%(title)s.%(ext)s"
        ])
        template_layout.addWidget(self.output_template_combo)
        
        template_layout.addWidget(QLabel("Common variables: %(title)s, %(uploader)s, %(upload_date)s, %(ext)s"))
        
        layout.addWidget(template_group)
        
        layout.addStretch()
        return widget
        
    def create_format_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Format selection
        format_group = QGroupBox("Format Selection")
        format_layout = QVBoxLayout(format_group)
        
        # Simple format selection
        format_layout.addWidget(QLabel("Quality:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "Best (Video + Audio)",
            "4K (if available)",
            "1440p (if available)",
            "1080p (if available)",
            "720p (if available)", 
            "480p (if available)",
            "Best Video Only",
            "Best Audio Only",
            "Worst (Smallest File)",
            "Custom Format"
        ])
        format_layout.addWidget(self.format_combo)
        
        # Custom format input
        self.custom_format_edit = QLineEdit()
        self.custom_format_edit.setPlaceholderText("e.g., bestvideo[height<=1080]+bestaudio/best")
        self.custom_format_edit.setEnabled(False)
        format_layout.addWidget(self.custom_format_edit)
        
        # Enable custom format when selected
        self.format_combo.currentTextChanged.connect(self.on_format_changed)
        
        layout.addWidget(format_group)
        
        # Audio extraction
        audio_group = QGroupBox("Audio Extraction")
        audio_layout = QVBoxLayout(audio_group)
        
        self.extract_audio_checkbox = QCheckBox("Extract audio only")
        audio_layout.addWidget(self.extract_audio_checkbox)
        
        audio_format_layout = QHBoxLayout()
        audio_format_layout.addWidget(QLabel("Audio Format:"))
        self.audio_format_combo = QComboBox()
        self.audio_format_combo.addItems(["mp3", "m4a", "ogg", "wav", "flac"])
        audio_format_layout.addWidget(self.audio_format_combo)
        
        audio_format_layout.addWidget(QLabel("Quality:"))
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["320", "256", "192", "128", "96", "64"])
        audio_format_layout.addWidget(self.audio_quality_combo)
        
        audio_layout.addLayout(audio_format_layout)
        
        layout.addWidget(audio_group)
        
        layout.addStretch()
        return widget
        
    def create_subtitles_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Subtitle options
        subtitle_group = QGroupBox("Subtitle Options")
        subtitle_layout = QVBoxLayout(subtitle_group)
        
        self.download_subtitles_checkbox = QCheckBox("Download subtitles")
        subtitle_layout.addWidget(self.download_subtitles_checkbox)
        
        self.embed_subtitles_checkbox = QCheckBox("Embed subtitles in video")
        subtitle_layout.addWidget(self.embed_subtitles_checkbox)
        
        # Language selection
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Languages:"))
        self.subtitle_languages_edit = QLineEdit()
        self.subtitle_languages_edit.setPlaceholderText("e.g., en,es,fr")
        lang_layout.addWidget(self.subtitle_languages_edit)
        
        subtitle_layout.addLayout(lang_layout)
        
        layout.addWidget(subtitle_group)
        
        layout.addStretch()
        return widget
        
    def create_advanced_tab(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Advanced options
        advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QVBoxLayout(advanced_group)
        
        self.write_thumbnail_checkbox = QCheckBox("Download thumbnail")
        advanced_layout.addWidget(self.write_thumbnail_checkbox)
        
        self.add_metadata_checkbox = QCheckBox("Add metadata to file")
        advanced_layout.addWidget(self.add_metadata_checkbox)
        
        self.download_playlist_checkbox = QCheckBox("Download entire playlist")
        advanced_layout.addWidget(self.download_playlist_checkbox)
        
        # Concurrent downloads
        concurrent_layout = QHBoxLayout()
        concurrent_layout.addWidget(QLabel("Max concurrent downloads:"))
        self.max_concurrent_spinbox = QSpinBox()
        self.max_concurrent_spinbox.setRange(1, 10)
        self.max_concurrent_spinbox.setValue(3)
        concurrent_layout.addWidget(self.max_concurrent_spinbox)
        
        advanced_layout.addLayout(concurrent_layout)
        
        layout.addWidget(advanced_group)
        
        # Custom arguments
        custom_group = QGroupBox("Custom yt-dlp Arguments")
        custom_layout = QVBoxLayout(custom_group)
        
        custom_layout.addWidget(QLabel("Additional command line arguments:"))
        self.custom_args_edit = QTextEdit()
        self.custom_args_edit.setMaximumHeight(100)
        self.custom_args_edit.setPlaceholderText("e.g., --user-agent \"Custom User Agent\"")
        custom_layout.addWidget(self.custom_args_edit)
        
        layout.addWidget(custom_group)
        
        layout.addStretch()
        return widget
        
    def on_format_changed(self, text: str):
        self.custom_format_edit.setEnabled(text == "Custom Format")
        
    def browse_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Download Directory", 
            self.output_dir_edit.text() or os.path.expanduser("~")
        )
        if dir_path:
            self.output_dir_edit.setText(dir_path)
            
    def get_settings(self) -> Dict[str, Any]:
        format_map = {
            "Best (Video + Audio)": "best[ext=mp4]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
            "4K (if available)": "best[height<=2160][ext=mp4]/bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=2160]+bestaudio/best[height<=2160]",
            "1440p (if available)": "best[height<=1440][ext=mp4]/bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1440]+bestaudio/best[height<=1440]",
            "1080p (if available)": "best[height<=1080][ext=mp4]/bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "720p (if available)": "best[height<=720][ext=mp4]/bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]",
            "480p (if available)": "best[height<=480][ext=mp4]/bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]",
            "Best Video Only": "bestvideo",
            "Best Audio Only": "bestaudio",
            "Worst (Smallest File)": "worst",
            "Custom Format": self.custom_format_edit.text() or "best[ext=mp4]/bestvideo+bestaudio/best"
        }
        
        return {
            'output_dir': self.output_dir_edit.text() or os.path.expanduser('~/Downloads'),
            'output_template': self.output_template_combo.currentText(),
            'format': format_map.get(self.format_combo.currentText(), "best"),
            'extract_audio': self.extract_audio_checkbox.isChecked(),
            'audio_format': self.audio_format_combo.currentText(),
            'audio_quality': self.audio_quality_combo.currentText(),
            'download_subtitles': self.download_subtitles_checkbox.isChecked(),
            'embed_subtitles': self.embed_subtitles_checkbox.isChecked(),
            'subtitle_languages': self.subtitle_languages_edit.text() or "en",
            'write_thumbnail': self.write_thumbnail_checkbox.isChecked(),
            'add_metadata': self.add_metadata_checkbox.isChecked(),
            'download_playlist': self.download_playlist_checkbox.isChecked(),
            'max_concurrent': self.max_concurrent_spinbox.value(),
            'custom_args': self.custom_args_edit.toPlainText()
        }
        
    def load_settings(self):
        # Load settings from QSettings
        self.output_dir_edit.setText(
            self.settings.value('output_dir', os.path.expanduser('~/Downloads'))
        )
        self.output_template_combo.setCurrentText(
            self.settings.value('output_template', '%(title)s.%(ext)s')
        )
        
        format_text = self.settings.value('format_text', 'Best (Video + Audio)')
        self.format_combo.setCurrentText(format_text)
        
        self.custom_format_edit.setText(
            self.settings.value('custom_format', '')
        )
        
        self.extract_audio_checkbox.setChecked(
            self.settings.value('extract_audio', False, bool)
        )
        self.audio_format_combo.setCurrentText(
            self.settings.value('audio_format', 'mp3')
        )
        self.audio_quality_combo.setCurrentText(
            self.settings.value('audio_quality', '192')
        )
        
        self.download_subtitles_checkbox.setChecked(
            self.settings.value('download_subtitles', False, bool)
        )
        self.embed_subtitles_checkbox.setChecked(
            self.settings.value('embed_subtitles', False, bool)
        )
        self.subtitle_languages_edit.setText(
            self.settings.value('subtitle_languages', 'en')
        )
        
        self.write_thumbnail_checkbox.setChecked(
            self.settings.value('write_thumbnail', False, bool)
        )
        self.add_metadata_checkbox.setChecked(
            self.settings.value('add_metadata', False, bool)
        )
        self.download_playlist_checkbox.setChecked(
            self.settings.value('download_playlist', False, bool)
        )
        
        self.max_concurrent_spinbox.setValue(
            self.settings.value('max_concurrent', 3, int)
        )
        self.custom_args_edit.setPlainText(
            self.settings.value('custom_args', '')
        )
        
    def save_settings(self):
        # Save settings to QSettings
        self.settings.setValue('output_dir', self.output_dir_edit.text())
        self.settings.setValue('output_template', self.output_template_combo.currentText())
        self.settings.setValue('format_text', self.format_combo.currentText())
        self.settings.setValue('custom_format', self.custom_format_edit.text())
        self.settings.setValue('extract_audio', self.extract_audio_checkbox.isChecked())
        self.settings.setValue('audio_format', self.audio_format_combo.currentText())
        self.settings.setValue('audio_quality', self.audio_quality_combo.currentText())
        self.settings.setValue('download_subtitles', self.download_subtitles_checkbox.isChecked())
        self.settings.setValue('embed_subtitles', self.embed_subtitles_checkbox.isChecked())
        self.settings.setValue('subtitle_languages', self.subtitle_languages_edit.text())
        self.settings.setValue('write_thumbnail', self.write_thumbnail_checkbox.isChecked())
        self.settings.setValue('add_metadata', self.add_metadata_checkbox.isChecked())
        self.settings.setValue('download_playlist', self.download_playlist_checkbox.isChecked())
        self.settings.setValue('max_concurrent', self.max_concurrent_spinbox.value())
        self.settings.setValue('custom_args', self.custom_args_edit.toPlainText())
        
    def apply_settings(self):
        self.save_settings()