
import random
from jinja2 import Environment, FileSystemLoader


def _solve(bytes):
    return bytes * 8

def generate_problem():
    x = random.randint(0,10)
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('problem_templates/bytes2bits.j2')
    data = {
        'input_bytes': x
    }
    markdown_question = template.render(data)
    answer = _solve(x)

    return {
        'question': markdown_question,
        'options': [f"{answer}", f"{answer+1}", f"{answer-1}", f"{answer+2}"],
        'correct': 0
    }



if __name__ == "__main__":
    
    prob = generate_problem()
    print(prob)

