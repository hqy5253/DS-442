from collections import deque
from classes.puzzle import Puzzle

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
                    if not new_puzzle.is_solved:
                        self.visited.add(new_puzzle.value)
                        self.stack.append(new_puzzle)

        return False
    
    def get_solution(self) -> list:
        """
        Get the solution path
        :return: list
        """
        return self.solution