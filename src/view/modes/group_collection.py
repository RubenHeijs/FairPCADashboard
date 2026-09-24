from PySide6.QtCore import QObject, Slot, Signal

class GroupCollection(QObject):
    group_added = Signal(object)
    group_changed = Signal(object)
    group_removed = Signal(object)
    def __init__(self):
        super(GroupCollection,self).__init__()
        self.groups = []
        self.group_pv_samplers = []

    def add_group(self, group, group_pv_sampler):
        self.groups.append(group)
        self.group_pv_samplers.append(group_pv_sampler)
        group.delete_requested.connect(self.on_group_delete_requested)
        self.group_added.emit(group)

    @Slot(object)
    def on_group_delete_requested(self, group):
        index = self.groups.index(group)
        del self.groups[index]
        del self.group_pv_samplers[index]
        self.group_removed.emit(group)

    def on_group_changed(self, group):
        self.group_changed.emit(group)

    def get_groups(self):
        return self.groups