__all__ = ["FileProc", "Reader"]

from json import dumps, load
from pathlib import Path
from typing import Dict, Callable, Any, List, Tuple

from web_gui_generator.dto import AtomicWidgetDTO, CompWidgetContentDTO, ContWidgetDTO, TreeDescrDTO, TreeDTO, \
    NodeDTO, CompWidgetDTO
from web_gui_generator.model.tree import Tree, Node
from web_gui_generator.model.w_descr import TreeDescr, AtomicWidgetDescr, CompWidgetDescr, CompWidgetContentDescr, \
    ContWidgetDescr



class FileProc(object):
    @classmethod
    def write_json(cls, obj, p: Path, mode: str = 'w', mk_parents: bool = True, exist_ok: bool = True,
                   obj_hook: Callable[[Any], Dict] = None):
        if obj_hook is None:
            obj_hook = lambda d: d.__dict__

        filepath = p.parent
        if filepath:
            filepath.mkdir(parents=mk_parents, exist_ok=exist_ok)
        with open(p, mode) as out:
            json_str = dumps(obj, default=obj_hook)
            out.write(json_str)

    @classmethod
    def read_json(cls, p: Path, obj_hook: Callable[[Dict], Any] = None, mode: str = 'r') -> Any:
        with open(p, mode) as fin:
            data = load(fin, object_hook=obj_hook)
        return data

    @classmethod
    def write_file(cls, p: Path, text: str, mode: str = 'w', mk_parents: bool = True, exist_ok: bool = True):
        dir_path = p.parent
        dir_path.mkdir(parents=mk_parents, exist_ok=exist_ok)
        with open(p, mode) as out:
            out.write(text)


class DTOMapper(object):
    @classmethod
    def map_atomic_widget_dto(cls, dto: AtomicWidgetDTO) -> AtomicWidgetDescr:
        return AtomicWidgetDescr(dto.name, dto.solo, dto.prob)

    @classmethod
    def map_comp_widget_dto(cls, dto: CompWidgetDTO) -> CompWidgetDescr:
        content = []
        for cont_item_dto in dto.content:
            content.append(cls.map_comp_widget_content_dto(cont_item_dto))

        return CompWidgetDescr(dto.name, dto.solo, dto.prob, content)

    @classmethod
    def map_comp_widget_content_dto(cls, dto: CompWidgetContentDTO) -> CompWidgetContentDescr:
        return CompWidgetContentDescr(dto.name, dto.prob, dto.group)

    @classmethod
    def map_cont_widget_dto(cls, dto: ContWidgetDTO) -> ContWidgetDescr:
        max_nwidgets = dto.ncols * dto.nrows
        return ContWidgetDescr(dto.name, dto.children, dto.solo, dto.prob, max_nwidgets)

    @classmethod
    def map_tree_descr_dto(cls, dto: TreeDescrDTO) -> TreeDescr:
        return TreeDescr(dto.root, dto.min_nwidgets, dto.max_nwidgets)

    @classmethod
    def map_tree(cls, tree: Tree) -> TreeDTO:
        def dfs(node: 'Node') -> 'NodeDTO':
            node_dto = NodeDTO(node.name)
            for child in node.children:
                child_dto = dfs(child)
                node_dto.children.append(child_dto)
            return node_dto

        root_dto = dfs(tree.root)
        return TreeDTO(root_dto)

    @classmethod
    def map_tree_dto(cls, tree_dto: TreeDTO) -> Tree:
        def dfs(node_dto: 'NodeDTO') -> 'Node':
            node = Node(node_dto.name)
            for child_dto in node_dto.children:
                child = dfs(child_dto)
                node.children.append(child)
            return node

        root = dfs(tree_dto.root)
        return Tree(root)


class Reader(object):
    _ATOMIC = Path("atomic_widget_descr.json")
    _COMPOSITE = Path("comp_widget_descr.json")
    _CONTAINER = Path("cont_widget_descr.json")
    _TREE_DESCR = Path("tree_descr.json")

    @classmethod
    def __comp_list_json_reader_hook(cls, d: Dict):
        try:
            return CompWidgetDTO(**d)
        except:
            return CompWidgetContentDTO(**d)

    @classmethod
    def read_descriptions(cls, dir_path: Path) \
            -> Tuple[TreeDescr, List[AtomicWidgetDescr], List[CompWidgetDescr], List[ContWidgetDescr]]:
        atomic_list_dto: List[AtomicWidgetDTO] = FileProc.read_json(dir_path / cls._ATOMIC,
                                                                    obj_hook=lambda d: AtomicWidgetDTO(**d))
        comp_list_dto: List[CompWidgetDTO] = FileProc.read_json(dir_path / cls._COMPOSITE,
                                                                obj_hook=lambda d: cls.__comp_list_json_reader_hook(d))
        cont_list_dto: List[ContWidgetDTO] = FileProc.read_json(dir_path / cls._CONTAINER,
                                                                obj_hook=lambda d: ContWidgetDTO(**d))
        tree_descr_dto: TreeDescrDTO = FileProc.read_json(dir_path / cls._TREE_DESCR,
                                                          obj_hook=lambda d: TreeDescrDTO(**d))

        atomic_list = [DTOMapper.map_atomic_widget_dto(item) for item in atomic_list_dto]
        comp_list = [DTOMapper.map_comp_widget_dto(item) for item in comp_list_dto]
        cont_list = [DTOMapper.map_cont_widget_dto(item) for item in cont_list_dto]
        tree_descr = DTOMapper.map_tree_descr_dto(tree_descr_dto)
        return tree_descr, atomic_list, comp_list, cont_list

    @classmethod
    def __tree_json_reader_hook(cls, d: Dict):
        try:
            return TreeDTO(**d)
        except:
            return NodeDTO(**d)

    @classmethod
    def read_trees(cls, dir_path: Path, ntrees: int, start: int = 0) -> List[Tree]:
        trees_dto: List[TreeDTO] = []
        for i in range(start, start + ntrees):
            trees_dto.append(FileProc.read_json(dir_path / f"tree{i}.json",
                                                obj_hook=lambda d: cls.__tree_json_reader_hook(d)))
        return [DTOMapper.map_tree_dto(tree_dto) for tree_dto in trees_dto]


class Writer(object):
    @classmethod
    def write_names(cls, file_path: Path, names):
        output = "\n".join(names)
        FileProc.write_file(file_path, output)

    @classmethod
    def write_geom(cls, file_path: Path, geom: str):
        FileProc.write_file(file_path, geom + "\n", mode="a")
