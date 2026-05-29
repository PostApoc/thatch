from PySide6.QtGui import QFont, QPalette, QColor
from PySide6.QtWidgets import QApplication

# Minimalist Flat Dark QSS Stylesheet
# Clean lines, high contrast, subtle borders, and zero flashy glowing neons.
STYLESHEET = """
QMainWindow {
    background-color: #121212;
}

/* Sidebar Styling - Pure flat minimal */
QFrame#SidebarFrame {
    background-color: #161616;
    border-right: 1px solid #242424;
}

QLabel#SidebarTitle {
    color: #ffffff;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.5px;
    padding: 12px 16px;
    margin-bottom: 8px;
}

QPushButton#SidebarBtn {
    background-color: transparent;
    border: none;
    border-radius: 4px;
    padding: 10px 16px;
    color: #8e8e93;
    font-size: 13px;
    font-weight: bold;
    text-align: left;
}
QPushButton#SidebarBtn:hover {
    background-color: #242424;
    color: #ffffff;
}
QPushButton#SidebarBtn:checked {
    background-color: #2c2c2e;
    color: #ffffff;
    border-left: 2px solid #ffffff;
}

/* Main Content Area */
QLabel#ViewTitle {
    color: #ffffff;
    font-size: 22px;
    font-weight: bold;
}

/* Flat Cards & Panels */
QFrame#ChestCard, QFrame#AppCard, QFrame#DetailCard, QFrame#PrefCard {
    background-color: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 8px;
    padding: 16px;
}
QFrame#ChestCard:hover, QFrame#AppCard:hover {
    background-color: #242426;
    border: 1px solid #3a3a3c;
}

QLabel#CardTitle {
    color: #ffffff;
    font-size: 15px;
    font-weight: bold;
}

QLabel#CardLabel {
    color: #8e8e93;
    font-size: 12px;
}

QLabel#CardValue {
    color: #e5e5ea;
    font-size: 12px;
}

/* Minimal Flat Badges */
QLabel#BadgeReady {
    background-color: #1c1c1e;
    color: #30d158;
    border: 1px solid #30d158;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: bold;
}

QLabel#BadgeStopped {
    background-color: #1c1c1e;
    color: #8e8e93;
    border: 1px solid #48484a;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: bold;
}

QLabel#BadgePlatinum {
    color: #ffd60a;
    font-weight: bold;
    font-size: 11px;
}

QLabel#BadgeGold {
    color: #ff9f0a;
    font-weight: bold;
    font-size: 11px;
}

QLabel#BadgeSilver {
    color: #aeaeb2;
    font-weight: bold;
    font-size: 11px;
}

QLabel#AppTag {
    background-color: #2c2c2e;
    color: #d1d1d6;
    border-radius: 3px;
    padding: 2px 6px;
    font-size: 10px;
    font-weight: bold;
}

/* Flat Inputs & Comboboxes */
QLineEdit, QComboBox {
    background-color: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 6px;
    padding: 8px 12px;
    color: #ffffff;
    font-size: 12px;
}
QLineEdit:focus, QComboBox:hover {
    border: 1px solid #48484a;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 4px solid #8e8e93;
    margin-top: 2px;
    margin-right: 6px;
}
QComboBox QAbstractItemView {
    background-color: #1c1c1e;
    border: 1px solid #2c2c2e;
    selection-background-color: #2c2c2e;
    selection-color: #ffffff;
    color: #ffffff;
}

/* Minimalist Flat Buttons */
QPushButton {
    background-color: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 6px;
    padding: 8px 14px;
    color: #ffffff;
    font-size: 12px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #242426;
    border: 1px solid #3a3a3c;
}
QPushButton:pressed {
    background-color: #121212;
}
QPushButton:disabled {
    background-color: #121212;
    color: #48484a;
    border: 1px solid #1c1c1e;
}

/* Accent Buttons */
QPushButton#BlueBtn {
    background-color: #0a84ff;
    color: #ffffff;
    border: 1px solid #0a84ff;
}
QPushButton#BlueBtn:hover {
    background-color: #007aff;
    border: 1px solid #007aff;
}

/* Orange/Run Buttons */
QPushButton#OrangeBtn {
    background-color: #ff9f0a;
    color: #ffffff;
    border: 1px solid #ff9f0a;
}
QPushButton#OrangeBtn:hover {
    background-color: #ff453a;
    border: 1px solid #ff453a;
}

/* Red/Delete Buttons */
QPushButton#RedBtn {
    background-color: #ff453a;
    color: #ffffff;
    border: 1px solid #ff453a;
}
QPushButton#RedBtn:hover {
    background-color: #ff3b30;
}
QPushButton#RedBtnText {
    background-color: transparent;
    border: 1px solid #2c2c2e;
    color: #ff453a;
}
QPushButton#RedBtnText:hover {
    background-color: #1c1c1e;
    border: 1px solid #ff453a;
}

/* Flat tab buttons in Chest Details */
QPushButton#TabBtn {
    background-color: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    border-radius: 0px;
    padding: 8px 12px;
    color: #8e8e93;
    font-size: 13px;
    font-weight: bold;
}
QPushButton#TabBtn:hover {
    color: #ffffff;
}
QPushButton#TabBtn:checked {
    color: #ffffff;
    border-bottom: 2px solid #ffffff;
}

/* Stepper Stepper Circles */
QLabel#StepCircleActive {
    background-color: #2c2c2e;
    color: #ffffff;
    border: 1px solid #ffffff;
    border-radius: 12px;
    font-weight: bold;
    font-size: 12px;
    min-width: 24px;
    min-height: 24px;
    max-width: 24px;
    max-height: 24px;
    alignment: center;
}

QLabel#StepCircleInactive {
    background-color: #1c1c1e;
    color: #48484a;
    border: 1px solid #2c2c2e;
    border-radius: 12px;
    font-weight: bold;
    font-size: 12px;
    min-width: 24px;
    min-height: 24px;
    max-width: 24px;
    max-height: 24px;
    alignment: center;
}

QLabel#StepLine {
    background-color: #2c2c2e;
    max-height: 1px;
    min-height: 1px;
}

/* ScrollBars */
QScrollBar:vertical {
    border: none;
    background: #121212;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #2c2c2e;
    min-height: 30px;
    border-radius: 4px;
}
QScrollBar::handle:vertical:hover {
    background: #3a3a3c;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Toast/Snackbar Frame */
QFrame#ToastFrame {
    background-color: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 6px;
    padding: 8px 12px;
}

/* Progress bar */
QProgressBar {
    border: 1px solid #2c2c2e;
    border-radius: 4px;
    text-align: center;
    background-color: #121212;
    color: #ffffff;
    font-weight: bold;
    height: 20px;
}
QProgressBar::chunk {
    background-color: #30d158;
}

/* List Widgets inside Panels */
QListWidget {
    background-color: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 6px;
    padding: 4px;
    color: #e5e5ea;
}
QListWidget::item {
    background-color: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 4px;
    padding: 8px;
    margin-bottom: 4px;
    color: #e5e5ea;
}
QListWidget::item:hover {
    background-color: #242426;
}
QListWidget::item:selected {
    background-color: #2c2c2e;
    border: 1px solid #48484a;
    color: #ffffff;
    font-weight: bold;
}

/* Checkboxes */
QCheckBox {
    color: #e5e5ea;
    font-size: 12px;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #2c2c2e;
    border-radius: 3px;
    background-color: #1c1c1e;
}
QCheckBox::indicator:hover {
    border: 1px solid #48484a;
}
QCheckBox::indicator:checked {
    background-color: #2c2c2e;
    border: 1px solid #ffffff;
}

/* Log / Console area */
QTextEdit#ConsoleLog {
    background-color: #000000;
    border: 1px solid #2c2c2e;
    border-radius: 6px;
    color: #e5e5ea;
    font-family: 'Courier New', monospace;
    font-size: 11px;
    padding: 8px;
}
"""

def apply_theme(app: QApplication) -> None:
    """Applies the purely minimalist dark theme to the Qt App."""
    font = QFont("Inter", 10)
    if not font.exactMatch():
        font = QFont("Noto Sans", 9)
    app.setFont(font)
    
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#121212"))
    palette.setColor(QPalette.WindowText, QColor("#ffffff"))
    palette.setColor(QPalette.Base, QColor("#1c1c1e"))
    palette.setColor(QPalette.AlternateBase, QColor("#121212"))
    palette.setColor(QPalette.ToolTipBase, QColor("#121212"))
    palette.setColor(QPalette.ToolTipText, QColor("#ffffff"))
    palette.setColor(QPalette.Text, QColor("#e5e5ea"))
    palette.setColor(QPalette.Button, QColor("#1c1c1e"))
    palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
    palette.setColor(QPalette.BrightText, QColor("#ffffff"))
    palette.setColor(QPalette.Highlight, QColor("#2c2c2e"))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)
    
    app.setStyleSheet(STYLESHEET)
