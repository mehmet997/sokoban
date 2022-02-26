import collections

from dls import DLS
from node import Node

class IDS(DLS):
    def __init__(self, start_limit):
        super().__init__(start_limit)

    def search(self, start_node: Node):
        while 1:
            result = super(IDS, self).search(start_node)
            if result[0] != "cutoff": return result[0],result[1], self.limit
            self.limit = self.limit+1

