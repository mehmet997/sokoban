import collections
from node import Node


class DFS():

    def search(self, start_node:Node):
        fringe = collections.deque()
        fringe.append(start_node) # LIFO
        while fringe:
            current_node = fringe.pop() # choose the deepest node # LIFO
            if current_node.goal():
                return self.__solution(current_node)
            for child_node in current_node.expand():
                already_in_path = False
                child_node_state_as_string = ";".join([",".join(item) for item in child_node.game.matrix])
                parent = child_node.parent
                while parent:
                    parent_node_state_as_string= ";".join([",".join(item) for item in parent.game.matrix])
                    if child_node_state_as_string == parent_node_state_as_string:
                        already_in_path = True
                        break
                    parent = parent.parent
                if not already_in_path:
                    fringe.append(child_node) # LIFO
        return None  # failure if fringe is empty!

    def __solution(self, node):
        actions = []
        nodes = [node]
        curr_node=node
        while curr_node.parent:
            actions.append(curr_node.action)
            curr_node = curr_node.parent
            nodes.append(curr_node)
        return actions[::-1], nodes[::-1]






