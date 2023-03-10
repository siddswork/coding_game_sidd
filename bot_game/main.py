# This is a sample Python script.
import string
from typing import List

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import random
from dataclasses import dataclass

from player_boss import get_boss_moves
from player_one import get_p1_moves


# 2.1 - Define datastructures
@dataclass
class Tile:
    x: int
    y: int
    scrap_amount: int
    owner: int
    units: int
    recycler: bool
    can_build: bool
    can_spawn: bool
    in_range_of_recycler: bool


# 2.2 - Define constants
TEAL = (0, 128, 128)
BOARD_SIZE = (14, 7)  # board_size = (width, height)
TILE_SIZE = 82
BOARD_X_MAX, BOARD_Y_MAX = BOARD_SIZE
WINDOW_WIDTH = BOARD_X_MAX * TILE_SIZE
WINDOW_HEIGHT = BOARD_Y_MAX * TILE_SIZE
FRAMES_PER_SECOND = 20
NEUTRAL = -1
PLAYER1 = 0
PLAYER2 = 1

# 2.3 - Load assets: image(s), sound(s), etc.
TILE_P1_IMG = pygame.image.load('images/player1_tile_s.png')
TILE_P2_IMG = pygame.image.load('images/player2_tile_s.png')
TILE_N_IMG = pygame.image.load('images/neutral_tile_s.png')
TILE_G_IMG = pygame.image.load('images/grass_s.png')
P1_IMG = pygame.image.load('images/player1_s.png')
P2_IMG = pygame.image.load('images/player2_s.png')


def coordinate(x: int, y: int):
    return f'{x},{y}'


def empty_board():
    # board_list: list[Tile] = []
    board_dict: dict[string, Tile] = {}
    for x in range(BOARD_X_MAX):
        for y in range(BOARD_Y_MAX):
            scrap_amount = random.randint(1, 4)
            owner = -1
            units = 0
            recycler = False
            can_build = False
            can_spawn = False
            in_range_of_recycler = False
            tile = Tile(x, y, scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler)
            # board_list.append(tile)
            board_dict[coordinate(x, y)] = tile
    # return board_list, board_dict
    return board_dict


def update_start_positions(board_dict, player, pos_x, pos_y):
    # Middle
    board_dict[coordinate(pos_x, pos_y)].owner = player
    # up
    board_dict[coordinate(pos_x, pos_y - 1)].owner = player
    board_dict[coordinate(pos_x, pos_y - 1)].units = 1
    # down
    board_dict[coordinate(pos_x, pos_y + 1)].owner = player
    board_dict[coordinate(pos_x, pos_y + 1)].units = 1
    # left
    board_dict[coordinate(pos_x - 1, pos_y)].owner = player
    board_dict[coordinate(pos_x - 1, pos_y)].units = 1
    # right
    board_dict[coordinate(pos_x + 1, pos_y)].owner = player
    board_dict[coordinate(pos_x + 1, pos_y)].units = 1

    return board_dict


def initialize_board():
    board_dict = empty_board()
    # Code to initialize board with bots
    p2_x: int
    p2_y: int
    possible_start = [(1, 1), (12, 1), (12, 5), (1, 5)]

    p1_x, p1_y = possible_start[random.randint(0, 3)]
    if p1_x < 2:
        next_possible_start = [(12, 1), (12, 5)]
        p2_x, p2_y = next_possible_start[random.randint(0, 1)]
    else:
        next_possible_start = [(1, 1), (1, 5)]
        p2_x, p2_y = next_possible_start[random.randint(0, 1)]

    # print(f'P1 start: {p1_x}, {p1_y}')
    # print(f'P1 start: {p2_x}, {p2_y}')

    board_dict = update_start_positions(board_dict, PLAYER1, p1_x, p1_y)
    board_dict = update_start_positions(board_dict, PLAYER2, p2_x, p2_y)

    return board_dict


def draw_board(window, board_dict: dict[string, Tile]):
    window.fill(TEAL)
    for key in board_dict:
        tile = board_dict[key]
        if tile.scrap_amount == 0:
            window.blit(TILE_G_IMG, (tile.x * TILE_SIZE, tile.y * TILE_SIZE))
        elif tile.owner == NEUTRAL:
            window.blit(TILE_N_IMG, (tile.x * TILE_SIZE, tile.y * TILE_SIZE))
        elif tile.owner == PLAYER1:
            window.blit(TILE_P1_IMG, (tile.x * TILE_SIZE, tile.y * TILE_SIZE))
            if tile.units > 0:
                window.blit(P1_IMG, (tile.x * TILE_SIZE + 4, tile.y * TILE_SIZE + 3))
        elif tile.owner == PLAYER2:
            window.blit(TILE_P2_IMG, (tile.x * TILE_SIZE, tile.y * TILE_SIZE))
            if tile.units > 0:
                window.blit(P2_IMG, (tile.x * TILE_SIZE + 4, tile.y * TILE_SIZE + 3))
    # Update the window
    pygame.display.update()


def board_for_player(board_dict: dict[string, Tile]):
    const_board = []
    for key in board_dict:
        tile = board_dict[key]
        const_board.append((tile.x, tile.y, tile.scrap_amount, tile.owner, tile.units, tile.recycler, tile.can_build,
                            tile.can_spawn, tile.in_range_of_recycler))
    return const_board


