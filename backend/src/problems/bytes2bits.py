
import random
from .problem_base import Problem
from .utils.options import generate_options
from .utils.template import render_template


class Bytes2Bits(Problem):
    def generate_problem(self):
        x = random.randint(0,10)
        data = {
            'input_bytes': x
        }
        markdown_question = render_template('problem_templates/bytes2bits.j2', data)
        answer = self.solve(x)
        
        options, correct_index = generate_options(answer)

        return {
            'question': markdown_question,
            'options': options,
            'correct': correct_index
        }

    def solve(self, bytes):
        return bytes * 8


if __name__ == "__main__":
    
    prob = Bytes2Bits().generate_problem()
    print(prob)

