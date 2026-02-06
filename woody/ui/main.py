from .style import COLOURS, BORDER
from .layouts.header import Header
from .layouts.asset_browser import AssetBrowser
from .icons.icons import WoodyIcon

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGridLayout
from PySide6.QtGui import QIcon
import sys

class WoodyUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Woody")
        self.resize(1400,800)
 
        self.setWindowIcon(QIcon(WoodyIcon.ICON.path))
        
        self.add_widgets()
        self.layout()
        self.stylesheet()
        
    def stylesheet(self):
        self.setStyleSheet(f"""  
            QMainWIndow {{
                background-color: {COLOURS["theme_bg"]};    
            }}            
            QWidget#header {{
                background-color: {COLOURS["theme_bg"]};
                border-radius: {BORDER["radius"]};
                border: {BORDER["thickness"]} {COLOURS["theme"]};
            }}
            QWidget#asset_browser {{
                background-color: {COLOURS["theme_bg"]};
                border-radius: {BORDER["radius"]};
                border: {BORDER["thickness"]} {BORDER["colour"]};
            }}
        """)
        
    def add_widgets(self):
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.grid_layout = QGridLayout()
        
        self.asset_browser = AssetBrowser()
        self.asset_browser.setObjectName("asset_browser")
        self.header = Header(self.asset_browser)
        self.header.setObjectName("header")
    
    def layout(self):
        self.setCentralWidget(self.central_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        self.main_layout.addWidget(self.header)
        self.grid_layout.setSpacing(10)
        self.grid_layout.addWidget(self.asset_browser, 0, 0)
        self.main_layout.addLayout(self.grid_layout)
        
def run_ui():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    
    window = WoodyUI()
    window.show()

    app.exec()