def filter_out_of_board(pos):
    x, y = pos
    if x >= 0 and x < BOARD_X_MAX and y >= 0 and y < BOARD_Y_MAX:
        return pos


def filter_grass_and_recyclers(pos, board_dict: dict[string, Tile]):
    x, y = pos
    key = coordinate(x, y)
    if not board_dict[key].recycler and board_dict[key].scrap_amount != 0:
        return pos


def find_valid_next_steps(board_dict, bot_x, bot_y) -> [(int, int)]:
    # possible_next = [up, down, left, right]
    possible_next = [(bot_x, bot_y - 1), (bot_x, bot_y + 1), (bot_x - 1, bot_y), (bot_x + 1, bot_y)]
    valid_next = list(filter(filter_out_of_board, possible_next))
    valid_next = list(filter(lambda pos: filter_grass_and_recyclers(pos, board_dict), valid_next))

    return valid_next


def find_path(board_dict, start_x, start_y, target_x, target_y):
    def find_path_ending_with_nade(node, path):
        if type(path) is tuple:
            if path[-1] == node:
                return path
        else:
            if path == node:
                return path

    visited = []  # List for visited nodes.
    queue = []  # Initialize a queue
    start = coordinate(start_x, start_y)
    target = coordinate(target_x, target_y)
    if start == target:
        new_path = (start, target)
        return True, new_path
    paths = [(start)]

    visited.append(start)
    queue.append(start)

    while queue:  # Creating loop to visit each node
        checking_pos = queue.pop(0)
        x, y = map(int, checking_pos.split(','))
        valid_next = find_valid_next_steps(board_dict, x, y)

        for neighbour in valid_next:
            neighbour_as_string = coordinate(neighbour[0], neighbour[1])
            if neighbour_as_string not in visited:
                path = list(filter(lambda path: find_path_ending_with_nade(checking_pos, path), paths))

                new_path = ()
                if type(path[0]) is tuple:
                    new_path = path[0] + (neighbour_as_string,)
                else:
                    new_path = (path[0], neighbour_as_string)
                if neighbour_as_string == target:
                    return True, new_path
                    queue = []
                    break
                paths.append(new_path)
                visited.append(neighbour_as_string)
                queue.append(neighbour_as_string)
    return False, ()


def find_next_step(board_dict, bot_x, bot_y, target_x, target_y):
    next_x = -1
    next_y = -1
    has_path, valid_path = find_path(board_dict, bot_x, bot_y, target_x, target_y)
    if has_path:
        next_x, next_y = map(int, valid_path[1].split(","))
    else:
        valid_next: [(int, int)] = find_valid_next_steps(board_dict, bot_x, bot_y)
        if len(valid_next) > 0:
            next_x, next_y = valid_next[random.randint(0, len(valid_next) - 1)]
        else:
            next_x, next_y = bot_x, bot_y

    return next_x, next_y


def play_moves(player: int, moves: string, board_dict: dict[string, Tile]):
    for action in moves.split(";"):
        command = action.split(" ")[0]
        print(f'  COM: {command}')
        if command == "MOVE":
            if len(action.split(" ")) == 6:
                # get parameters
                try:
                    bot_count, bot_x, bot_y, target_x, target_y = map(int, action.split(" ")[1:])
                    source = coordinate(bot_x, bot_y)

                    # Move only when bots to move is greater than 0
                    if bot_count > 0:
                        # Move only when source loc is player's and has units
                        if board_dict[source].owner == player and board_dict[source].units > 0:
                            next_x, next_y = find_next_step(board_dict, bot_x, bot_y, target_x, target_y)
                            next = coordinate(next_x, next_y)
                            amount = bot_count if bot_count <= board_dict[source].units else board_dict[source].units
                            print(f'    Moving {amount} bot(s) from {bot_x}, {bot_y} to {next_x}, {next_y}')
                            #TODO: Code the movement by changing board values
                        else:
                            print(f'    Invalid command: {action}')
                except ValueError:
                    print(f'    Incorrect parameter type: {action}')
            else:
                print(f'    Incorrect parameter count: {action}')
                continue
        else:
            print(f'    Command not supported: {action}')
    return board_dict


def game():
    # 3 - Initialize the world
    board_dict = initialize_board()
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    # Clear the window & draw board
    window.fill(TEAL)
    draw_board(window, board_dict)

    temp1 = True
    temp2 = True

    while True:
        # 7 - Check for and handle events
        for event in pygame.event.get():
            # Clicked the close button? Quit pygame and end the program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # P1 move
        moves: string
        players_board_view = board_for_player(board_dict)
        if temp1:
            moves = get_p1_moves(players_board_view, BOARD_SIZE)
            print(f'P1: {moves}')
            temp1 = False
        # board = play_moves(PLAYER1, p1_moves, board_dict)
        draw_board(window, board_dict)

        # BOSS move (P2)
        players_board_view = board_for_player(board_dict)
        if temp2:
            moves = get_boss_moves(players_board_view, BOARD_SIZE)
            print(f'BOSS: {moves}')
            board_dict = play_moves(PLAYER2, moves, board_dict)
            temp2 = False
        draw_board(window, board_dict)

        # Slow things down a bit
        clock.tick(FRAMES_PER_SECOND)

    # Press the green button in the gutter to run the script.


if __name__ == '__main__':
    game()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
