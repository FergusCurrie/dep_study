from abc import ABC, abstractmethod


class Problem(ABC):
    @abstractmethod
    def generate_problem(self):
        pass

    @abstractmethod
    def solve(self, problem):
        pass