# import random
# from .problem_base import Problem
# from .utils.options import generate_options


# class LinearProgramDual(Problem):
#     """
#     Generate a convex quadratic problem with equality constraints only and ask for
#     the value of the dual function g(lambda) = min_x f(x) + lambda^T (A x - b)

#     We choose f(x) = 1/2 x^T Q x + c^T x with diagonal positive definite Q,
#     constraints A x = b, and provide a specific lambda.
#     For diagonal Q, g(lambda) has closed form:

#       v = c + A^T lambda
#       g(lambda) = -1/2 * v^T Q^{-1} v - b^T lambda

#     Dimensions are kept small (2 variables, 2 equality constraints) for simplicity.
#     """

#     def generate_problem(self):
#         # Diagonal positive definite Q
#         q1 = random.randint(1, 5)
#         q2 = random.randint(1, 5)

#         # Linear term c
#         c1 = random.randint(-5, 5)
#         c2 = random.randint(-5, 5)

#         # Equality constraints A x = b, A is 2x2 with small ints
#         a11 = random.randint(-3, 3)
#         a12 = random.randint(-3, 3)
#         a21 = random.randint(-3, 3)
#         a22 = random.randint(-3, 3)
#         # Ensure A is not all zeros
#         if a11 == a12 == a21 == a22 == 0:
#             a11 = 1

#         b1 = random.randint(-5, 5)
#         b2 = random.randint(-5, 5)

#         # Provided Lagrange multiplier lambda (2-dim)
#         l1 = random.randint(-3, 3)
#         l2 = random.randint(-3, 3)

#         data = {
#             "Q": [q1, q2],  # diagonal entries
#             "c": [c1, c2],
#             "A": [[a11, a12], [a21, a22]],
#             "b": [b1, b2],
#             "lam": [l1, l2],
#         }

#         markdown_question = self._question_markdown(data)
#         answer = self.solve(data)
#         solution_explanation = self.get_solution_explanation(data, answer)
#         options, correct_index = generate_options(answer)

#         return {
#             "question": markdown_question,
#             "options": options,
#             "correct": correct_index,
#             "solution_explanation": solution_explanation,
#         }

#     def solve(self, data):
#         q1, q2 = data["Q"]
#         c1, c2 = data["c"]
#         (a11, a12), (a21, a22) = data["A"]
#         b1, b2 = data["b"]
#         l1, l2 = data["lam"]

#         # v = c + A^T lambda
#         v1 = c1 + a11 * l1 + a21 * l2
#         v2 = c2 + a12 * l1 + a22 * l2

#         # g(lambda) = -1/2 * v^T Q^{-1} v - b^T lambda
#         quad = (v1 * v1) / q1 + (v2 * v2) / q2
#         btlam = b1 * l1 + b2 * l2
#         g = -0.5 * quad - btlam

#         return round(g, 2)

#     def get_solution_explanation(self, data, answer):
#         q1, q2 = data["Q"]
#         c1, c2 = data["c"]
#         (a11, a12), (a21, a22) = data["A"]
#         b1, b2 = data["b"]
#         l1, l2 = data["lam"]

