from woody.pywoody.handlers.processor import Processor
from woody.pywoody.core.console import quiet
from woody.pywoody.objects.guard import Guard

from PySide6.QtWidgets import QWidget, QComboBox, QHBoxLayout

class ProjectPicker(QWidget):
    guard = Guard()
    
    def __init__(self, asset_browser, parent=None):
        super().__init__(parent)
        
        self.asset_browser = asset_browser
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.setMinimumWidth(125)
        
        self.combo_box = QComboBox()
        self.get_projects()
        self.combo_box.setCurrentText(self.guard._current_project)
        self.combo_box.currentTextChanged.connect(self.on_project_selected)
        
        self.combo_box.setToolTip("Select a project to work on")
        
        self.layout.addWidget(self.combo_box)
    
    @quiet    
    def get_projects(self):
        projects = Processor().list_projects()
        self.combo_box.addItems(projects)
        
    def on_project_selected(self, project_name):
        Processor().switch_projects(project_name)
        self.asset_browser.clear()