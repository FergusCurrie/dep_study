
import random
from .problem_base import Problem
from .utils.options import generate_options
from .utils.template import render_template


class RamBandwidth(Problem):
    def generate_problem(self):
        bits = random.choice([8, 16, 32, 64, 128, 256])
        clock_freq = random.choice([0.25, 0.5, 1])
        DATA_RATE = 2 # double data rate 
        data = {
            'bits': bits,
            'clock_freq': clock_freq
        }
        markdown_question = render_template('problem_templates/ram_bandwidth.j2', data)
        answer = self.solve(bits, clock_freq, DATA_RATE)
        
        options, correct_index = generate_options(answer)

        return {
            'question': markdown_question,
            'options': options,
            'correct': correct_index
        }

    def solve(self, bits, clock_freq, data_rate):
        return (bits / 8) * clock_freq * data_rate


if __name__ == "__main__":
    
    prob = RamBandwidth().generate_problem()
    print(prob)

