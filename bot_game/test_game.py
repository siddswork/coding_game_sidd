import string
import unittest

from main import filter_out_of_board, initialize_board, coordinate, Tile, filter_grass_and_recyclers, \
    find_valid_next_steps, find_path, find_next_step

BOARD_SIZE = (14, 7)  # board_size = (width, height)
BOARD_X_MAX, BOARD_Y_MAX = BOARD_SIZE


def possible_four_moves(x, y):
    # up, down, left & right
    return [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]


class MethodTest(unittest.TestCase):
    def test_filter_within_board_0_0(self):
        possible_next = possible_four_moves(0, 0)
        valid_next = list(filter(filter_out_of_board, possible_next))
        self.assertEqual(True, valid_next == [(0, 1), (1, 0)])  # add assertion here

    def test_filter_within_board_13_6(self):
        possible_next = possible_four_moves(13, 6)
        valid_next = list(filter(filter_out_of_board, possible_next))
        self.assertEqual(True, valid_next == [(13, 5), (12, 6)])  # add assertion here

    def test_filter_within_board_13_0(self):
        possible_next = possible_four_moves(13, 0)
        valid_next = list(filter(filter_out_of_board, possible_next))
        self.assertEqual(True, valid_next == [(13, 1), (12, 0)])  # add assertion here

    def test_filter_within_board_0_6(self):
        possible_next = possible_four_moves(0, 6)
        valid_next = list(filter(filter_out_of_board, possible_next))
        self.assertEqual(True, valid_next == [(0, 5), (1, 6)])  # add assertion here

    def test_filter_grass_with_filter_grass_and_recyclers(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(0, 1)].recycler = True
        valid_next = find_valid_next_steps(board_dict, 0, 0)
        possible_next = possible_four_moves(0, 0)
        valid_next = list(filter(filter_out_of_board, possible_next))
        valid_next = list(filter(lambda pos: filter_grass_and_recyclers(pos, board_dict), valid_next))
        self.assertEqual([(1, 0)], valid_next)

    def test_filter_recyclers_with_filter_grass_and_recyclers(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(0, 1)].scrap_amount = 0
        valid_next = find_valid_next_steps(board_dict, 0, 0)
        self.assertEqual([(1, 0)], valid_next)

    def test_filter_both_with_filter_grass_and_recyclers(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(0, 1)].scrap_amount = 0
        board_dict[coordinate(1, 0)].recycler = True
        valid_next = find_valid_next_steps(board_dict, 0, 0)
        self.assertEqual(0, len(valid_next))

    def test_find_path_with_same_source_and_target(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(1, 0)].scrap_amount = 0
        board_dict[coordinate(1, 1)].recycler = True
        board_dict[coordinate(1, 2)].scrap_amount = 0
        bot_x, bot_y = (0, 0)
        target_x, target_y = (0, 0)
        has_path, valid_path = find_path(board_dict, bot_x, bot_y, target_x, target_y)
        self.assertEqual(True, has_path)
        self.assertEqual(('0,0', '0,0'), valid_path)

    def test_find_path_complex(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(1, 0)].scrap_amount = 0
        board_dict[coordinate(1, 1)].recycler = True
        board_dict[coordinate(1, 2)].scrap_amount = 0
        bot_x, bot_y = (0, 0)
        target_x, target_y = (2, 0)
        has_path, valid_path = find_path(board_dict, bot_x, bot_y, target_x, target_y)
        self.assertEqual(True, has_path)
        self.assertEqual(('0,0', '0,1', '0,2', '0,3', '1,3', '2,3', '2,2', '2,1', '2,0'), valid_path)

    def test_failed_find_path(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(1, 0)].scrap_amount = 0
        board_dict[coordinate(1, 1)].recycler = True
        board_dict[coordinate(1, 2)].scrap_amount = 0
        board_dict[coordinate(0, 3)].scrap_amount = 0
        bot_x, bot_y = (0, 0)
        target_x, target_y = (2, 0)
        has_path, valid_path = find_path(board_dict, bot_x, bot_y, target_x, target_y)
        self.assertEqual(False, has_path)
        self.assertEqual((), valid_path)

    def test_find_next_step_edge(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(1, 0)].scrap_amount = 0
        board_dict[coordinate(1, 1)].recycler = True
        board_dict[coordinate(1, 2)].scrap_amount = 0
        bot_x, bot_y = (0, 0)
        target_x, target_y = (0, 0)
        x, y = find_next_step(board_dict, bot_x, bot_y, target_x, target_y)
        self.assertEqual(0, x)
        self.assertEqual(0, y)

    def test_find_next_step_complex(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(1, 0)].scrap_amount = 0
        board_dict[coordinate(1, 1)].recycler = True
        board_dict[coordinate(1, 2)].scrap_amount = 0
        bot_x, bot_y = (0, 0)
        target_x, target_y = (2, 0)
        x, y = find_next_step(board_dict, bot_x, bot_y, target_x, target_y)
        self.assertEqual(0, x)
        self.assertEqual(1, y)
        #self.assertEqual(True, valid_path == ('0,0', '0,1', '0,2', '0,3', '1,3', '2,3', '2,2', '2,1', '2,0'))

    def test_find_next_step_none(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(1, 0)].scrap_amount = 0
        board_dict[coordinate(1, 1)].recycler = True
        board_dict[coordinate(1, 2)].scrap_amount = 0
        board_dict[coordinate(0, 3)].scrap_amount = 0
        bot_x, bot_y = (0, 0)
        target_x, target_y = (2, 0)
        x, y = find_next_step(board_dict, bot_x, bot_y, target_x, target_y)
        # going back to previous step
        self.assertEqual(0, x)
        self.assertEqual(1, y)

    def test_find_next_step_cant_move(self):
        board_dict: dict[string, Tile] = initialize_board()
        board_dict[coordinate(1, 0)].scrap_amount = 0
        board_dict[coordinate(1, 1)].recycler = True
        board_dict[coordinate(1, 2)].scrap_amount = 0
        board_dict[coordinate(0, 1)].scrap_amount = 0
        bot_x, bot_y = (0, 0)
        target_x, target_y = (2, 0)
        x, y = find_next_step(board_dict, bot_x, bot_y, target_x, target_y)
        # Can't move at all
        self.assertEqual(0, x)
        self.assertEqual(0, y)

    def test_BFS(self):
        graph = {
            '5': ['3', '7'],
            '3': ['2', '4'],
            '7': ['8'],
            '2': ['6', '1'],
            '4': ['8'],
            '8': [],
            '6': [],
            '1': []
        }

        visited = []  # List for visited nodes.
        queue = []  # Initialize a queue
        start = '5'
        target = '9'
        paths = [(start)]


        visited.append(start)
        queue.append(start)

        def fun(path, node_str):
            if type(path) is tuple:
                if path[-1] == node_str:
                    return path
            else:
                if path == node_str:
                    return path

        while queue:  # Creating loop to visit each node
            m = queue.pop(0)
            # print(m, end=" ")

            for neighbour in graph[m]:
                if neighbour not in visited:
                    path = list(filter(lambda path: fun(path, m), paths))
                    new_path = ()
                    if type(path[0]) is tuple:
                        new_path = path[0] + (neighbour,)
                        paths.append(new_path)
                    else:
                        new_path = (path[0], neighbour)
                        paths.append(new_path)
                    if neighbour == target:
                        print(f'Path to {target} is {new_path}')
                        queue = []
                        break
                    else:
                        paths.append(new_path)
                    visited.append(neighbour)
                    queue.append(neighbour)
        # print('Path not found')


if __name__ == '__main__':
    unittest.main()
