from ..widgets.header.project_picker import ProjectPicker
from ..icons.icons import WoodyIcon

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class Header(QWidget):
    def __init__(self, asset_browser, parent=None):
        super().__init__(parent)
        
        self.asset_browser = asset_browser
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        
        self.setMinimumHeight(60)
        self.setMaximumHeight(60)
    
        self.add_widgets()
        self.layout_widgets()
    
    def add_widgets(self):
        self.logo = QLabel()
        logo_image = QPixmap(WoodyIcon.HEADER.path)
        logo_image = logo_image.scaled(130, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(logo_image)
        
        self.projects_label = QLabel("<b>Current Project:</b>")
        
    def layout_widgets(self):
        self.layout.addWidget(self.logo)
        self.layout.addStretch()
        self.layout.addWidget(self.projects_label)
        self.layout.addWidget(ProjectPicker(self.asset_browser))