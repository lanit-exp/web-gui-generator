from enum import Enum
from typing import Dict, Iterable, List

from web_gui_generator import Singleton, fileproc, CONF_PATH
from web_gui_generator.model.w_descr import TreeDescr, WidgetDescrMixin, AtomicWidgetDescr, CompWidgetDescr, \
    ContWidgetDescr


class DescrHolder(metaclass=Singleton):
    _instance = None

    def __init__(self):
        tree_descr, atomic_descr, comp_descr, cont_descr =  fileproc.Reader.read_descriptions(CONF_PATH)
        self._tree: TreeDescr = tree_descr
        self._descr_dict: Dict[WidgetDescrEnum, WidgetDescrDict] = {
            WidgetDescrEnum.ATOMIC: WidgetDescrDict(atomic_descr),
            WidgetDescrEnum.COMP: WidgetDescrDict(comp_descr),
            WidgetDescrEnum.CONT: WidgetDescrDict(cont_descr)
        }

        self._widget_names = []
        for descr_dict_ in self._descr_dict.values():
            self._widget_names.extend(descr_dict_.get_all_widget_names())

    @classmethod
    def get_instance(cls) -> "DescrHolder":
        if cls._instance is None:
            cls._instance = DescrHolder()
        return cls._instance

    @property
    def tree(self) -> TreeDescr:
        return self._tree

    @property
    def widget_names(self):
        return self._widget_names

    def get_descr_dict(self, descr_type: 'WidgetDescrEnum') -> "WidgetDescrDict":
        return self._descr_dict[descr_type]

    def get_widget_name_number(self, name: str) -> int:
        return self._widget_names.index(name)


class WidgetDescrDict(object):
    def __init__(self, descr: Iterable[WidgetDescrMixin]):
        self._d: Dict[str, WidgetDescrMixin] \
            = {d.name: d for d in descr}

    def get_descr(self, name: str) -> WidgetDescrMixin:
        return self._d[name]

    def get_all_descrs(self) -> List[WidgetDescrMixin]:
        return list(self._d.values())

    def get_all_widget_names(self) -> List[str]:
        return list(self._d.keys())


class WidgetDescrEnum(Enum):
    ATOMIC = ("atomic", AtomicWidgetDescr)
    COMP = ("comp", CompWidgetDescr)
    CONT = ("cont", ContWidgetDescr)

    def __new__(cls, descr_name, desc_type):
        obj = object.__new__(cls)
        obj._value_ = descr_name
        obj.__descr_type = desc_type
        return obj

    def get_type(self):
        return self.__descr_type