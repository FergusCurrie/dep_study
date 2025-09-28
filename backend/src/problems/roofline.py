import random
from .problem_base import Problem
from .utils.options import generate_options


class Roofline(Problem):
    def generate_problem(self):
        peak_flops_gflops = random.randint(2,5) * 100
        peak_bandwidth = random.randint(2,5) * 100
        flop_per_thread = random.randint(5,10)
        memory_access_per_thread = random.randint(5,10)
        
        memory_access_size_bits = random.choice([8, 16, 32, 64, 128, 256])
        
        problem_data = {
            'flop_per_thread': flop_per_thread,
            'memory_access_per_thread' : memory_access_per_thread,
            'memory_access_size_bits' : memory_access_size_bits,
            'peak_flops_gflops' : peak_flops_gflops,
            'peak_bandwidth': peak_bandwidth
        }
        
        # Generate question using template text with string interpolation
        markdown_question = f"""# GPU roofline model 

Determine (True/False) if kernel is memory bound:

- Peak throughput in GFLOPs = {peak_flops_gflops}
- Peak bandwidth = {peak_bandwidth}
- Flops per thread = {flop_per_thread}
- memory access per thread = {memory_access_per_thread}
- memory access size = {memory_access_size_bits}"""
        answer = self.solve(flop_per_thread, memory_access_size_bits, memory_access_per_thread, peak_bandwidth, peak_flops_gflops)
        solution_explanation = self.get_solution_explanation(problem_data, answer)
        
        options, correct_index = generate_options(answer)

        return {
            'question': markdown_question,
            'options': options,
            'correct': correct_index,
            'solution_explanation': solution_explanation
        }

    def solve(self, flop_per_thread, memory_access_size_bits, memory_access_per_thread, peak_bandwidth, peak_flops_gflops):
        bytes_per_thread = (memory_access_size_bits / 8) * memory_access_per_thread
        ai = flop_per_thread / bytes_per_thread

        throughput = ai * peak_bandwidth

        memory_bound = int(throughput < peak_flops_gflops)
        return memory_bound
    
    def get_solution_explanation(self, problem_data, answer):
        flop_per_thread = problem_data['flop_per_thread']
        memory_access_per_thread = problem_data['memory_access_per_thread']
        memory_access_size_bits = problem_data['memory_access_size_bits']
        peak_flops_gflops = problem_data['peak_flops_gflops']
        peak_bandwidth = problem_data['peak_bandwidth']
        
        bytes_per_thread = (memory_access_size_bits / 8) * memory_access_per_thread
        ai = flop_per_thread / bytes_per_thread
        throughput = ai * peak_bandwidth
        
        explanation = f"""## Solution Explanation

**Given:**
- FLOPS per thread: {flop_per_thread}
- Memory accesses per thread: {memory_access_per_thread}
- Memory access size: {memory_access_size_bits} bits
- Peak FLOPS: {peak_flops_gflops} GFLOPS
- Peak bandwidth: {peak_bandwidth} GB/s

**Step 1: Calculate bytes per thread**
Bytes per thread = ({memory_access_size_bits} bits ÷ 8) × {memory_access_per_thread} = {bytes_per_thread} bytes

**Step 2: Calculate arithmetic intensity**
Arithmetic intensity = {flop_per_thread} FLOPS ÷ {bytes_per_thread} bytes = {ai:.2f} FLOPS/byte

**Step 3: Calculate theoretical throughput**
Throughput = {ai:.2f} FLOPS/byte × {peak_bandwidth} GB/s = {throughput:.2f} GFLOPS

**Step 4: Determine if memory-bound**
Since {throughput:.2f} GFLOPS < {peak_flops_gflops} GFLOPS, the kernel is memory-bound.

**Answer:** {"Memory-bound" if answer == 1 else "Compute-bound"}

**Note:** A kernel is memory-bound when its theoretical throughput is limited by memory bandwidth rather than compute capability."""
        
        return explanation
