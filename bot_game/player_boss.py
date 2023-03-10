# 1 - Import packages
import random
from dataclasses import dataclass


# Define datastructures
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


@dataclass
class Target:
    x: int
    y: int


# Define constants
ME = 1
OPP = 0
NONE = -1

# Define global
width: int
height: int

def get_key(x: int, y: int):
    return '{}_{}'.format(x, y)

def get_boss_moves(const_board, board_size: (int, int)):
    width, height = board_size
    tiles: list[Tile] = []
    tile_dict = {}
    # player 1 data
    my_tiles = []
    my_units = []
    my_recyclers = []
    can_spawn_tiles = []
    can_recyclers_tiles = []
    # player 2 data
    opp_tiles = []
    opp_units = []
    opp_recyclers = []
    # Neutral data
    neutral_tiles = []

    for item in const_board:
        x, y, scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = item
        tile = Tile(x, y, scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler)

        tiles.append(tile)
        tile_dict[get_key(x, y)] = tile

        if tile.owner == ME:
            my_tiles.append(tile)
            if tile.units > 0:
                my_units.append(tile)
            elif tile.recycler:
                my_recyclers.append(tile)
            elif tile.can_spawn:
                can_spawn_tiles.append(tile)
            if tile.can_build:
                can_recyclers_tiles.append(tile)
        elif tile.owner == OPP:
            opp_tiles.append(tile)
            if tile.units > 0:
                opp_units.append(tile)
            elif tile.recycler:
                opp_recyclers.append(tile)
        else:
            if tile.scrap_amount != 0:
                neutral_tiles.append(tile)

    actions = []

    target = [(1, 1), (12, 1), (12, 5), (1, 5)]
    i = 0
    for unit in my_units:
        amount = unit.units
        target_x, target_y = target[i]
        actions.append('MOVE {} {} {} {} {}'.format(amount, unit.x, unit.y, target_x, target_y))
        i += 1

    # invalid test
    # x: int = int(width/2)
    # y: int = int(height/2)
    # actions.append('MOVE {} {} {} {} {}'.format(1, x, y, 1, 1))
    # actions.append('MOVE {} {} {} {} {}'.format(1, my_units[0].x + 1, my_units[0].y, 1, 1))

    return_string = ';'.join(actions) if len(actions) > 0 else 'WAIT'
    return return_string
