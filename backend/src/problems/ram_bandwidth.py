
import random
from .problem_base import Problem
from .utils.options import generate_options


class RamBandwidth(Problem):
    def generate_problem(self):
        bits = random.choice([8, 16, 32, 64, 128, 256])
        clock_freq = random.choice([0.25, 0.5, 1])
        DATA_RATE = 2 # double data rate 
        problem_data = {
            'bits': bits,
            'clock_freq': clock_freq
        }
        # Generate question using template text with string interpolation
        markdown_question = f"""# Ram bandwidth

Calculate the bandwidth in GB/s for a {bits}-bit DDR bus with clock frequency {clock_freq} GHz: 

"""
        answer = self.solve(bits, clock_freq, DATA_RATE)
        solution_explanation = self.get_solution_explanation(problem_data, answer, DATA_RATE)
        
        options, correct_index = generate_options(answer)

        return {
            'question': markdown_question,
            'options': options,
            'correct': correct_index,
            'solution_explanation': solution_explanation
        }

    def solve(self, bits, clock_freq, data_rate):
        return (bits / 8) * clock_freq * data_rate
    
    def get_solution_explanation(self, problem_data, answer, data_rate):
        bits = problem_data['bits']
        clock_freq = problem_data['clock_freq']
        
        explanation = f"""## Solution Explanation

**Given:**
- Data width: {bits} bits
- Clock frequency: {clock_freq} GHz
- Data rate: {data_rate}x (Double Data Rate)

**Step 1: Convert bits to bytes**
Data width in bytes = {bits} bits ÷ 8 = {bits / 8} bytes

**Step 2: Calculate bandwidth**
Bandwidth = Data width (bytes) × Clock frequency (GHz) × Data rate
Bandwidth = {bits / 8} bytes × {clock_freq} GHz × {data_rate} = {answer} GB/s

**Answer:** {answer} GB/s

**Note:** This calculates the theoretical peak memory bandwidth. DDR (Double Data Rate) memory transfers data on both the rising and falling edges of the clock signal, effectively doubling the data rate."""
        
        return explanation


if __name__ == "__main__":
    
    prob = RamBandwidth().generate_problem()
    print(prob)

