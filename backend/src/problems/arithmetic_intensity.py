import random
from .problem_base import Problem
from .utils.options import generate_options


class ArithmeticIntensity(Problem):
    def generate_problem(self):
        flop_per_thread = random.randint(5,30)
        memory_access_per_thread = random.randint(5,30)
        memory_access_size_bits = random.choice([8, 16, 32, 64, 128, 256])
        
        problem_data = {
            'flop_per_thread': flop_per_thread,
            'memory_access_per_thread' : memory_access_per_thread,
            'memory_access_size_bits' : memory_access_size_bits
        }
        
        # Generate question using template text with string interpolation
        markdown_question = f"""# Arithmetic intensity

Calculate arithmetic intensity for a kernel with {flop_per_thread} flops per thread, {memory_access_per_thread} memory accesses per thread and access size of {memory_access_size_bits} bits. Round to 2dp:"""
        answer = self.solve(flop_per_thread, memory_access_size_bits, memory_access_per_thread)
        solution_explanation = self.get_solution_explanation(problem_data, answer)
        
        options, correct_index = generate_options(answer)

        return {
            'question': markdown_question,
            'options': options,
            'correct': correct_index,
            'solution_explanation': solution_explanation
        }

    def solve(self, flop_per_thread, memory_access_size_bits, memory_access_per_thread):
        bytes_per_thread = (memory_access_size_bits / 8) * memory_access_per_thread
        if bytes_per_thread == 0:
            return float('inf')
        return round(flop_per_thread / bytes_per_thread, 2)
    
    def get_solution_explanation(self, problem_data, answer):
        flop_per_thread = problem_data['flop_per_thread']
        memory_access_per_thread = problem_data['memory_access_per_thread']
        memory_access_size_bits = problem_data['memory_access_size_bits']
        
        return f"""## Solution Explanation

**Given:**
- FLOPS per thread: {flop_per_thread}
- Memory accesses per thread: {memory_access_per_thread}
- Memory access size: {memory_access_size_bits} bits

**Step 1: Convert memory access size to bytes**
Memory access size in bytes = {memory_access_size_bits} bits ÷ 8 = {memory_access_size_bits / 8} bytes

**Step 2: Calculate total bytes accessed per thread**
Total bytes per thread = {memory_access_size_bits / 8} bytes × {memory_access_per_thread} accesses = {(memory_access_size_bits / 8) * memory_access_per_thread} bytes

**Step 3: Calculate arithmetic intensity**
Arithmetic intensity = FLOPS per thread ÷ Bytes per thread
Arithmetic intensity = {flop_per_thread} ÷ {(memory_access_size_bits / 8) * memory_access_per_thread} = {answer}

**Answer:** {answer} FLOPS/byte

**Note:** Arithmetic intensity measures the ratio of floating-point operations to memory bandwidth. Higher values indicate compute-bound kernels, while lower values indicate memory-bound kernels."""



if __name__ == "__main__":
    prob = ArithmeticIntensity().generate_problem()
    print(prob)

