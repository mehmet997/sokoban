# Sokoban solver 
A Sokoban solver based on the following implementation of the Sokoban Game: 
https://github.com/morenod/sokoban

This solver uses different search algorithms to solve the Sokoban game

## Dependencies

```pip install pygame```
```pip install arrow```

## How to run
run the sokoban.py file to select a level and a search algorithm. 
Levels 1-11 can be solved by the A* search

## Search algorithms and timings 
- "X" means that it took too long, so the algorithm is not suitable for the level
- Timings are used from timing.py, measured on MacBook Pro 2021 with Apple M1 Pro chip

 | algorithm \\ level | BFS | DFS | DLS(limit=5) | IDS | UCS | A*  |
 |---|---|---|---|---|---|---|
 | 1 |	0,0003	|	0,0003	|	0,0024	|	0,0003	|	0,0003	|	0,0004 |
 | 2 |	0,0014	|	0,0008	|	0,0159	|	0,0100	|	0,0016	|	0,0025 |
 | 3 |	4,2586	|	X	|	0,1611 (cutoff)	|	X	|	5,4929	|	1,6945 |
 | 4 |	2,1534	|	X	|	0,0546 (cutoff)	|	X	|	2,5279	|	1,8801 |
 | 5 |	0,3728	|	X	|	0,0080 (cutoff)	|	X	|	0,4396	|	0,3408 |
 | 6 |	59,4061	|	X	|	0,1514 (cutoff)	|	X	|	68,3629	|	52,3653 |
 | 7 |	0,0706	|	X	|	0,0236(cutoff)	|	24,7084	|	0,0907	|	0,0435 |
 | 8 |	239,3241	|	X	|	0.0342 (cutoff)	|	X	|	273,4978	|	298,8732 |
 | 9 |	0,0031	|	55,5628	|	0,0054	|	0,0068	|	0,0064	|	0,0023 |
 | 10 |	4,2907	|	X	|	0,0228(cutoff)	|	X	|	4,8786	|	4,9565 |
 | 11 |	151,1135	|	X	|	0,1639 (cutoff)	|	X	|	262,7064	|	6,0691 |