#         md = []
#         md.append("# Dual function for equality-constrained quadratic")
#         md.append("")
#         md.append("The dual function with equality constraints is:")
#         md.append(
#             r"$ g(\lambda) = \min_{\mathbf{x}} \left[ f(\mathbf{x}) + \lambda^T(\mathbf{A}\mathbf{x} - \mathbf{b}) \right] $"
#         )
#         md.append("")
#         md.append("**Step 1: Expand the Lagrangian**")
#         md.append("")
#         md.append("Substitute $f(\\mathbf{x}) = \\tfrac{1}{2}\\mathbf{x}^T\\mathbf{Q}\\mathbf{x} + \\mathbf{c}^T\\mathbf{x}$:")
#         md.append("")
#         md.append(
#             r"$ L(\mathbf{x}, \lambda) = \tfrac{1}{2}\mathbf{x}^T\mathbf{Q}\mathbf{x} + \mathbf{c}^T\mathbf{x} + \lambda^T\mathbf{A}\mathbf{x} - \lambda^T\mathbf{b} $"
#         )
#         md.append("")
#         md.append("Rewrite $\\lambda^T\\mathbf{A}\\mathbf{x} = (\\mathbf{A}^T\\lambda)^T\\mathbf{x}$ and group the linear terms:")
#         md.append("")
#         md.append(
#             r"$ L(\mathbf{x}, \lambda) = \tfrac{1}{2}\mathbf{x}^T\mathbf{Q}\mathbf{x} + (\mathbf{c} + \mathbf{A}^T\lambda)^T\mathbf{x} - \mathbf{b}^T\lambda $"
#         )
#         md.append("")
#         md.append("**Step 2: Find the minimum by setting gradient to zero**")
#         md.append("")
#         md.append(
#             r"$$ \nabla_{\mathbf{x}} L = \mathbf{Q}\mathbf{x} + (\mathbf{c} + \mathbf{A}^T\lambda) = 0 $$"
#         )
#         md.append("")
#         md.append(
#             r"$$ \mathbf{x}^* = -\mathbf{Q}^{-1}(\mathbf{c} + \mathbf{A}^T\lambda) $$"
#         )
#         md.append("")
#         md.append(
#             "Since $\\mathbf{Q}$ is positive definite, this is indeed a minimum."
#         )
#         md.append("")
#         md.append("**Step 3: Substitute back to get dual function**")
#         md.append("")
#         md.append("Substituting $\\mathbf{x}^* = -\\mathbf{Q}^{-1}(\\mathbf{c} + \\mathbf{A}^T\\lambda)$ back into $L$:")
#         md.append("")
#         md.append(
#             r"$ g(\lambda) = \tfrac{1}{2}(-\mathbf{Q}^{-1}(\mathbf{c} + \mathbf{A}^T\lambda))^T\mathbf{Q}(-\mathbf{Q}^{-1}(\mathbf{c} + \mathbf{A}^T\lambda)) + (\mathbf{c} + \mathbf{A}^T\lambda)^T(-\mathbf{Q}^{-1}(\mathbf{c} + \mathbf{A}^T\lambda)) - \mathbf{b}^T\lambda $"
#         )
#         md.append("")
#         md.append("Simplifying (using $\\mathbf{Q}^T = \\mathbf{Q}$ and $(\\mathbf{Q}^{-1})^T = \\mathbf{Q}^{-1}$ for diagonal $\\mathbf{Q}$):")
#         md.append("")
#         md.append(
#             r"$ g(\lambda) = -\tfrac{1}{2}(\mathbf{c} + \mathbf{A}^T\lambda)^T\mathbf{Q}^{-1}(\mathbf{c} + \mathbf{A}^T\lambda) - \mathbf{b}^T\lambda $"
#         )
#         md.append("")
#         md.append("Let $\\mathbf{v} = \\mathbf{c} + \\mathbf{A}^T\\lambda$ to simplify notation:")
#         md.append("")
#         md.append(
#             r"$ g(\lambda) = -\tfrac{1}{2}\mathbf{v}^T\mathbf{Q}^{-1}\mathbf{v} - \mathbf{b}^T\lambda $"
#         )
#         md.append("")
#         md.append("**Step 4: Calculate for the given values**")
#         md.append("")
        
#         # Calculate A^T lambda
#         atl1 = a11 * l1 + a21 * l2
#         atl2 = a12 * l1 + a22 * l2
#         md.append(
#             rf"$$ \mathbf{{A}}^T\lambda = \begin{{bmatrix}} {a11} & {a21} \\ {a12} & {a22} \end{{bmatrix}} \begin{{bmatrix}} {l1} \\ {l2} \end{{bmatrix}} = \begin{{bmatrix}} {atl1} \\ {atl2} \end{{bmatrix}} $$"
#         )
#         md.append("")
        
#         v1 = c1 + atl1
#         v2 = c2 + atl2
#         md.append(
#             rf"$$ \mathbf{{v}} = \mathbf{{c}} + \mathbf{{A}}^T\lambda = \begin{{bmatrix}} {c1} \\ {c2} \end{{bmatrix}} + \begin{{bmatrix}} {atl1} \\ {atl2} \end{{bmatrix}} = \begin{{bmatrix}} {v1} \\ {v2} \end{{bmatrix}} $$"
#         )
#         md.append("")
        
