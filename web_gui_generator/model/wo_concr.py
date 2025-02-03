from typing import Iterable, List

from web_gui_generator.model.tree import Tree, Node
from web_gui_generator.model.wo_abc import ContWOMixin, ContCompWOUnion, WOUnion, AtomicWOMixin, CompWOMixin


# container widget objects ---------------------------------------------------------------------------------------------
class ScreenWO(ContWOMixin):
    def __init__(self, id_: int, name: str, children: Iterable[WOUnion], parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent, children)


class DivWO(ContWOMixin):
    def __init__(self, id_: int, name: str, children: Iterable[WOUnion], parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent, children)


# atomic widget objects ------------------------------------------------------------------------------------------------
class ButtonWO(AtomicWOMixin):
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent)


class TextareaWO(AtomicWOMixin):
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent)


class CheckboxWO(AtomicWOMixin):
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent)


class TextWO(AtomicWOMixin):
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent)


class LabelWO(AtomicWOMixin):
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent)


class RadioWO(AtomicWOMixin):
    def __init__(self, id_: int, name: str, parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent)


# composite widget objects ---------------------------------------------------------------------------------------------
class DivItemWO(CompWOMixin):
    def __init__(self, id_: int, name: str, children: Iterable[WOUnion], parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent, children)


class RevDivItemWO(CompWOMixin):
    def __init__(self, id_: int, name: str, children: Iterable[WOUnion], parent: ContCompWOUnion = None):
        super().__init__(id_, name, parent, children)


# wo factory -----------------------------------------------------------------------------------------------------------

class WOFactory(object):
    __wo_name_mapping = {
        # cont
        "LWindow": ScreenWO,
        "Div": DivWO,
        # comp
        "DivItem": DivItemWO,
        "RevDivItem": RevDivItemWO,
        # atom
        "Label": LabelWO,
        "TextArea": TextareaWO,
        "Button": ButtonWO,
        "Text": TextWO,
        "Checkbox": CheckboxWO,
        "Radio": RadioWO
    }
    __init_wo_id = -1
    __next_wo_id = __init_wo_id

    @classmethod
    def create_wo(cls, name: str, children: List[WOUnion] = None, parent: ContCompWOUnion = None) -> WOUnion:
        if children is None:
            children = []
        id_ = cls.__get_next_id()

        wo_class = cls.__wo_name_mapping[name]
        if issubclass(wo_class, AtomicWOMixin):
            return wo_class(id_, name, parent)
        else:
            return wo_class(id_, name, children, parent)

    @classmethod
    def __get_next_id(cls) -> int:
        cls.__next_wo_id += 1
        return cls.__next_wo_id

    @classmethod
    def create_from_tree(cls, tree: Tree):
        def rec_create_child(tree_node: 'Node') -> WOUnion:
            wo_children = []
            for ch_node in tree_node.children:
                ch_wo = rec_create_child(ch_node)
                wo_children.append(ch_wo)

            wo = cls.create_wo(tree_node.name, children=wo_children)
            return wo

        root_wo = cls.create_wo(tree.root.name)
        for child_node in tree.root.children:
            child_wo = rec_create_child(child_node)
            root_wo.add_child(child_wo)
        return root_wo

    @classmethod
    def reset_ids(cls):
        cls.__next_wo_id = cls.__init_wo_id
