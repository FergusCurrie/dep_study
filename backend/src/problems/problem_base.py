from abc import ABC, abstractmethod


class Problem(ABC):
    @abstractmethod
    def generate_problem(self):
        pass

    @abstractmethod
    def solve(self, problem):
        pass
    
    @abstractmethod
    def get_solution_explanation(self, problem_data, answer):
        """
        Generate a step-by-step solution explanation for the problem.
        
        Args:
            problem_data: The data used to generate the problem
            answer: The correct answer
            
        Returns:
            str: Markdown-formatted solution explanation
        """
        pass