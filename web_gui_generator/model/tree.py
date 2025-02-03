from typing import List


class Tree(object):
    def __init__(self, root: 'Node'):
        self._root = root

    @property
    def root(self) -> 'Node':
        return self._root

    def __repr__(self):
        def dfs(node: Node, level: int) -> None:
            result_string_list.append(("    " * level)
                                      + f"<level {level}>::{node.__str__()}"
                                      + f"::<amount of children {len(node.children)}>")
            for child_node in node.children:
                dfs(child_node, level + 1)

        obj_marker = f"\n<------ Tree ------>"
        result_string_list = [obj_marker]
        dfs(self.root, 0)
        result_string_list.append(obj_marker + f" nwidget: {len(result_string_list) - 1}")
        return '\n'.join(result_string_list)


class Node(object):
    def __init__(self, name: str, parent: 'Node' = None, children: List['Node'] = None):
        if children is None:
            children = []

        self._name = name
        self._children = children
        self._parent = parent

    @property
    def name(self) -> str:
        return self._name

    @property
    def children(self) -> List['Node']:
        return self._children

    @property
    def parent(self) -> 'Node':
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def add_children(self, children: List['Node']):
        self._children.extend(children)

    def add_child(self, child: 'Node'):
        self._children.append(child)

    # def can_have_as_child(self, potential_child: 'Node', containers: Dict[str, ContWidgetDescr]) -> bool:
    #     return (self._name in containers.keys()) and (potential_child.name in containers[self._name].children)

    def get_node_and_descendants(self) -> List['Node']:
        def dfs(ls: List['Node'], node: 'Node'):
            ls.append(node)
            for child in node.children:
                dfs(ls, child)

        result = []
        dfs(result, self)
        return result

    def __repr__(self):
        return f'<Node -- name: {self._name} children: {self._children}>'

    def __str__(self):
        return f'<Node -- name: {self._name}>'
