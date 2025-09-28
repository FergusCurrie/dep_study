

import numpy as np
import random
from .problem_base import Problem
from .utils.latex import matrix_to_latex
from .utils.options import generate_options
from .utils.template import render_template


class RecSysMatrixFact(Problem):
    def generate_problem(self):
        """Generate a problem asking to predict a missing rating using matrix factorization"""
        # Create simple 2D feature vectors for hand calculation
        num_users = random.choice([2, 3])
        num_items = random.choice([2, 3])
        num_features = 2  # Keep it simple for hand calculation
        
        # Generate simple integer feature vectors
        user_features = []
        for i in range(num_users):
            features = [random.randint(1, 3) for _ in range(num_features)]
            user_features.append(features)
        user_features = np.array(user_features).T
        
        item_features = []
        for i in range(num_items):
            features = [random.randint(1, 3) for _ in range(num_features)]
            item_features.append(features)
        item_features = np.array(item_features).T
        
        
        # Choose which rating to predict
        target_user = random.randint(0, num_users - 1)
        target_item = random.randint(0, num_items - 1)
        
        # Calculate the correct answer
        answer = self.solve(user_features, item_features, target_user, target_item)
        
        data = {
            'user_features': matrix_to_latex(user_features),
            'item_features': matrix_to_latex(item_features),
            'target_user': target_user + 1,  # 1-indexed for display
            'target_item': target_item + 1,
            'num_features': num_features
        }
        markdown_question = render_template('problem_templates/rec_sys_matrix_fact.j2', data)
        
        options, correct_index = generate_options(answer, variation_range=3)
        
        return {
            'question': markdown_question,
            'options': options,
            'correct': correct_index
        }

    def solve(self, user_features, item_features, user_idx, item_idx):
        """Solve for missing rating using dot product of user and item feature vectors"""
        return np.dot(user_features[:, user_idx], item_features[:, item_idx])

if __name__ == "__main__":
    prob = RecSysMatrixFact().generate_problem()
    print(prob)