from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLineEdit

class ListBox(QWidget):
    def __init__(self, searchable=False, parent=None):
        super().__init__(parent)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)
        
        self.items_cache = [] 
        
        self.search_box = None
        if searchable:
            self.search_box = QLineEdit()
            self.search_box.setPlaceholderText("Search...")
            self.search_box.setClearButtonEnabled(True)
            self.search_box.textChanged.connect(self._filter_items)
            self.main_layout.addWidget(self.search_box)

        self.list_widget = QListWidget()
        self.main_layout.addWidget(self.list_widget)
        
        self.clear()

    def add_items(self, items: list):
        self.items_cache = items
        self._refresh_list_display(items)
        self.enable()
        
        if self.search_box:
            self.search_box.blockSignals(True)
            self.search_box.clear()
            self.search_box.blockSignals(False)
            
    def _filter_items(self, text):
        search_text = text.lower()
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setHidden(search_text not in item.text().lower())

    def _refresh_list_display(self, items):
        self.list_widget.clear()
        if not items:
            self.list_widget.addItems(["No items"])
            self.disable()
        else:
            self.list_widget.addItems(items)
            self.enable()

    def enable(self):
        self.list_widget.setEnabled(True)
        if self.search_box:
            self.search_box.setEnabled(True)
    
    def disable(self):
        self.list_widget.setEnabled(False)
        if self.search_box:
            self.search_box.setEnabled(False)
        
    def clear(self):
        self.items_cache = []
        self._refresh_list_display([])