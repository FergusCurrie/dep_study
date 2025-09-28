
import random
from .problem_base import Problem
from .utils.options import generate_options


class Bytes2Bits(Problem):
    def generate_problem(self):
        x = random.randint(0,10)
        problem_data = {
            'input_bytes': x
        }
        # Generate question using template text with string interpolation
        markdown_question = f"""# Bit to byte 

Convert {x} bytes to bits."""
        answer = self.solve(x)
        solution_explanation = self.get_solution_explanation(problem_data, answer)
        
        options, correct_index = generate_options(answer)

        return {
            'question': markdown_question,
            'options': options,
            'correct': correct_index,
            'solution_explanation': solution_explanation
        }

    def solve(self, bytes):
        return bytes * 8
    
    def get_solution_explanation(self, problem_data, answer):
        input_bytes = problem_data['input_bytes']
        
        explanation = f"""## Solution Explanation

**Given:**
- Input: {input_bytes} bytes

**Step 1: Convert bytes to bits**
Since 1 byte = 8 bits:
{input_bytes} bytes × 8 bits/byte = {answer} bits

**Answer:** {answer} bits

**Note:** This is a simple unit conversion. Each byte contains 8 bits, so we multiply the number of bytes by 8 to get the total number of bits."""
        
        return explanation


if __name__ == "__main__":
    
    prob = Bytes2Bits().generate_problem()
    print(prob)

