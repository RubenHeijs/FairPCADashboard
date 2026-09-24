from PySide6.QtWidgets import (
    QComboBox, QStyledItemDelegate, QStyleOptionComboBox, QStyle, QAbstractItemView, 

)
from src.view.control_components.group_combobox_item import GroupComboboxItem
from PySide6.QtGui import QStandardItemModel, QStandardItem, QPainter 
from PySide6.QtCore import Qt, QEvent, QModelIndex, Signal

class NoHighlightDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.state &= ~QStyle.State_Selected
        option.state &= ~QStyle.State_HasFocus
        super().paint(painter, option, index)
class GroupComboBox(QComboBox):
    groups_changed = Signal(object)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(QStandardItemModel(self))
        # Give it a delegate just so row sizing behaves
        self.setItemDelegate(QStyledItemDelegate(self))
        self.setItemDelegate(NoHighlightDelegate(self))
        self.view().viewport().installEventFilter(self)
        self.view().setSelectionMode(QAbstractItemView.NoSelection)
        self.view().setFocusPolicy(Qt.NoFocus)
        self.view().setCurrentIndex(QModelIndex())

    def add_group_widget(self, widget: GroupComboboxItem, data=None):
        item = QStandardItem()
        item.setSizeHint(widget.sizeHint())
        item.setData(data, Qt.UserRole)
        self.model().appendRow(item)
        index = self.model().index(self.model().rowCount() - 1, 0)
        self.view().setIndexWidget(index, widget)
        widget.delete_requested.connect(self.on_widget_delete_requested)
        widget.item_changed.connect(self.broadcast_groups)
        self.broadcast_groups()

    def on_widget_delete_requested(self, widget):
        for row in range(self.model().rowCount()):
            index = self.model().index(row, 0)
            if self.view().indexWidget(index) is widget:
                self.model().removeRow(row)
                break
        self.broadcast_groups()

    def broadcast_groups(self):
        self.groups_changed.emit(self.get_current_groups())

    def get_current_groups(self):
        groups = []
        for row in range(self.model().rowCount()):
            index = self.model().index(row, 0)
            group_widget = self.view().indexWidget(index)
            if group_widget.is_checked():
                groups.append(group_widget.get_group_data())
        return groups
    
    def eventFilter(self, obj, event):
        if obj is self.lineEdit() and event.type() == QEvent.MouseButtonPress:
            print('click2')
            self.showPopup()
            return True
        if obj == self.view().viewport() and event.type() == QEvent.MouseButtonRelease:
            print('click')
            return True  # eat the event so popup doesn't close
        return super().eventFilter(obj, event)

    def showPopup(self):
        super().showPopup()
        self.view().setCurrentIndex(QModelIndex())

    def paintEvent(self, event):
        painter = QPainter(self)
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        opt.currentText = "Select groups:"
        self.style().drawComplexControl(QStyle.CC_ComboBox, opt, painter, self)
        self.style().drawControl(QStyle.CE_ComboBoxLabel, opt, painter, self)