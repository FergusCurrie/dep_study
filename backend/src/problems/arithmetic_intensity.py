import random
from .problem_base import Problem
from .utils.options import generate_options
from .utils.template import render_template


class ArithmeticIntensity(Problem):
    def generate_problem(self):
        flop_per_thread = random.randint(5,30)
        memory_access_per_thread = random.randint(5,30)
        memory_access_size_bits = random.choice([8, 16, 32, 64, 128, 256])
        


        data = {
            'flop_per_thread': flop_per_thread,
            'memory_access_per_thread' : memory_access_per_thread,
            'memory_access_size_bits' : memory_access_size_bits

        }
        markdown_question = render_template('problem_templates/arithmetic_intensity.j2', data)
        answer = self.solve(flop_per_thread, memory_access_size_bits, memory_access_per_thread)
        
        options, correct_index = generate_options(answer)

        return { # TODO: make data model 
            'question': markdown_question,
            'options': options,
            'correct': correct_index
        }

    def solve(self, flop_per_thread, memory_access_size_bits, memory_access_per_thread):
        bytes_per_thread = (memory_access_size_bits / 8) * memory_access_per_thread
        return round(flop_per_thread / bytes_per_thread, 2)
        #return _solve(problem['flop_per_thread'], problem['memory_access_size_bits'], problem['memory_access_per_thread'])



if __name__ == "__main__":
    
    prob = ArithmeticIntensity().generate_problem()
    print(prob)

