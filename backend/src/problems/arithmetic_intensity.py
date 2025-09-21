import random
from jinja2 import Environment, FileSystemLoader


def _solve(flop_per_thread, memory_access_size_bits, memory_access_per_thread):
    bytes_per_thread = (memory_access_size_bits / 8) * memory_access_per_thread
    return round(flop_per_thread / bytes_per_thread, 2)

def generate_problem():
    flop_per_thread = random.randint(5,30)
    memory_access_per_thread = random.randint(5,30)
    memory_access_size_bits = random.choice([8, 16, 32, 64, 128, 256])
    


    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('problem_templates/arithmetic_intensity.j2')
    data = {
        'flop_per_thread': flop_per_thread,
        'memory_access_per_thread' : memory_access_per_thread,
        'memory_access_size_bits' : memory_access_size_bits

    }
    markdown_question = template.render(data)
    answer = _solve(flop_per_thread, memory_access_size_bits, memory_access_per_thread)

    return {
        'question': markdown_question,
        'options': [f"{answer}", f"{answer+1}", f"{answer-1}", f"{answer+2}"],
        'correct': 0
    }



if __name__ == "__main__":
    
    prob = generate_problem()
    print(prob)

