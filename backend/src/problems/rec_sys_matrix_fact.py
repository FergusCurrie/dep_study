

import numpy as np
import random
from .problem_base import Problem
from .utils.latex import matrix_to_latex
from .utils.options import generate_options


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
        
        problem_data = {
            'user_features': matrix_to_latex(user_features),
            'item_features': matrix_to_latex(item_features),
            'target_user': target_user + 1,  # 1-indexed for display
            'target_item': target_item + 1,
            'num_features': num_features,
            'user_features_array': user_features,
            'item_features_array': item_features,
            'target_user_idx': target_user,
            'target_item_idx': target_item
        }
        
        # Generate question using template text with string interpolation
        markdown_question = f"""

# Matrix Factorization: Predicting Missing Rating


In a collaborative filtering system, we represent users and items using feature vectors that capture latent preferences.

**User Feature Matrix P:**
$$
{problem_data['user_features']}
$$

**Item Feature Matrix Q:**
$$
{problem_data['item_features']}
$$


**What rating would User {target_user + 1} give to Item {target_item + 1}?**
"""
        solution_explanation = self.get_solution_explanation(problem_data, answer)
        
        options, correct_index = generate_options(answer, variation_range=3)
        
        return {
            'question': markdown_question,
            'options': options,
            'correct': correct_index,
            'solution_explanation': solution_explanation
        }

    def solve(self, user_features, item_features, user_idx, item_idx):
        """Solve for missing rating using dot product of user and item feature vectors"""
        return np.dot(user_features[:, user_idx], item_features[:, item_idx])
    
    def get_solution_explanation(self, problem_data, answer):
        user_features = problem_data['user_features_array']
        item_features = problem_data['item_features_array']
        target_user_idx = problem_data['target_user_idx']
        target_item_idx = problem_data['target_item_idx']
        target_user_display = problem_data['target_user']
        target_item_display = problem_data['target_item']
        
        user_vector = user_features[:, target_user_idx]
        item_vector = item_features[:, target_item_idx]
        
        explanation = f"""## Solution Explanation

**Given:**
- User {target_user_display} feature vector: [{user_vector[0]}, {user_vector[1]}]
- Item {target_item_display} feature vector: [{item_vector[0]}, {item_vector[1]}]

**Step 1: Calculate dot product**
The predicted rating is the dot product of the user and item feature vectors:

Rating = (User₁ × Item₁) + (User₂ × Item₂)
Rating = ({user_vector[0]} × {item_vector[0]}) + ({user_vector[1]} × {item_vector[1]})
Rating = {user_vector[0] * item_vector[0]} + {user_vector[1] * item_vector[1]}
Rating = {answer}

**Answer:** {answer}

**Note:** Matrix factorization predicts ratings by finding latent features that capture user preferences and item characteristics. The dot product measures how well the user's preferences align with the item's features."""
        
        return explanation

if __name__ == "__main__":
    prob = RecSysMatrixFact().generate_problem()
    print(prob)