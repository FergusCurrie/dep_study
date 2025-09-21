
import random 
from jinja2 import Environment, FileSystemLoader


def _solve(bits, clock_freq, data_rate):
    return (bits / 8) * clock_freq * data_rate

def generate_problem():
    bits = random.choice([8, 16, 32, 64, 128, 256])
    clock_freq = random.choice([0.25, 0.5, 1])
    DATA_RATE = 2 # double data rate 
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('problem_templates/ram_bandwidth.j2')
    data = {
        'bits': bits,
        'clock_freq': clock_freq
    }
    markdown_question = template.render(data)
    answer = _solve(bits, clock_freq, DATA_RATE)

    return {
        'question': markdown_question,
        'options': [f"{answer}", f"{answer+1}", f"{answer-1}", f"{answer+2}"],
        'correct': 0
    }



if __name__ == "__main__":
    
    prob = generate_problem()
    print(prob)

