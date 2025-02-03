from abc import ABC, abstractmethod
from typing import List


class TreeDescr(object):
    def __init__(self, root: str, min_nwidgets: int, max_nwidgets: int):
        self._root = root
        self._min_nwidgets = min_nwidgets
        self._max_nwidgets = max_nwidgets

    @property
    def root(self) -> str:
        return self._root

    @property
    def min_nwidgets(self) -> int:
        return self._min_nwidgets

    @property
    def max_nwidgets(self) -> int:
        return self._max_nwidgets

    def __repr__(self):
        return f"<TreeDescr -- root: {self._root}, min_nwidgets: {self._min_nwidgets}, " \
               f"max_nwidgets: {self._max_nwidgets}>"


class WidgetDescrMixin(ABC):
    @abstractmethod
    def __init__(self, name: str, solo: bool, prob: float):
        self._name = name
        self._solo = solo
        self._prob = prob

    @property
    def name(self):
        return self._name

    @property
    def solo(self) -> bool:
        return self._solo

    @property
    def prob(self) -> float:
        return self._prob

    def _props_repr(self) -> str:
        return f"name: {self._name}, solo: {self._solo}, prob: {self._prob}"

    def __repr__(self):
        return f"<WidgetDescrMixin -- {self._props_repr()}>"


class AtomicWidgetDescr(WidgetDescrMixin):
    def __init__(self, name: str, solo: bool, prob: float):
        super().__init__(name, solo, prob)

    def __repr__(self):
        return f"<AtomicWidgetDescr -- {self._props_repr()}>"


class CompWidgetDescr(AtomicWidgetDescr):
    def __init__(self, name: str, solo: bool, prob: float, content: List['CompWidgetContentDescr']):
        super().__init__(name, solo, prob)
        if content is None:
            content = []

        self._content = content

    @property
    def content(self) -> List['CompWidgetContentDescr']:
        return self._content

    def _props_repr(self) -> str:
        return f"{super()._props_repr()}, content: {self._content}"

    def __repr__(self):
        return f"<CompWidgetDescr -- {self._props_repr()}"


class CompWidgetContentDescr(WidgetDescrMixin):
    def __init__(self, name: str, prob: float, group: int):
        super(CompWidgetContentDescr, self).__init__(name, False, prob)
        self._group = group

    @property
    def group(self) -> int:
        return self._group

    def _props_repr(self) -> str:
        return f"name: {self._name}, group: {self._group}, prob: {self._prob}"

    def __repr__(self):
        return f"<CompWidgetContent -- {self._props_repr()}>"


class ContWidgetDescr(AtomicWidgetDescr):
    def __init__(self, name: str, children: List[str], solo: bool, prob: float, max_nwidget: int):
        super().__init__(name, solo, prob)
        self._children = children
        self._max_nwidgets = max_nwidget if max_nwidget > 0 else 1_000_000_000

    @property
    def children(self):
        return self._children

    @property
    def max_nwidget(self):
        return self._max_nwidgets

    def _props_repr(self) -> str:
        return f"{super()._props_repr()}, children: {self._children}"

    def __repr__(self):
        return f"<ContWidget -- {self._props_repr()}"
