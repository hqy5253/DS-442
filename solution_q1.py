from collections import deque


class Puzzle:
    """
    Puzzle class to represent the 8-block puzzle
    """

    def __init__(self, puzzle_string: str):
        """
        Initialize the Puzzle object
        :param puzzle_string: str
        """
        self.value = self.__load_puzzle(puzzle_string)
        self.is_solvable = self.__is_solvable()
        if not self.is_solvable:
            raise ValueError('Puzzle is not solvable')
        self.is_solved = self.__is_solved()
        self.moves = []

    # ---- Helper Functions ----

    def __is_solvable(self) -> bool:
        inversions = 0
        self.state = self.value.replace('_', '9')
        for i in range(len(self.state)):
            for j in range(i + 1, len(self.state)):
                if self.state[i] != "9" and self.state[j] != "9" and self.state[i] > self.state[j]:
                    inversions += 1
        return inversions % 2 == 0

    def __is_solved(self) -> bool:
        """
        Check if the puzzle is solved
        :return: bool
        """
        return self.value == '_12345678'

    def __load_puzzle(self, puzzle_string: str) -> str:
        """
        Load the puzzle string and return it
        :param puzzle_string: str
        :return: str
        """
        if ',' in puzzle_string:
            puzzle_string = puzzle_string.replace(',', '')
        if len(puzzle_string) != 9:
            raise ValueError('Invalid input')
        return puzzle_string

    # ---- Use Functions ----

    def execute_move(self, move: dict) -> 'Puzzle':
        """
        Execute a move on the puzzle
        :param move: dict
        :return: Puzzle
        """
        new_value = list(self.value)
        new_value[move['replacement_index']], new_value[self.value.index('_')] = new_value[self.value.index('_')], move[
            'replacement_value']
        new_puzzle = Puzzle(''.join(new_value))
        new_puzzle.moves = self.moves + [move['move']]
        new_puzzle.heuristic = move['heuristic']
        return new_puzzle

    @property
    def available_moves(self) -> list:
        """
        Get the available moves for the puzzle
        :return: list
        """
        blank_index = self.value.index('_')
        i, j = divmod(blank_index, 3)
        moves = []
        if i < 2:  # Blank can move up
            replacement_index = blank_index + 3
            move = {'direction': 'D', 'replacement_index': replacement_index,
                    'replacement_value': self.value[replacement_index],
                    'move': f'{self.value[replacement_index]}U',
                    'heuristic': self.__manhattan_distance(replacement_index)}
            moves.append(move)
        if i > 0:  # Blank can move down
            replacement_index = blank_index - 3
            move = {'direction': 'U', 'replacement_index': replacement_index,
                    'replacement_value': self.value[replacement_index],
                    'move': f'{self.value[replacement_index]}D',
                    'heuristic': self.__manhattan_distance(replacement_index)}
            moves.append(move)
        if j < 2:  # Blank can move left
            replacement_index = blank_index + 1
            move = {'direction': 'R', 'replacement_index': replacement_index,
                    'replacement_value': self.value[replacement_index],
                    'move': f'{self.value[replacement_index]}L',
                    'heuristic': self.__manhattan_distance(replacement_index)}
            moves.append(move)
        if j > 0:  # Blank can move right
            replacement_index = blank_index - 1
            move = {'direction': 'L', 'replacement_index': replacement_index,
                    'replacement_value': self.value[replacement_index],
                    'move': f'{self.value[replacement_index]}R',
                    'heuristic': self.__manhattan_distance(replacement_index)}
            moves.append(move)
        return moves

    def __manhattan_distance(self, index: int) -> int:
        """
        Calculate the Manhattan distance between the current index and the goal index
        :param index: int
        :return: int
        """
        goal_index = '_12345678'.index(self.value[index])
        goal_i, goal_j = divmod(goal_index, 3)
        i, j = divmod(index, 3)
        return abs(goal_i - i) + abs(goal_j - j)

    def __repr__(self) -> str:
        """
        String representation of the Puzzle object
        :return: str
        """
        # Print the puzzle in a 3x3 grid
        return f'\n{" ".join(self.value[:3])}\n{" ".join(self.value[3:6])}\n{" ".join(self.value[6:])}\n'


