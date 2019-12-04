from anytree import NodeMixin
from anytree.exporter import DictExporter
import uuid


class BizDataNode(NodeMixin):

    def __init__(self, name: str = '', value: str = '', parent=None, subset_filter: dict = None):
        self.subset_filter = subset_filter
        self.name = name
        self.value = value
        self.parent = parent
        self.id = uuid.uuid1().hex

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str((self.id, self.name, self.value, self.subset_filter))

    def tree_to_dict(self):
        return DictExporter().export(self)
