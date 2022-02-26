import collections
from node import Node


class DLS():
    def __init__(self, limit):
        self.limit = limit

    def search(self, start_node: Node):
        node = self.__depth_limited_search(start_node, self.limit)
        return self.__solution(node)

    def __depth_limited_search(self, node, limit):
        cutoff_occured = False
        if node.goal():
            return node
        elif self.__depth(node) == limit: return "cutoff"
        else:
            for successor in node.expand():
                result = self.__depth_limited_search(successor, limit)
                if result == "cutoff": cutoff_occured = True
                elif result: return result
            if cutoff_occured: return "cutoff"
            else: return "failure"

    def __depth(self, node):
        depth = 0
        parent = node.parent
        while parent:
            parent = parent.parent
            depth = depth +1
        return depth

    def __solution(self, node):
        if node == "cutoff":
            return "cutoff", None
        if node == "failure":
            return "failure", None
        actions = []
        nodes = [node]
        curr_node=node
        while curr_node.parent:
            actions.append(curr_node.action)
            curr_node = curr_node.parent
            nodes.append(curr_node)
        return actions[::-1], nodes[::-1]