# Question 1.1.a
class DFS:
    """
    Depth First Search class to solve the 8-puzzle problem
    Written by: Luke Kerwin
    """

    def __init__(self):
        self.visited = set()
        self.stack = deque()
        self.solution = []

    def dfs(self, puzzle: Puzzle) -> bool:
        """
        Iterative function to solve the 8-puzzle problem
        :param puzzle: Puzzle object
        :return: True if solved, False if not
        """
        self.visited.add(puzzle.value)
        self.stack.append(puzzle)

        while self.stack:
            current_puzzle = self.stack.pop()
            if current_puzzle.is_solved:
                self.solution = current_puzzle.moves
                return True

            for move in current_puzzle.available_moves:
                new_puzzle = current_puzzle.execute_move(move)
                if new_puzzle.value not in self.visited:
                    self.visited.add(new_puzzle.value)
                    self.stack.append(new_puzzle)

        return False

    def get_solution(self) -> list:
        """
        Get the solution path
        :return: list
        """
        return self.solution


# Question 1.1.b
class BFS:
    """
    Breadth First Search class to solve the 8-puzzle problem
    Written by: Luke Kerwin
    """

    def __init__(self):
        self.visited = set()
        self.queue = deque()
        self.solution = []

    def bfs(self, puzzle: Puzzle) -> bool:
        """
        Function to solve the 8-puzzle problem
        :param puzzle: Puzzle object
        :return: True if solved, False if not
        """
        self.visited.add(puzzle.value)
        self.queue.append(puzzle)
        while self.queue:
            current_puzzle = self.queue.popleft()
            if current_puzzle.is_solved:
                self.solution = current_puzzle.moves
                return True
            for move in current_puzzle.available_moves:
                new_puzzle = current_puzzle.execute_move(move)
                if new_puzzle.value not in self.visited:
                    self.visited.add(new_puzzle.value)
                    self.queue.append(new_puzzle)
        return False

    def get_solution(self) -> list:
        """
        Get the solution path
        :return: list
        """
        return self.solution


# Question 1.1.c
class UCS:
    """
    Uniform Cost Search class to solve the 8-puzzle problem
    Written by: Luke Kerwin
    """

    def __init__(self) -> None:
        self.visited = set()
        self.queue = deque()
        self.solution = []

    def ucs(self, puzzle: Puzzle) -> bool:
        """
        Function to solve the 8-puzzle problem
        :param puzzle: Puzzle object
        :return: True if solved, False if not
        """
        self.visited.add(puzzle.value)
        self.queue.append(puzzle)
        while self.queue:
            current_puzzle = self.queue.popleft()
            if current_puzzle.is_solved:
                self.solution = current_puzzle.moves
                return True
            for move in current_puzzle.available_moves:
                new_puzzle = current_puzzle.execute_move(move)
                if new_puzzle.value not in self.visited:
                    self.visited.add(new_puzzle.value)
                    self.queue.append(new_puzzle)
            self.queue = deque(sorted(self.queue, key=lambda x: len(x.moves)))
        return False

    def get_solution(self) -> list:
        """
        Get the solution path
        :return: list
        """
        return self.solution


# Question 1.1.d
class AStar:
    """
    A* Search class to solve the 8-puzzle problem
    Written by: Luke Kerwin
    """

    def __init__(self) -> None:
        self.visited = set()
        self.queue = deque()
        self.solution = []

    def a_star(self, puzzle: Puzzle) -> bool:
        """
        Function to solve the 8-puzzle problem
        :param puzzle: Puzzle object
        :return: True if solved, False if not
        """
        self.visited.add(puzzle.value)
        self.queue.append(puzzle)
        while self.queue:
            current_puzzle = self.queue.popleft()
            if current_puzzle.is_solved:
                self.solution = current_puzzle.moves
                return True
            for move in current_puzzle.available_moves:
                new_puzzle = current_puzzle.execute_move(move)
                if new_puzzle.value not in self.visited:
                    self.visited.add(new_puzzle.value)
                    self.queue.append(new_puzzle)
            self.queue = deque(sorted(self.queue, key=lambda x: len(x.moves) + x.heuristic))
        return False

    def get_solution(self) -> list:
        """
        Get the solution path
        :return: list
        """
        return self.solution


