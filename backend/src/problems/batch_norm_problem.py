import random
from .problem_base import Problem
from .utils.options import generate_options


class BatchNormProblem(Problem):
    """
    Generate a batch normalization problem asking students to compute the normalized output.
    
    Given a mini-batch of values x = [x1, x2, x3], compute the batch-normalized output:
    
    1. Compute batch mean: μ = (1/m) Σ xi
    2. Compute batch variance: σ² = (1/m) Σ (xi - μ)²
    3. Normalize: x̂i = (xi - μ) / sqrt(σ² + ε)
    4. Scale and shift: yi = γ * x̂i + β
    
    We keep batch size small (m=3) for hand calculations.
    We ask for one specific output value yi.
    """

    def generate_problem(self):
        # Generate a mini-batch of 3 values
        # Keep values small for easier hand calculation
        x1 = random.randint(-10, 10)
        x2 = random.randint(-10, 10)
        x3 = random.randint(-10, 10)
        
        # Learnable parameters gamma (scale) and beta (shift)
        gamma = random.choice([0.5, 1.0, 1.5, 2.0])
        beta = random.randint(-5, 5)
        
        # Small epsilon for numerical stability
        epsilon = 0.01
        
        # Which output to ask for (0, 1, or 2)
        output_index = random.randint(0, 2)
        
        data = {
            "x": [x1, x2, x3],
            "gamma": gamma,
            "beta": beta,
            "epsilon": epsilon,
            "output_index": output_index,
        }

        markdown_question = self._question_markdown(data)
        answer = self.solve(data)
        solution_explanation = self.get_solution_explanation(data, answer)
        options, correct_index = generate_options(answer)

        return {
            "question": markdown_question,
            "options": options,
            "correct": correct_index,
            "solution_explanation": solution_explanation,
        }

    def solve(self, data):
        x = data["x"]
        gamma = data["gamma"]
        beta = data["beta"]
        epsilon = data["epsilon"]
        output_index = data["output_index"]
        
        # Step 1: Compute batch mean
        mu = sum(x) / len(x)
        
        # Step 2: Compute batch variance
        variance = sum((xi - mu)**2 for xi in x) / len(x)
        
        # Step 3: Normalize
        x_normalized = [(xi - mu) / (variance + epsilon)**0.5 for xi in x]
        
        # Step 4: Scale and shift
        y = [gamma * x_hat + beta for x_hat in x_normalized]
        
        return round(y[output_index], 2)

    def get_solution_explanation(self, data, answer):
        x = data["x"]
        gamma = data["gamma"]
        beta = data["beta"]
        epsilon = data["epsilon"]
        output_index = data["output_index"]
        
        md = []
        md.append("# Batch Normalization Calculation")
        md.append("")
        md.append("Batch normalization transforms inputs using the following steps:")
        md.append("")
        
        # Step 1: Mean
        md.append("**Step 1: Compute batch mean**")
        md.append("")
        mu = sum(x) / len(x)
        x_str = " + ".join(str(xi) for xi in x)
        md.append(
            rf"$$ \mu = \frac{{1}}{{m}} \sum_{{i=1}}^{{m}} x_i = \frac{{1}}{{3}}({x_str}) = \frac{{{sum(x)}}}{{3}} = {mu:.4f} $$"
        )
        md.append("")
        
        # Step 2: Variance
        md.append("**Step 2: Compute batch variance**")
        md.append("")
        variance = sum((xi - mu)**2 for xi in x) / len(x)
        variance_terms = " + ".join(f"({xi} - {mu:.4f})^2" for xi in x)
        variance_values = " + ".join(f"{(xi - mu)**2:.4f}" for xi in x)
        md.append(
            r"$$ \sigma^2 = \frac{1}{m} \sum_{i=1}^{m} (x_i - \mu)^2 $$"
        )
        md.append("")
        md.append(
            rf"$$ \sigma^2 = \frac{{1}}{{3}}({variance_terms}) $$"
        )
        md.append("")
        md.append(
            rf"$$ \sigma^2 = \frac{{1}}{{3}}({variance_values}) = {variance:.4f} $$"
        )
        md.append("")
        
        # Step 3: Normalize
        md.append("**Step 3: Normalize each value**")
        md.append("")
        std_with_eps = (variance + epsilon)**0.5
        md.append(
            rf"$$ \hat{{x}}_i = \frac{{x_i - \mu}}{{\sqrt{{\sigma^2 + \epsilon}}}} = \frac{{x_i - {mu:.4f}}}{{\sqrt{{{variance:.4f} + {epsilon}}}}} = \frac{{x_i - {mu:.4f}}}{{{std_with_eps:.4f}}} $$"
        )
        md.append("")
        
        x_normalized = [(xi - mu) / std_with_eps for xi in x]
        for i, (xi, x_hat) in enumerate(zip(x, x_normalized, strict=False)):
            md.append(
                rf"$$ \hat{{x}}_{i+1} = \frac{{{xi} - {mu:.4f}}}{{{std_with_eps:.4f}}} = {x_hat:.4f} $$"
            )
        md.append("")
        
        # Step 4: Scale and shift
        md.append("**Step 4: Scale and shift**")
        md.append("")
        md.append(
            rf"$$ y_i = \gamma \hat{{x}}_i + \beta = {gamma} \cdot \hat{{x}}_i + {beta} $$"
        )
        md.append("")
        
        y = [gamma * x_hat + beta for x_hat in x_normalized]
        for i, (x_hat, yi) in enumerate(zip(x_normalized, y, strict=False)):
            md.append(
                rf"$$ y_{i+1} = {gamma} \cdot {x_hat:.4f} + {beta} = {yi:.4f} $$"
            )
        md.append("")
        
        # Final answer
        md.append("**Answer:**")
        md.append("")
        md.append(
            rf"$$ y_{output_index + 1} = {answer:.2f} $$"
        )
        
        return "\n".join(md)

    def _question_markdown(self, data):
        x = data["x"]
        gamma = data["gamma"]
        beta = data["beta"]
        epsilon = data["epsilon"]
        output_index = data["output_index"]
        
        x_tex = rf"\begin{{bmatrix}} {x[0]} \\ {x[1]} \\ {x[2]} \end{{bmatrix}}"
        
        return (
            "# Batch Normalization\n\n"
            "Given a mini-batch of values and batch normalization parameters, "
            f"compute the normalized output $y_{output_index + 1}$.\n\n"
            "**Input batch:**\n\n"
            rf"$$ \mathbf{{x}} = {x_tex} $$"
            "\n\n"
            "**Batch normalization parameters:**\n\n"
            rf"$$ \gamma = {gamma}, \quad \beta = {beta}, \quad \epsilon = {epsilon} $$"
            # "\n\n"
            # "**Batch normalization formula:**\n\n"
            # r"$$ \mu = \frac{1}{m}\sum_{i=1}^{m} x_i $$"
            # "\n\n"
            # r"$$ \sigma^2 = \frac{1}{m}\sum_{i=1}^{m} (x_i - \mu)^2 $$"
            # "\n\n"
            # r"$$ \hat{x}_i = \frac{x_i - \mu}{\sqrt{\sigma^2 + \epsilon}} $$"
            # "\n\n"
            # r"$$ y_i = \gamma \hat{x}_i + \beta $$"
            "\n\n"
            f"Find: $y_{output_index + 1}$\n\n"
            "Round your answer to 2 dp."
        )

if __name__ == "__main__":
    prob = BatchNormProblem().generate_problem()
    print(prob)
