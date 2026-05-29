from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QComboBox, QFrame, QScrollArea, QLineEdit, 
                               QPushButton, QFileDialog, QMessageBox, QGridLayout)
from PySide6.QtCore import Slot, Qt, Signal
from pathlib import Path
import math
import shutil
from database import ThatchDB

class PreferencesView(QWidget):
    """
    Unified Application Preferences view. Merges default configurations, 
    folder paths, and the Winetricks cache cleaner into a single unified menu.
    """
    toast_requested = Signal(str)
    update_catalog_requested = Signal()

    def __init__(self, db: ThatchDB, runners: list[str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.db = db
        self.runners = runners
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)
        
        # 1. Header Title
        lbl_title = QLabel("Preferences")
        lbl_title.setObjectName("ViewTitle")
        layout.addWidget(lbl_title)
        
        # 2. Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: transparent;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(16)
        
        # COMBINED CARD: Application Settings & Paths
        card_prefs = QFrame()
        card_prefs.setObjectName("PrefCard")
        prefs_layout = QVBoxLayout(card_prefs)
        prefs_layout.setSpacing(16)
        
        lbl_card_title = QLabel("Application Settings & Paths")
        lbl_card_title.setObjectName("CardTitle")
        prefs_layout.addWidget(lbl_card_title)
        
        # Form grid combining defaults and paths
        grid = QGridLayout()
        grid.setSpacing(14)
        
        # Row 0: Default Runner
        lbl_runner = QLabel("Default Runner:")
        lbl_runner.setObjectName("CardLabel")
        self.combo_runner = QComboBox()
        self._populate_runners_combo()
        self.combo_runner.currentTextChanged.connect(self._save_default_runner)
        grid.addWidget(lbl_runner, 0, 0)
        grid.addWidget(self.combo_runner, 0, 1, 1, 2)  # Span columns to match browse buttons
        
        # Row 1: Launch Action
        lbl_launch = QLabel("Launch Action:")
        lbl_launch.setObjectName("CardLabel")
        self.combo_launch = QComboBox()
        self.combo_launch.addItem("Close Thatch on Launch", "extreme")
        self.combo_launch.addItem("Minimize to System Tray", "stealth")
        self.combo_launch.addItem("Keep Thatch open in background", "keep")
        self.combo_launch.currentTextChanged.connect(self._save_launch_mode)
        grid.addWidget(lbl_launch, 1, 0)
        grid.addWidget(self.combo_launch, 1, 1, 1, 2)
        
        # Row 2: Default Terminal
        lbl_term = QLabel("Default Terminal:")
        lbl_term.setObjectName("CardLabel")
        self.combo_term = QComboBox()
        self.installed_terminals = self._scan_installed_terminals()
        self.combo_term.addItems(self.installed_terminals)
        self.combo_term.currentTextChanged.connect(self._save_default_terminal)
        grid.addWidget(lbl_term, 2, 0)
        grid.addWidget(self.combo_term, 2, 1, 1, 2)
        
        # Row 3: Chests Path
        lbl_path_pref = QLabel("Chests Path:")
        lbl_path_pref.setObjectName("CardLabel")
        self.txt_path_pref = QLineEdit(str(self.db.get_prefixes_dir()))
        self.txt_path_pref.setReadOnly(True)
        btn_path_pref = QPushButton("Browse")
        btn_path_pref.setCursor(Qt.PointingHandCursor)
        btn_path_pref.clicked.connect(self._browse_prefixes)
        grid.addWidget(lbl_path_pref, 3, 0)
        grid.addWidget(self.txt_path_pref, 3, 1)
        grid.addWidget(btn_path_pref, 3, 2)
        
        # Row 4: Runners Path
        lbl_path_run = QLabel("Runners Path:")
        lbl_path_run.setObjectName("CardLabel")
        self.txt_path_run = QLineEdit(str(self.db.get_runners_dir()))
        self.txt_path_run.setReadOnly(True)
        btn_path_run = QPushButton("Browse")
        btn_path_run.setCursor(Qt.PointingHandCursor)
        btn_path_run.clicked.connect(self._browse_runners)
        grid.addWidget(lbl_path_run, 4, 0)
        grid.addWidget(self.txt_path_run, 4, 1)
        grid.addWidget(btn_path_run, 4, 2)
        
        # Row 5: Winetricks Cache Path
        lbl_path_cache = QLabel("Winetricks Cache:")
        lbl_path_cache.setObjectName("CardLabel")
        self.txt_path_cache = QLineEdit(str(self.db.get_winetricks_cache_dir()))
        self.txt_path_cache.setReadOnly(True)
        btn_path_cache = QPushButton("Browse")
        btn_path_cache.setCursor(Qt.PointingHandCursor)
        btn_path_cache.clicked.connect(self._browse_cache)
        grid.addWidget(lbl_path_cache, 5, 0)
        grid.addWidget(self.txt_path_cache, 5, 1)
        grid.addWidget(btn_path_cache, 5, 2)
        
        prefs_layout.addLayout(grid)
        
        # Winetricks Cache stats & cleanup row
        self.cache_mgr_frame = QFrame()
        self.cache_mgr_frame.setStyleSheet("background-color: #121214; border: 1px solid #2d2d34; border-radius: 6px; padding: 12px;")
        cache_layout = QHBoxLayout(self.cache_mgr_frame)
        cache_layout.setContentsMargins(12, 8, 12, 8)
        
        lbl_cache_title = QLabel("Winetricks Cache size:")
        lbl_cache_title.setStyleSheet("color: #ffffff; font-size: 12px; font-weight: bold;")
        self.lbl_cache_size = QLabel("Scanning size...")
        self.lbl_cache_size.setStyleSheet("color: #8e8e93; font-size: 12px;")
        
        self.btn_update_catalog = QPushButton("🔄 Actualizar Catálogo Winetricks")
        self.btn_update_catalog.setCursor(Qt.PointingHandCursor)
        self.btn_update_catalog.setStyleSheet("padding: 4px 10px; font-size: 11px; color: #ffffff; background-color: #2563eb; border: none; border-radius: 4px; margin-right: 8px;")
        self.btn_update_catalog.clicked.connect(self.update_catalog_requested.emit)
        
        self.btn_clear_cache = QPushButton("Clear Cache")
        self.btn_clear_cache.setObjectName("RedBtnText")
        self.btn_clear_cache.setCursor(Qt.PointingHandCursor)
        self.btn_clear_cache.setStyleSheet("padding: 4px 10px; font-size: 11px;")
        self.btn_clear_cache.clicked.connect(self._clear_winetricks_cache)
        
        cache_layout.addWidget(lbl_cache_title)
        cache_layout.addWidget(self.lbl_cache_size)
        cache_layout.addStretch(1)
        cache_layout.addWidget(self.btn_update_catalog)
        cache_layout.addWidget(self.btn_clear_cache)
        prefs_layout.addWidget(self.cache_mgr_frame)
        
        # Static System Details
        lbl_specs_title = QLabel("System Details")
        lbl_specs_title.setStyleSheet("color: #ffffff; font-size: 13px; font-weight: bold; margin-top: 10px;")
        prefs_layout.addWidget(lbl_specs_title)
        
        lbl_specs = QLabel(
            "Thatch Version: 1.0.0 (Native Core)\n"
            "Wine Engine Compatibility: Proton / Soda / System Wine\n"
            "Winetricks Client Version: Latest (Auto-updates via WINEPREFIX)"
        )
        lbl_specs.setStyleSheet("color: #71717a; font-size: 12px; line-height: 18px;")
        prefs_layout.addWidget(lbl_specs)
        
        scroll_layout.addWidget(card_prefs)
        scroll_layout.addStretch(1)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, stretch=1)
        
        # Initial loads
        self._load_config_vals()
        self._refresh_cache_size()

    def _populate_runners_combo(self) -> None:
        self.combo_runner.clear()
        if self.runners:
            self.combo_runner.addItems(self.runners)
        self.combo_runner.addItem("Wine del Sistema (/usr/bin/wine)")

    def _load_config_vals(self) -> None:
        """Prefills UI components with active db values."""
        # Launch action mode
        launch_mode = self.db.get_launch_mode()
        idx = self.combo_launch.findData(launch_mode)
        if idx != -1:
            self.combo_launch.setCurrentIndex(idx)
            
        # Default runner
        default_runner = self.db.data["global_config"].get("default_runner", "")
        if default_runner:
            idx_run = self.combo_runner.findText(default_runner)
            if idx_run != -1:
                self.combo_runner.setCurrentIndex(idx_run)

        # Default terminal
        default_term = self.db.data["global_config"].get("default_terminal", "")
        if default_term:
            idx_term = self.combo_term.findText(default_term)
            if idx_term != -1:
                self.combo_term.setCurrentIndex(idx_term)

    def _scan_installed_terminals(self) -> list[str]:
        import shutil
        terminals = ["gnome-terminal", "konsole", "alacritty", "kitty", "xfce4-terminal", "xterm", "tilix"]
        installed = []
        for term in terminals:
            if shutil.which(term):
                installed.append(term)
        if not installed:
            installed.append("xterm")
        return installed

    @Slot()
    def _save_default_terminal(self) -> None:
        self.db.data["global_config"]["default_terminal"] = self.combo_term.currentText()
        self.db.save()

    def update_runners_list(self, runners: list[str]) -> None:
        """Externally updates the list of installed wine runners."""
        self.runners = runners
        self._populate_runners_combo()
        self._load_config_vals()

    def _refresh_cache_size(self) -> None:
        """Calculates disk space taken up by winetricks cache folder."""
        cache_path = self.db.get_winetricks_cache_dir()
        if not cache_path.exists():
            self.lbl_cache_size.setText("0 B")
            return
            
        try:
            total_bytes = sum(f.stat().st_size for f in cache_path.glob('**/*') if f.is_file())
            if total_bytes == 0:
                self.lbl_cache_size.setText("0 B")
            else:
                size_names = ("B", "KB", "MB", "GB", "TB")
                i = int(math.floor(math.log(total_bytes, 1024)))
                p = math.pow(1024, i)
                s = round(total_bytes / p, 2)
                self.lbl_cache_size.setText(f"{s} {size_names[i]}")
        except Exception as e:
            self.lbl_cache_size.setText("Unknown size")
            print(f"Error calculating cache size: {e}")

    @Slot()
    def _clear_winetricks_cache(self) -> None:
        cache_path = self.db.get_winetricks_cache_dir()
        if not cache_path.exists() or not any(cache_path.iterdir()):
            QMessageBox.information(self, "Cache Empty", "Winetricks cache is already empty.")
            return
            
        confirm = QMessageBox.question(
            self, "Clear Winetricks Cache",
            f"Are you sure you want to delete all cached files in {cache_path}?\nThis will remove installers that need to be re-downloaded next time you inject dependencies.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                for item in cache_path.iterdir():
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                self._refresh_cache_size()
                self.toast_requested.emit("Winetricks cache cleared successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to clear cache: {e}")

    @Slot()
    def _save_default_runner(self) -> None:
        self.db.data["global_config"]["default_runner"] = self.combo_runner.currentText()
        self.db.save()

    @Slot()
    def _save_launch_mode(self) -> None:
        mode = self.combo_launch.currentData()
        self.db.set_launch_mode(mode)

    @Slot()
    def _browse_prefixes(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Chests Directory", self.txt_path_pref.text())
        if path:
            self.txt_path_pref.setText(path)
            self.db.set_prefixes_dir(path)
            self.toast_requested.emit("Chests directory updated successfully.")

    @Slot()
    def _browse_runners(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Wine Runners Directory", self.txt_path_run.text())
        if path:
            self.txt_path_run.setText(path)
            self.db.set_runners_dir(path)
            self.toast_requested.emit("Wine runners directory updated successfully.")

    @Slot()
    def _browse_cache(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Winetricks Cache Directory", self.txt_path_cache.text())
        if path:
            self.txt_path_cache.setText(path)
            self.db.set_winetricks_cache_dir(path)
            self._refresh_cache_size()
            self.toast_requested.emit("Winetricks cache directory updated successfully.")
