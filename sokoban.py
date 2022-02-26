#!../bin/python
import collections
import itertools
import sys
import time
from enum import Enum

import pygame

from HeuristicFunctionModeEnum import HeuristicFunctionMode
from a_star import A_star
from bfs import BFS
from dfs import DFS
from dls import DLS
from ids import IDS
from node import Node
from ucs import UCS


class game:

    def is_valid_value(self, char):
        if (char == ' ' or  # floor
                char == '#' or  # wall
                char == '@' or  # worker on floor
                char == '.' or  # dock
                char == '*' or  # box on dock
                char == '$' or  # box
                char == '+'):  # worker on dock
            return True
        else:
            return False

    def __init__(self, filename, level):
        self.queue = collections.deque()
        self.matrix = []
        #        if level < 1 or level > 50:
        if level < 1:
            print("ERROR: Level " + str(level) + " is out of range")
            sys.exit(1)
        else:
            file = open(filename, 'r')
            level_found = False
            for line in file:
                row = []
                if not level_found:
                    if "Level " + str(level) == line.strip():
                        level_found = True
                else:
                    if line.strip() != "":
                        row = []
                        for c in line:
                            if c != '\n' and self.is_valid_value(c):
                                row.append(c)
                            elif c == '\n':  # jump to next row when newline
                                continue
                            else:
                                print("ERROR: Level " + str(level) + " has invalid value " + c)
                                sys.exit(1)
                        self.matrix.append(row)
                    else:
                        break

    def load_size(self):
        x = 0
        y = len(self.matrix)
        for row in self.matrix:
            if len(row) > x:
                x = len(row)
        return (x * 32, y * 32)

    def get_matrix(self):
        return self.matrix

    def print_matrix(self):
        for row in self.matrix:
            for char in row:
                sys.stdout.write(char)
                sys.stdout.flush()
            sys.stdout.write('\n')

    def get_content(self, x, y):
        return self.matrix[y][x]

    def set_content(self, x, y, content):
        if self.is_valid_value(content):
            self.matrix[y][x] = content
        else:
            print("ERROR: Value '" + content + "' to be added is not valid")

    def worker(self):
        x = 0
        y = 0
        for row in self.matrix:
            for pos in row:
                if pos == '@' or pos == '+':
                    return (x, y, pos)
                else:
                    x = x + 1
            y = y + 1
            x = 0

    def can_move(self, x, y):
        return self.get_content(self.worker()[0] + x, self.worker()[1] + y) not in ['#', '*', '$']

    def next(self, x, y):
        return self.get_content(self.worker()[0] + x, self.worker()[1] + y)

    def can_push(self, x, y):
        return (self.next(x, y) in ['*', '$'] and self.next(x + x, y + y) in [' ', '.'])

    def is_completed(self):
        for row in self.matrix:
            for cell in row:
                if cell == '$':
                    return False
        return True

    def move_box(self, x, y, a, b):
        #        (x,y) -> move to do
        #        (a,b) -> box to move
        current_box = self.get_content(x, y)
        future_box = self.get_content(x + a, y + b)
        if current_box == '$' and future_box == ' ':
            self.set_content(x + a, y + b, '$')
            self.set_content(x, y, ' ')
        elif current_box == '$' and future_box == '.':
            self.set_content(x + a, y + b, '*')
            self.set_content(x, y, ' ')
        elif current_box == '*' and future_box == ' ':
            self.set_content(x + a, y + b, '$')
            self.set_content(x, y, '.')
        elif current_box == '*' and future_box == '.':
            self.set_content(x + a, y + b, '*')
            self.set_content(x, y, '.')

    def unmove(self):
        if self.queue:
            movement = self.queue.pop()
            if movement[2]:
                current = self.worker()
                self.move(movement[0] * -1, movement[1] * -1, False)
                self.move_box(current[0] + movement[0], current[1] + movement[1], movement[0] * -1, movement[1] * -1)
            else:
                self.move(movement[0] * -1, movement[1] * -1, False)

    def move(self, x, y, save):
        if self.can_move(x, y):
            current = self.worker()
            future = self.next(x, y)
            if current[2] == '@' and future == ' ':
                self.set_content(current[0] + x, current[1] + y, '@')
                self.set_content(current[0], current[1], ' ')
                if save: self.queue.appendleft((x, y, False))
            elif current[2] == '@' and future == '.':
                self.set_content(current[0] + x, current[1] + y, '+')
                self.set_content(current[0], current[1], ' ')
                if save: self.queue.appendleft((x, y, False))
            elif current[2] == '+' and future == ' ':
                self.set_content(current[0] + x, current[1] + y, '@')
                self.set_content(current[0], current[1], '.')
                if save: self.queue.appendleft((x, y, False))
            elif current[2] == '+' and future == '.':
                self.set_content(current[0] + x, current[1] + y, '+')
                self.set_content(current[0], current[1], '.')
                if save: self.queue.appendleft((x, y, False))
        elif self.can_push(x, y):
            current = self.worker()
            future = self.next(x, y)
            future_box = self.next(x + x, y + y)
            if current[2] == '@' and future == '$' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save: self.queue.appendleft((x, y, True))
            elif current[2] == '@' and future == '$' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save: self.queue.appendleft((x, y, True))
            elif current[2] == '@' and future == '*' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.appendleft((x, y, True))
            elif current[2] == '@' and future == '*' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], ' ')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.appendleft((x, y, True))
            if current[2] == '+' and future == '$' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '@')
                if save: self.queue.appendleft((x, y, True))
            elif current[2] == '+' and future == '$' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.appendleft((x, y, True))
            elif current[2] == '+' and future == '*' and future_box == ' ':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.appendleft((x, y, True))
            elif current[2] == '+' and future == '*' and future_box == '.':
                self.move_box(current[0] + x, current[1] + y, x, y)
                self.set_content(current[0], current[1], '.')
                self.set_content(current[0] + x, current[1] + y, '+')
                if save: self.queue.appendleft((x, y, True))


