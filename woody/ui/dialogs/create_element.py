from woody.pywoody.handlers.processor import Processor
from woody.pywoody.objects.guard import Guard
from woody.pywoody.core.console import quiet
from ..icons.icons import WoodyIcon
from ..widgets.list_box import ListBox
from ..widgets.separators import create_hline

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class CreateElement(QDialog):
    guard = Guard()
    
    def __init__(self, type, group_selection, parent=None):
        super().__init__(parent)
        
        self.type = type
        self.tree = self.guard._context.get("tree")
        self.group_selection = group_selection
        
        if self.tree == "assets":
            self.group = "Groups"
        elif self.tree == "shots":
            self.group = "Sequences"
        
        self.processor = Processor()
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        self.setWindowTitle(f"Create New {self.type}")
        self.setWindowIcon(QIcon(WoodyIcon.ICON.path))
        self.setFixedSize(300, 400)
        
        self.add_widgets()
        self.layout_widgets()
        self.connections()
        self._get_groups()
        
    def add_widgets(self):
        self.title_label = QLabel(f"<h3>Create {self.type}</h3>")
        
        self.group_row_layout = QHBoxLayout()
        
        self.group_label = QLabel(f"<h4>Avalible {self.group}:</h4>")
        
        icon = QIcon(WoodyIcon.CREATE_GROUP.path)
        self.new_group_button = QPushButton(icon, f"New {self.group[:-1]}")
        self.new_group_button.setFixedWidth(130)
        self.new_group_button.setAutoDefault(False)
        self.new_group_button.setDefault(False)
        
        self.group_list_box = ListBox(searchable=True)
        
        self.element_label = QLabel(f"<h4>New {self.type} Name:</h4>")
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(f"{self.type} Name...")
        
        self.btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Create")
        self.cancel_btn = QPushButton("Cancel")
        
    def layout_widgets(self):
        self.group_row_layout.addWidget(self.group_label)
        self.group_row_layout.addWidget(self.new_group_button)
        self.btn_layout.addWidget(self.ok_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(create_hline())
        self.layout.addLayout(self.group_row_layout)
        self.layout.addWidget(self.group_list_box)
        self.layout.addWidget(self.element_label)
        self.layout.addWidget(self.name_input)
        self.layout.addLayout(self.btn_layout)
        
    def connections(self):
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
    
    @quiet    
    def _get_groups(self):
        groups = self.processor.list_groups(self.tree)
        self.group_list_box.add_items(groups)

        items = self.group_list_box.list_widget.findItems(self.group_selection, Qt.MatchExactly)
        if items:
            self.group_list_box.list_widget.setCurrentItem(items[0])

    def create_element(self):
        group_selection = self.group_list_box.list_widget.currentItem().text()
        name = self.name_input.text()
        
        if self.tree == "assets":
            return self.processor.create_asset(group_selection, name)
        elif self.tree == "shots":
            return self.processor.create_shot(group_selection, name)