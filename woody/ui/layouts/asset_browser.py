from woody.pywoody.objects.guard import Guard
from woody.pywoody.handlers.processor import Processor
from woody.pywoody.core.console import quiet
from ..dialogs.create_element import CreateElement
from ..widgets.list_box import ListBox
from ..widgets.separators import create_hline
from ..icons.icons import WoodyIcon

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication, QStyle
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class AssetBrowser(QWidget):
    guard = Guard()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.processor = Processor()
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)
        
        self.setMinimumWidth(200)
        self.setMaximumWidth(400)
    
        self.add_widgets()
        self.layout_widgets()
        self.connections()
        self.jump_to_context()

    
    def add_widgets(self):  
        self.projects_label = QLabel("<h3>Asset Browser:</h3>")
        self.projects_label.setStyleSheet("padding-left: 2px; padding-top: 5px; padding-bottom: 5px;")
        
        self.tree_label = QLabel("<h4>Tree:</h4>")
        self.tree_label.setStyleSheet("padding-left: 2px;")
        self.tree_list_box = ListBox()
        self.tree_list_box.list_widget.setMaximumHeight(70)
        self.tree_list_box.list_widget.setMinimumHeight(70)
        self.tree_list_box.add_items(["assets", "shots"])
        self.tree_list_box.enable()
        
        self.group_label = QLabel("<h4>Group:</h4>")
        self.group_label.setStyleSheet("padding-left: 2px;")
        self.group_list_box = ListBox(searchable=True)
        
        self.asset_row_layout = QHBoxLayout()
        self.asset_label = QLabel("<h4>Asset:</h4>")
        self.asset_label.setStyleSheet("padding-left: 2px;")
        icon = QIcon(WoodyIcon.CREATE_ELEMENT.path)
        self.create_element_button = QPushButton(icon, "Create Asset")
        self.create_element_button.setFixedWidth(110)
        self.create_element_button.setEnabled(False)
        self.asset_list_box = ListBox(searchable=True)
        
    def layout_widgets(self):
        self.layout.addWidget(self.projects_label)
        self.layout.addWidget(create_hline())
        self.layout.addWidget(self.tree_label)
        self.layout.addWidget(self.tree_list_box)
        self.layout.addWidget(self.group_label)
        self.layout.addWidget(self.group_list_box)
        self.layout.addLayout(self.asset_row_layout)
        self.asset_row_layout.addWidget(self.asset_label)
        self.asset_row_layout.addWidget(self.create_element_button)
        self.layout.addWidget(self.asset_list_box)
        
        self.layout.setStretchFactor(self.tree_list_box, 0)
        self.layout.setStretchFactor(self.group_list_box, 1)
        self.layout.setStretchFactor(self.asset_list_box, 1)
            
    def connections(self):
        self.tree_list_box.list_widget.itemClicked.connect(self._on_tree)
        self.group_list_box.list_widget.itemClicked.connect(self._on_group)
        self.asset_list_box.list_widget.itemClicked.connect(self._on_asset)
        self.create_element_button.clicked.connect(self._on_create_element)
        
    def jump_to_context(self):
        context = self.guard._context
        tree = context.get("tree")
        group = context.get("group")
        asset = context.get("asset")

        if not tree:
            return

        tree_items = self.tree_list_box.list_widget.findItems(tree, Qt.MatchExactly)
        if not tree_items:
            return
        self.tree_list_box.list_widget.setCurrentItem(tree_items[0])
        self._on_tree(tree_items[0])

        if not group:
            return

        group_items = self.group_list_box.list_widget.findItems(group, Qt.MatchExactly)
        if not group_items:
            return
        self.group_list_box.list_widget.setCurrentItem(group_items[0])
        self._on_group(group_items[0])

        if not asset:
            return

        asset_items = self.asset_list_box.list_widget.findItems(asset, Qt.MatchExactly)
        if not asset_items:
            return
        self.asset_list_box.list_widget.setCurrentItem(asset_items[0])
        self._on_asset(asset_items[0])
        
    def clear(self):
        self.group_list_box.clear()
        self.asset_list_box.clear()
    
    @quiet   
    def _on_tree(self, item):
        if hasattr(item, "text"):
            self.tree = item.text()
        else:
            self.tree = str(item)
            
        groups = self.processor.list_groups(self.tree)
        self.processor.clear_context()
        self.processor.set_context([self.tree])
        
        self.create_element_button.setEnabled(False)
        
        if groups:
            self.group_list_box.enable()
            self.group_list_box.add_items(groups)
            self.asset_list_box.clear()
        else:
            self.group_list_box.clear()
            self.asset_list_box.clear()
            
        if self.tree == "assets":
            self.group_label.setText("<h4>Group:</h4>")
            self.asset_label.setText("<h4>Asset:</h4>")
            self.create_element_button.setText("Create Asset")
        elif self.tree == "shots":
            self.group_label.setText("<h4>Sequence:</h4>")
            self.asset_label.setText("<h4>Shots:</h4>")
            self.create_element_button.setText("Create Shot")
    
    @quiet        
    def _on_group(self, item):
        if hasattr(item, "text"):
            self.group = item.text()
        else:
            self.group = str(item)
            
        names = self.processor.list_names(self.tree, self.group)
        self.processor.clear_context()
        self.processor.set_context([self.tree, self.group])
        
        if names:
            self.asset_list_box.enable()
            self.asset_list_box.add_items(names)
            self.create_element_button.setEnabled(True)
        else:
            self.asset_list_box.clear()
    
    @quiet        
    def _on_asset(self, item):
        if hasattr(item, "text"):
            self.asset = item.text()
        else:
            self.asset = str(item)
                             
        self.processor.clear_context()
        self.processor.set_context([self.tree, self.group, self.asset])
        
    def _on_create_element(self):
        if self.tree == "assets":
            tree = "Asset"
        elif self.tree == "shots":
            tree = "Shot"
            
        group_selection = self.group_list_box.list_widget.currentItem().text()
            
        dialog = CreateElement(tree, group_selection)
        
        if dialog.exec(): 
            dialog.create_element()