#         # Calculate v^T Q^{-1} v
#         v_term = (v1**2) / q1 + (v2**2) / q2
#         md.append(
#             rf"$$ \mathbf{{v}}^T\mathbf{{Q}}^{{-1}}\mathbf{{v}} = {v1}^2 \cdot \tfrac{{1}}{{{q1}}} + {v2}^2 \cdot \tfrac{{1}}{{{q2}}} = {v1**2/q1:.2f} + {v2**2/q2:.2f} = {v_term:.2f} $$"
#         )
#         md.append("")
        
#         # Calculate b^T lambda
#         btlam = b1 * l1 + b2 * l2
#         md.append(
#             rf"$$ \mathbf{{b}}^T\lambda = {b1} \cdot {l1} + {b2} \cdot {l2} = {btlam} $$"
#         )
#         md.append("")
        
#         md.append("**Final answer:**")
#         md.append("")
#         md.append(
#             rf"$$ g(\lambda) = -\tfrac{{1}}{{2}} \cdot {v_term:.2f} - ({btlam}) = {-0.5*v_term:.2f} - ({btlam}) = {answer:.2f} $$"
#         )
        
#         return "\n".join(md)

#     def _question_markdown(self, data):
#         q1, q2 = data["Q"]
#         c1, c2 = data["c"]
#         (a11, a12), (a21, a22) = data["A"]
#         b1, b2 = data["b"]
#         l1, l2 = data["lam"]

#         A_tex = rf"\begin{{bmatrix}} {a11} & {a12} \\ {a21} & {a22} \end{{bmatrix}}"
#         b_tex = rf"\begin{{bmatrix}} {b1} \\ {b2} \end{{bmatrix}}"
#         c_tex = rf"\begin{{bmatrix}} {c1} \\ {c2} \end{{bmatrix}}"
#         lam_tex = rf"\begin{{bmatrix}} {l1} \\ {l2} \end{{bmatrix}}"
#         Q_tex = rf"\text{{diag}}({q1}, {q2})"

#         return (
#             "# Dual function value\n\n"
#             "Compute the value of the dual function for the following data (no inequality constraints):\n\n"
#             rf"$$ f(\mathbf{{x}}) = \tfrac{{1}}{{2}}\mathbf{{x}}^T\mathbf{{Q}}\mathbf{{x}} + \mathbf{{c}}^T\mathbf{{x}}, \quad \mathbf{{Q}} = {Q_tex}, \quad \mathbf{{c}} = {c_tex} $$"
#             "\n\n"
#             rf"$$ \mathbf{{A}}x = \mathbf{{b}}, \quad \mathbf{{A}} = {A_tex}, \quad \mathbf{{b}} = {b_tex}, \quad \lambda = {lam_tex} $$"
#             "\n\n"
#             r"Find: $$ g(\lambda) = \min_{\mathbf{x}} \left[ f(\mathbf{x}) + \lambda^T(\mathbf{A}\mathbf{x} - \mathbf{b}) \right] $$"
#             "\n\n"
#             "Round your answer to 2 dp."
#         )


import random
from .problem_base import Problem
from .utils.options import generate_options