# Question 1.1.e
class SL_Puzzle:
    """
    Puzzle class to represent the 8-block puzzle that uses Straight Line Distance heuristic
    """

    def __init__(self, puzzle_string: str):
        """
        Initialize the Puzzle object
        :param puzzle_string: str
        """
        self.value = self.__load_puzzle(puzzle_string)
        self.is_solvable = self.__is_solvable()
        if not self.is_solvable:
            raise ValueError('Puzzle is not solvable')
        self.is_solved = self.__is_solved()
        self.moves = []

    # ---- Helper Functions ----

    def __is_solvable(self) -> bool:
        inversions = 0
        self.state = self.value.replace('_', '9')
        for i in range(len(self.state)):
            for j in range(i + 1, len(self.state)):
                if self.state[i] != "9" and self.state[j] != "9" and self.state[i] > self.state[j]:
                    inversions += 1
        return inversions % 2 == 0

    def __is_solved(self) -> bool:
        """
        Check if the puzzle is solved
        :return: bool
        """
        return self.value == '_12345678'

    def __load_puzzle(self, puzzle_string: str) -> str:
        """
        Load the puzzle string and return it
        :param puzzle_string: str
        :return: str
        """
        if ',' in puzzle_string:
            puzzle_string = puzzle_string.replace(',', '')
        if len(puzzle_string) != 9:
            raise ValueError('Invalid input')
        return puzzle_string

    # ---- Use Functions ----

    def execute_move(self, move: dict) -> 'SL_Puzzle':
        """
        Execute a move on the puzzle
        :param move: dict
        :return: SL_Puzzle
        """
        new_value = list(self.value)
        new_value[move['replacement_index']], new_value[self.value.index('_')] = new_value[self.value.index('_')], move[
            'replacement_value']
        new_puzzle = SL_Puzzle(''.join(new_value))
        new_puzzle.moves = self.moves + [move['move']]
        new_puzzle.heuristic = move['heuristic']
        return new_puzzle

    @property
    def available_moves(self) -> list:
        """
        Get the available moves for the puzzle
        :return: list
        """
        blank_index = self.value.index('_')
        i, j = divmod(blank_index, 3)
        moves = []
        if i < 2:
            replacement_index = blank_index + 3
            move = {'direction': 'D', 'replacement_index': replacement_index,
                    'replacement_value': self.value[replacement_index],
                    'move': f'{self.value[replacement_index]}U',
                    'heuristic': self.__straight_line_distance(replacement_index)}
            moves.append(move)
        if i > 0:
            replacement_index = blank_index - 3
            move = {'direction': 'U', 'replacement_index': replacement_index,
                    'replacement_value': self.value[replacement_index],
                    'move': f'{self.value[replacement_index]}D',
                    'heuristic': self.__straight_line_distance(replacement_index)}
            moves.append(move)
        if j < 2:
            replacement_index = blank_index + 1
            move = {'direction': 'R', 'replacement_index': replacement_index,
                    'replacement_value': self.value[replacement_index],
                    'move': f'{self.value[replacement_index]}L',
                    'heuristic': self.__straight_line_distance(replacement_index)}
            moves.append(move)
        if j > 0:
            replacement_index = blank_index - 1
            move = {'direction': 'L', 'replacement_index': replacement_index,
                    'replacement_value': self.value[replacement_index],
                    'move': f'{self.value[replacement_index]}R',
                    'heuristic': self.__straight_line_distance(replacement_index)}
            moves.append(move)
        return moves

    def __straight_line_distance(self, index: int) -> int:
        """
        Calculate the Straight Line Distance between the current index and the goal index
        :param index: int
        :return: int
        """
        goal_index = '_12345678'.index(self.value[index])
        goal_i, goal_j = divmod(goal_index, 3)
        i, j = divmod(index, 3)
        distance = 0
        for row in range(3):
            for col in range(3):
                tile_index = row * 3 + col
                tile_i, tile_j = divmod(tile_index, 3)
                tile_value = self.value[tile_index]
                if tile_value != '_':
                    goal_tile_index = '_12345678'.index(tile_value)
                    goal_tile_i, goal_tile_j = divmod(goal_tile_index, 3)
                    distance += abs(goal_tile_i - tile_i) + abs(goal_tile_j - tile_j)
        return distance

    def __repr__(self) -> str:
        """
        String representation of the Puzzle object
        :return: str
        """
        # Print the puzzle in a 3x3 grid
        return f'\n{" ".join(self.value[:3])}\n{" ".join(self.value[3:6])}\n{" ".join(self.value[6:])}\n'


if __name__ == '__main__':
    # Assuming input.txt is in the same directory as this file
    with open('input.txt', 'r') as f:
        puzzle_string = f.readline().strip().replace(',', '')
        f.close()

    puzzle = Puzzle(puzzle_string)

    # Question 1.2.a
    dfs = DFS()
    dfs.dfs(puzzle)
    print(','.join(dfs.get_solution()))

    # Question 1.2.a times out, but Professor said it's okay

    # Question 1.2.b
    bfs = BFS()
    bfs.bfs(puzzle)
    print(','.join(bfs.get_solution()))

    # Question 1.2.c
    ucs = UCS()
    ucs.ucs(puzzle)
    print(','.join(ucs.get_solution()))

    # Question 1.2.d
    a_star = AStar()
    a_star.a_star(puzzle)
    print(','.join(a_star.get_solution()))

    # Question 1.2.e
    sl_puzzle = SL_Puzzle(puzzle_string)
    a_star2 = AStar()
    a_star2.a_star(sl_puzzle)
    print(','.join(a_star2.get_solution()))