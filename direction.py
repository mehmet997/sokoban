class Direction():
    def __init__(self, movement):
        """Direction class,
        self.movement = tuple defining the movement e.g.
        right = (1, 0)
        left = (-1, 0)
        down = (0, 1)
        up = (0,-1)
        """
        self.movement = movement


# possible directions:
UP = Direction((0, -1))
RIGHT = Direction((1, 0))
DOWN = Direction((0, 1))
LEFT = Direction((-1, 0))