def print_game(matrix, screen):
    screen.fill(background)
    x = 0
    y = 0
    for row in matrix:
        for char in row:
            if char == ' ':  # floor
                screen.blit(floor, (x, y))
            elif char == '#':  # wall
                screen.blit(wall, (x, y))
            elif char == '@':  # worker on floor
                screen.blit(worker, (x, y))
            elif char == '.':  # dock
                screen.blit(docker, (x, y))
            elif char == '*':  # box on dock
                screen.blit(box_docked, (x, y))
            elif char == '$':  # box
                screen.blit(box, (x, y))
            elif char == '+':  # worker on dock
                screen.blit(worker_docked, (x, y))
            x = x + 32
        x = 0
        y = y + 32


def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass


def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None, 18)
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 100,
                      (screen.get_height() / 2) - 10,
                      200, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255),
                     ((screen.get_width() / 2) - 300,
                      (screen.get_height() / 2) - 12,
                      500, 24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    ((screen.get_width() / 2) - 300, (screen.get_height() / 2) - 10))
    pygame.display.flip()


def display_end(screen):
    message = "Level Completed"
    fontobject = pygame.font.Font(None, 18)
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 100,
                      (screen.get_height() / 2) - 10,
                      200, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255),
                     ((screen.get_width() / 2) - 102,
                      (screen.get_height() / 2) - 12,
                      204, 24), 1)
    screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()


def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + "".join(current_string))
    while 1:
        inkey = get_key()
        if inkey == pygame.K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == pygame.K_RETURN:
            break
        elif inkey == pygame.K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + "".join(current_string))
    return int("".join(current_string))


def start_game():
    start = pygame.display.set_mode((700, 240))
    level = ask(start, "Select Level")
    start = pygame.display.set_mode((700, 240))
    mode = ask(start, "select search algorithm: BFS = 1, DFS = 2, DLS = 3, IDS = 4, UCS = 5, A_STAR = 6")

    if level > 0:
        return level, mode
    else:
        print("ERROR: Invalid Level: " + str(level))
        sys.exit(2)

def main():
    print("python main function")



class Mode(Enum):
    BFS = 1
    DFS = 2
    DLS = 3
    IDS = 4
    UCS = 5
    A_STAR = 6
if __name__ == '__main__':
    wall = pygame.image.load('images/wall.png')
    floor = pygame.image.load('images/floor.png')
    box = pygame.image.load('images/box.png')
    box_docked = pygame.image.load('images/box_docked.png')
    worker = pygame.image.load('images/worker.png')
    worker_docked = pygame.image.load('images/worker_dock.png')
    docker = pygame.image.load('images/dock.png')
    background = 255, 226, 191
    pygame.init()

    level, mode_selector = start_game()
    game = game('levels', level)
    n = Node(None, None, 0, game)





    actions = None

    mode = Mode(mode_selector)
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
        dls = DLS(limit=17)
        actions, nodes = dls.search(n)
    elif mode == Mode.IDS:
        ids = IDS(3)
        actions, nodes, depth = ids.search(n)
        #print("IDS found solution at depth: ", depth)


    size = game.load_size()
    screen = pygame.display.set_mode(size)

    for i in itertools.count(start=0):
        if game.is_completed(): display_end(screen)
        print_game(game.get_matrix(), screen)
        if i < len(actions):
            game.move(actions[i].movement[0], actions[i].movement[1], True)
            pygame.display.update()

        if i > len(actions) + 10:
            break
        time.sleep(0.5)

