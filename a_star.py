import collections

from HeuristicFunctionModeEnum import HeuristicFunctionMode
from node import Node
from ucs import UCS


class A_star(UCS):
    def search(self, start_node: Node, heuristic_function = HeuristicFunctionMode.MANHATTAN):
        start_node = Node(start_node.action, start_node.parent, start_node.g, start_node.game, heuristic_function)
        result = super(A_star, self).search(start_node)
        return result
