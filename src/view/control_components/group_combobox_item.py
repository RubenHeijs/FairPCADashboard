from PySide6.QtWidgets import  QWidget, QHBoxLayout, QLabel, QCheckBox
from PySide6.QtGui import QPalette
from PySide6.QtCore import Signal, QObject, Slot

class GroupComboboxItem(QWidget):
    """Whatever custom widget you want per row."""
    delete_requested = Signal(object)
    item_changed = Signal()
    def __init__(self, group, parent=None):
        super().__init__(parent)
        self.group_data = group.get_summary_data()
        group.color_changed.connect(self.on_color_changed)
        group.delete_requested.connect(self.on_delete_requested)
        group.group_changed.connect(self.on_group_changed)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)

        self.name_label = QLabel(group.get_label())
        self.name_palette = self.name_label.palette()
        self.name_palette.setColor(QPalette.ColorRole.Text,group.get_color())
        self.name_label.setPalette(self.name_palette)
        self.checkbox = QCheckBox("")
        self.checkbox.setChecked(False)
        self.checkbox.checkStateChanged.connect(self.on_check_state_changed)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.name_label)
        
        layout.addStretch()
    def on_check_state_changed(self):
        self.item_changed.emit()
    def on_group_changed(self, summary_data):
        self.group_data = summary_data
        if self.is_checked():
            self.item_changed.emit()
    
    def on_delete_requested(self):
        self.delete_requested.emit(self)
    def on_color_changed(self, color):
        self.name_palette.setColor(QPalette.ColorRole.Text,color)
        self.name_label.setPalette(self.name_palette)

    def mousePressEvent(self, event):
        self.checkbox.setChecked(not self.checkbox.isChecked())
        #print(event)
    def is_checked(self):
        return self.checkbox.isChecked()
    
    def get_group_data(self):
        return self.group_data