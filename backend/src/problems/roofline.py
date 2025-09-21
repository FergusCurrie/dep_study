import random
from jinja2 import Environment, FileSystemLoader


def _solve(flop_per_thread, memory_access_size_bits, memory_access_per_thread, peak_bandwidth, peak_flops_gflops):
    bytes_per_thread = (memory_access_size_bits / 8) * memory_access_per_thread
    ai = flop_per_thread / bytes_per_thread

    throughput = ai * peak_bandwidth

    memory_bound = int(throughput < peak_flops_gflops)
    return memory_bound 

def generate_problem():
    peak_flops_gflops = random.randint(2,5) * 100
    peak_bandwidth = random.randint(2,5) * 100
    flop_per_thread = random.randint(5,10)
    memory_access_per_thread = random.randint(5,10)
    
    memory_access_size_bits = random.choice([8, 16, 32, 64, 128, 256])
    


    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('problem_templates/roofline.j2')
    data = {
        'flop_per_thread': flop_per_thread,
        'memory_access_per_thread' : memory_access_per_thread,
        'memory_access_size_bits' : memory_access_size_bits,
        'peak_flops_gflops' : peak_flops_gflops,
        'peak_bandwidth': peak_bandwidth

    }
    markdown_question = template.render(data)
    answer = _solve(flop_per_thread, memory_access_size_bits, memory_access_per_thread, peak_bandwidth, peak_flops_gflops)

    return {
        'question': markdown_question,
        'options': [f"{answer}", f"{answer+1}", f"{answer-1}", f"{answer+2}"],
        'correct': 0
    }
