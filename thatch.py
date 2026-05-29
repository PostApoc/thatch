#!/usr/bin/env python3
import sys
from pathlib import Path

# Add src/ folder to Python module search paths
src_dir = Path(__file__).parent.resolve() / "src"
sys.path.insert(0, str(src_dir))

from PySide6.QtWidgets import QApplication
from main import ThatchLauncher
from style import apply_theme

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_theme(app)
    gui = ThatchLauncher()
    gui.show()
    sys.exit(app.exec())