class LinearProgramDual(Problem):
    """
    Generate a convex quadratic problem with equality constraints only and ask for
    the value of the dual function g(lambda) = min_x f(x) + lambda^T (A x - b)

    We choose f(x) = 1/2 x^T Q x with diagonal positive definite Q (no linear term),
    constraints A x = b, and provide a specific lambda.
    For diagonal Q, g(lambda) has closed form:

      g(lambda) = -1/2 * (A^T lambda)^T Q^{-1} (A^T lambda) - b^T lambda

    Dimensions are kept small (2 variables, 2 equality constraints) for simplicity.
    """

    def generate_problem(self):
        # Diagonal positive definite Q
        q1 = random.randint(1, 5)
        q2 = random.randint(1, 5)

        # Equality constraints A x = b, A is 2x2 with small ints
        a11 = random.randint(-3, 3)
        a12 = random.randint(-3, 3)
        a21 = random.randint(-3, 3)
        a22 = random.randint(-3, 3)
        # Ensure A is not all zeros
        if a11 == a12 == a21 == a22 == 0:
            a11 = 1

        b1 = random.randint(-5, 5)
        b2 = random.randint(-5, 5)

        # Provided Lagrange multiplier lambda (2-dim)
        l1 = random.randint(-3, 3)
        l2 = random.randint(-3, 3)

        data = {
            "Q": [q1, q2],  # diagonal entries
            "A": [[a11, a12], [a21, a22]],
            "b": [b1, b2],
            "lam": [l1, l2],
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
        q1, q2 = data["Q"]
        (a11, a12), (a21, a22) = data["A"]
        b1, b2 = data["b"]
        l1, l2 = data["lam"]

        # v = A^T lambda
        v1 = a11 * l1 + a21 * l2
        v2 = a12 * l1 + a22 * l2

        # g(lambda) = -1/2 * v^T Q^{-1} v - b^T lambda
        quad = (v1 * v1) / q1 + (v2 * v2) / q2
        btlam = b1 * l1 + b2 * l2
        g = -0.5 * quad - btlam

        return round(g, 2)

    def get_solution_explanation(self, data, answer):
        q1, q2 = data["Q"]
        (a11, a12), (a21, a22) = data["A"]
        b1, b2 = data["b"]
        l1, l2 = data["lam"]

        md = []
        md.append("# Dual function for equality-constrained quadratic")
        md.append("")
        md.append("The dual function with equality constraints is:")
        md.append(
            r"$$ g(\lambda) = \min_{\mathbf{x}} \left[ f(\mathbf{x}) + \lambda^T(\mathbf{A}\mathbf{x} - \mathbf{b}) \right] $$"
        )
        md.append("")
        md.append("**Step 1: Expand the Lagrangian**")
        md.append("")
        md.append("Substitute $f(\\mathbf{x}) = \\tfrac{1}{2}\\mathbf{x}^T\\mathbf{Q}\\mathbf{x}$ (note: no linear term):")
        md.append("")
        md.append(
            r"$$ L(\mathbf{x}, \lambda) = \tfrac{1}{2}\mathbf{x}^T\mathbf{Q}\mathbf{x} + \lambda^T\mathbf{A}\mathbf{x} - \lambda^T\mathbf{b} $$"
        )
        md.append("")
        md.append("Rewrite $\\lambda^T\\mathbf{A}\\mathbf{x} = (\\mathbf{A}^T\\lambda)^T\\mathbf{x}$:")
        md.append("")
        md.append(
            r"$$ L(\mathbf{x}, \lambda) = \tfrac{1}{2}\mathbf{x}^T\mathbf{Q}\mathbf{x} + (\mathbf{A}^T\lambda)^T\mathbf{x} - \mathbf{b}^T\lambda $$"
        )
        md.append("")
        md.append("**Step 2: Find the minimum by setting gradient to zero**")
        md.append("")
        md.append(
            r"$$ \nabla_{\mathbf{x}} L = \mathbf{Q}\mathbf{x} + \mathbf{A}^T\lambda = 0 $$"
        )
        md.append("")
        md.append(
            r"$$ \mathbf{x}^* = -\mathbf{Q}^{-1}\mathbf{A}^T\lambda $$"
        )
        md.append("")
        md.append(
            "Since $\\mathbf{Q}$ is positive definite, this is indeed a minimum."
        )
        md.append("")
        md.append("**Step 3: Substitute back to get dual function**")
        md.append("")
        md.append("Substituting $\\mathbf{x}^* = -\\mathbf{Q}^{-1}\\mathbf{A}^T\\lambda$ back into $L$:")
        md.append("")
        md.append(
            r"$$ g(\lambda) = \tfrac{1}{2}(-\mathbf{Q}^{-1}\mathbf{A}^T\lambda)^T\mathbf{Q}(-\mathbf{Q}^{-1}\mathbf{A}^T\lambda) + (\mathbf{A}^T\lambda)^T(-\mathbf{Q}^{-1}\mathbf{A}^T\lambda) - \mathbf{b}^T\lambda $$"
        )
        md.append("")
        md.append("Simplifying (using $\\mathbf{Q}^T = \\mathbf{Q}$ and $(\\mathbf{Q}^{-1})^T = \\mathbf{Q}^{-1}$ for diagonal $\\mathbf{Q}$):")
        md.append("")
        md.append(
            r"$$ g(\lambda) = \tfrac{1}{2}(\mathbf{A}^T\lambda)^T\mathbf{Q}^{-1}(\mathbf{A}^T\lambda) - (\mathbf{A}^T\lambda)^T\mathbf{Q}^{-1}(\mathbf{A}^T\lambda) - \mathbf{b}^T\lambda $$"
        )
        md.append("")
        md.append(
            r"$$ g(\lambda) = -\tfrac{1}{2}(\mathbf{A}^T\lambda)^T\mathbf{Q}^{-1}(\mathbf{A}^T\lambda) - \mathbf{b}^T\lambda $$"
        )
        md.append("")
        md.append("Let $\\mathbf{v} = \\mathbf{A}^T\\lambda$ to simplify notation:")
        md.append("")
        md.append(
            r"$$ g(\lambda) = -\tfrac{1}{2}\mathbf{v}^T\mathbf{Q}^{-1}\mathbf{v} - \mathbf{b}^T\lambda $$"
        )
        md.append("")
        md.append("**Step 4: Calculate for the given values**")
        md.append("")
        
        # Calculate A^T lambda
        atl1 = a11 * l1 + a21 * l2
        atl2 = a12 * l1 + a22 * l2
        md.append(
            rf"$$ \mathbf{{v}} = \mathbf{{A}}^T\lambda = \begin{{bmatrix}} {a11} & {a21} \\ {a12} & {a22} \end{{bmatrix}} \begin{{bmatrix}} {l1} \\ {l2} \end{{bmatrix}} = \begin{{bmatrix}} {atl1} \\ {atl2} \end{{bmatrix}} $$"
        )
        md.append("")
        
        # Calculate v^T Q^{-1} v
        v_term = (atl1**2) / q1 + (atl2**2) / q2
        md.append(
            rf"$$ \mathbf{{v}}^T\mathbf{{Q}}^{{-1}}\mathbf{{v}} = {atl1}^2 \cdot \tfrac{{1}}{{{q1}}} + {atl2}^2 \cdot \tfrac{{1}}{{{q2}}} = {atl1**2/q1:.2f} + {atl2**2/q2:.2f} = {v_term:.2f} $$"
        )
        md.append("")
        
        # Calculate b^T lambda
        btlam = b1 * l1 + b2 * l2
        md.append(
            rf"$$ \mathbf{{b}}^T\lambda = {b1} \cdot {l1} + {b2} \cdot {l2} = {btlam} $$"
        )
        md.append("")
        
        md.append("**Final answer:**")
        md.append("")
        md.append(
            rf"$$ g(\lambda) = -\tfrac{{1}}{{2}} \cdot {v_term:.2f} - ({btlam}) = {-0.5*v_term:.2f} - ({btlam}) = {answer:.2f} $$"
        )
        
        return "\n".join(md)

    def _question_markdown(self, data):
        q1, q2 = data["Q"]
        (a11, a12), (a21, a22) = data["A"]
        b1, b2 = data["b"]
        l1, l2 = data["lam"]

        A_tex = rf"\begin{{bmatrix}} {a11} & {a12} \\ {a21} & {a22} \end{{bmatrix}}"
        b_tex = rf"\begin{{bmatrix}} {b1} \\ {b2} \end{{bmatrix}}"
        lam_tex = rf"\begin{{bmatrix}} {l1} \\ {l2} \end{{bmatrix}}"
        Q_tex = rf"\text{{diag}}({q1}, {q2})"

        return (
            "# Dual function value\n\n"
            "Compute the value of the dual function for the following data (no inequality constraints):\n\n"
            rf"$$ f(\mathbf{{x}}) = \tfrac{{1}}{{2}}\mathbf{{x}}^T\mathbf{{Q}}\mathbf{{x}}, \quad \mathbf{{Q}} = {Q_tex} $$"
            "\n\n"
            rf"$$ \mathbf{{A}}x = \mathbf{{b}}, \quad \mathbf{{A}} = {A_tex}, \quad \mathbf{{b}} = {b_tex}, \quad \lambda = {lam_tex} $$"
            "\n\n"
            r"Find: $$ g(\lambda) = \min_{\mathbf{x}} \left[ f(\mathbf{x}) + \lambda^T(\mathbf{A}\mathbf{x} - \mathbf{b}) \right] $$"
            "\n\n"
            "Round your answer to 2 dp."
        )