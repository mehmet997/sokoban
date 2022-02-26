import collections

from node import Node

class UCS():
    """Falls back to BFS if all costs are same! """
    def search(self, start_node: Node):
        fringe = collections.deque()
        fringe.append(start_node)
        explored = None
        while 1:
            if not fringe:
                return None  # failure if fringe is empty!

            current_node = fringe.popleft()  # choose the lowest-cost node in fringe
            if current_node.goal():
                return self.__solution(current_node)

            current_node_state_as_string = "X".join(["Y".join(item) for item in current_node.game.matrix])

            if not explored:
                explored = {current_node_state_as_string}
            else:
                explored.add(current_node_state_as_string)  # add node.State to explored
            for child in current_node.expand():
                child_node_state_as_string = "X".join(["Y".join(item) for item in child.game.matrix])
                child_in_fringe = False
                child_in_fringe_index = None
                for index, fringe_item in enumerate(fringe):
                    fringe_item_as_string = "X".join(["Y".join(item) for item in fringe_item.game.matrix])
                    if fringe_item_as_string == child_node_state_as_string:
                        child_in_fringe = True
                        child_in_fringe_index = index

                if not (child_in_fringe or (child_node_state_as_string in explored)):
                    fringe.appendleft(child)
                    fringelist = sorted(fringe)
                    fringe = collections.deque(fringelist)

                elif child_in_fringe and child.eval() < fringe[child_in_fringe_index].eval():
                    fringe[child_in_fringe_index] = child
                    #fringe.appendleft(child)
                    fringelist = sorted(fringe)
                    fringe = collections.deque(fringelist)





    def __solution(self, node):
        actions = []
        nodes = [node]
        curr_node = node
        while curr_node.parent:
            actions.append(curr_node.action)
            curr_node = curr_node.parent
            nodes.append(curr_node)
        return actions[::-1], nodes[::-1]