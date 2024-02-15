from collections import deque
from classes.puzzle import Puzzle

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