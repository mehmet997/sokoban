from sokoban import game
from HeuristicFunctionModeEnum import HeuristicFunctionMode
from a_star import A_star
from bfs import BFS
from dfs import DFS
from dls import DLS
from ids import IDS
from node import Node
from sokoban import Mode
from ucs import UCS
import arrow


""" single level single algorithm time analysis """


level = 5
algorithm = 2
print(" level:", level, " algorithm:",algorithm)
game_obj = game('levels', level)
n = Node(None, None, 0, game_obj)
mode = Mode(algorithm)
time1 = arrow.utcnow()
if mode == Mode.BFS:
    bfs = BFS()
    actions, nodes = bfs.search(n)
    #print([action.movement for action in actions])
elif mode == Mode.DFS:
    dfs = DFS()
    actions, nodes = dfs.search(n)
    #print([action.movement for action in actions])
elif mode == Mode.UCS:
    ucs = UCS()
    actions, nodes = ucs.search(n)
    #print([action.movement for action in actions])

elif mode == Mode.A_STAR:
    a_star = A_star()
    actions, nodes = a_star.search(n, heuristic_function=HeuristicFunctionMode.MANHATTAN)

elif mode == Mode.DLS:
    dls = DLS(limit=5)
    actions, nodes = dls.search(n)
elif mode == Mode.IDS:
    ids = IDS(3)
    actions, nodes, depth = ids.search(n)

time2 = arrow.utcnow()
elapsed_time = (time2 - time1).total_seconds()
print(elapsed_time)