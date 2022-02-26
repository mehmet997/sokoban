import collections
from node import Node


class BFS():

    def search(self, start_node:Node):
        if start_node.goal():
            return self.__solution(start_node)
        fringe = collections.deque()
        fringe.appendleft(start_node) # FIFO
        explored = None
        while 1:
            if not fringe:
                return None # failure if fringe is empty!
            current_node = fringe.pop() # choose the shallowest node FIFO
            current_node_state_as_string = "X".join([ "Y".join(item) for item in current_node.game.matrix])
            #print(current_node.game.matrix)
            if not explored:
                explored = {current_node_state_as_string}
            else:
                explored.add(current_node_state_as_string) # add node.State to explored
            for child in current_node.expand():

                child_node_state_as_string = "X".join(["Y".join(item) for item in child.game.matrix])
                child_in_fringe = False
                for fringe_item in fringe:
                    fringe_item_as_string = "X".join(["Y".join(item) for item in fringe_item.game.matrix])
                    if fringe_item_as_string == child_node_state_as_string: child_in_fringe = True
                if not (child_in_fringe or (child_node_state_as_string in explored)):
                    if child.goal():
                        return self.__solution(child)
                    else:
                        fringe.appendleft(child) # FIFO

    def __solution(self, node):
        actions = []
        nodes = [node]
        curr_node=node
        while curr_node.parent:
            actions.append(curr_node.action)
            curr_node = curr_node.parent
            nodes.append(curr_node)
        return actions[::-1], nodes[::-1]






