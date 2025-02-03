from abc import ABC, abstractmethod
from typing import Union, Iterable, Dict, List

from web_gui_generator.model.w_descr import ContWidgetDescr, \
    WidgetDescrMixin
from web_gui_generator.model.w_descr_holder import DescrHolder, WidgetDescrEnum

WOUnion = Union['AtomicWOMixin', 'CompWOMixin', 'ContWOMixin', 'WOMixin']
ContCompWOUnion = Union['ContWOMixin', 'CompWOMixin']


class WOMixin(ABC):
    @abstractmethod
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion):
        self._name = name
        self._id = id_
        self._parent = parent
        if parent is not None:
            parent.add_child(self)

    def set_parent(self, parent: ContCompWOUnion):
        self._parent = parent

    def _get_respective_wo_description(self, description_enum: WidgetDescrEnum):
        description = DescrHolder.get_instance().get_descr_dict(description_enum).get_descr(self._name)
        if isinstance(description, description_enum.get_type()):
            return description
        else:
            raise RuntimeError("Wrong conf is returned")

    @property
    def id_(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> ContCompWOUnion:
        return self._parent

    @property
    @abstractmethod
    def widget_object_description(self) -> WidgetDescrMixin:
        pass

    @abstractmethod
    def get_children_count(self):
        pass


class AtomicWOMixin(WOMixin):
    @abstractmethod
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion):
        super().__init__(id_, name, parent)
        self._widget_object_description \
            = self._get_respective_wo_description(WidgetDescrEnum.ATOMIC)

    @property
    def widget_object_description(self):
        return self._widget_object_description

    def get_children_count(self) -> int:
        return 0


class CompWOMixin(WOMixin):
    @abstractmethod
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion, children: Iterable[WOUnion]):
        super().__init__(id_, name, parent)
        self._children: Dict[int, WOUnion] = {ch.id_: ch for ch in children}
        self.set_self_as_parent_for_children(children)
        self._widget_object_description = self._get_respective_wo_description(WidgetDescrEnum.COMP)

    def set_self_as_parent_for_children(self, children):
        for child in children:
            child.set_parent(self)

    @property
    def children(self) -> List[WOUnion]:
        return list(self._children.values())

    def get_content_item(self, id_: int) -> WOUnion:
        return self._children[id_]

    @property
    def widget_object_description(self):
        return self._widget_object_description

    def get_children_count(self) -> int:
        cnt = len(self._children.values())
        for child in self._children.values():
            cnt += child.get_children_count()
        return cnt


class ContWOMixin(WOMixin):
    @abstractmethod
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion, children: Iterable[WOUnion]):
        super().__init__(id_, name, parent)
        self._children: Dict[int, WOUnion] = {ch.id_: ch for ch in children}
        self.set_self_as_parent_for_children(children)
        self._widget_object_description = self._get_respective_wo_description(WidgetDescrEnum.CONT)

    def set_self_as_parent_for_children(self, children):
        for child in children:
            child.set_parent(self)

    @property
    def children(self) -> List[WOUnion]:
        return list(self._children.values())

    def get_child(self, id_: int) -> WOUnion:
        return self._children[id_]

    def add_child(self, child: WOUnion) -> bool:
        elem_belongs = child.id_ in self._children.keys()
        if not elem_belongs:
            self._children[child.id_] = child
            child.set_parent(self)
        return elem_belongs

    @property
    def widget_object_description(self):
        return self._widget_object_description

    def get_children_count(self) -> int:
        cnt = len(self._children.values())
        for child in self._children.values():
            cnt += child.get_children_count()
        return cnt
