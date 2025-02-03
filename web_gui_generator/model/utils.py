from typing import Union

from web_gui_generator.model.tree import Node
from web_gui_generator.model.wo_abc import AtomicWOMixin, ContWOMixin, CompWOMixin

HasChildrenNode = Union[Node, ContWOMixin, CompWOMixin]
GeneralNode = Union[Node, ContWOMixin, CompWOMixin, AtomicWOMixin]


class Utils(object):
    @classmethod
    def dfs(cls, start_node: HasChildrenNode, node_handler=None):
        """
        :param start_node: node to start traversal. Must have children property
        :param node_handler: function that takes 1 arg: GeneralNode as a value.
            Invoke for each node in traversal. May return an
        object

        :return a list of its return value for each node
        """

        res_list = []

        def dfs_(node: GeneralNode):
            res_list.append(node_handler(node))

            if not isinstance(node, AtomicWOMixin):
                for child_node in node.children:
                    dfs_(child_node)

        dfs_(start_node)
        return res_list
