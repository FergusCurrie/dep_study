import random


def generate_options(correct_answer, num_options=4, variation_range=None):
    """
    Generate randomized multiple choice options with the correct answer.
    
    Args:
        correct_answer: The correct answer (can be int, float, or string)
        num_options: Number of total options (default 4)
        variation_range: Range for generating wrong answers. If None, uses smart defaults.
    
    Returns:
        tuple: (options_list, correct_index)
    """
    # Convert to float for calculations if it's numeric
    try:
        numeric_answer = float(correct_answer)
        is_numeric = True
        # Check if the original answer was an integer
        is_integer = isinstance(correct_answer, int) or (isinstance(correct_answer, str) and correct_answer.isdigit()) or (numeric_answer == int(numeric_answer))
    except (ValueError, TypeError):
        is_numeric = False
        is_integer = False
        numeric_answer = None
    
    options = [str(correct_answer)]
    
    if is_numeric:
        # Smart variation based on the magnitude of the answer
        if variation_range is None:
            if numeric_answer == 0:
                variation_range = 5
            elif abs(numeric_answer) < 10:
                variation_range = max(2, abs(numeric_answer) * 0.5)
            elif abs(numeric_answer) < 100:
                variation_range = max(5, abs(numeric_answer) * 0.3)
            else:
                variation_range = max(10, abs(numeric_answer) * 0.2)
        
        # Generate wrong answers with various strategies
        wrong_answers = []
        
        # Strategy 1: Add/subtract variations
        for _ in range(num_options - 1):
            if is_integer:
                # For integer answers, use integer variations
                variation = random.randint(-int(variation_range), int(variation_range))
                wrong_answer = int(numeric_answer) + variation
            else:
                # For float answers, use float variations
                variation = random.uniform(-variation_range, variation_range)
                wrong_answer = numeric_answer + variation
                
                # Round to reasonable precision
                if abs(wrong_answer) < 1:
                    wrong_answer = round(wrong_answer, 2)
                elif abs(wrong_answer) < 10:
                    wrong_answer = round(wrong_answer, 1)
                else:
                    wrong_answer = round(wrong_answer)
            
            wrong_answers.append(str(wrong_answer))
        
        options.extend(wrong_answers)
    else:
        # For non-numeric answers, generate simple variations
        for _ in range(num_options - 1):
            if isinstance(correct_answer, str):
                # Simple string variations
                if correct_answer.isdigit():
                    base_num = int(correct_answer)
                    variation = random.randint(-5, 5)
                    wrong_answer = str(base_num + variation)
                else:
                    # For non-numeric strings, just add a suffix
                    wrong_answer = correct_answer + str(random.randint(1, 9))
            else:
                wrong_answer = str(correct_answer) + str(random.randint(1, 9))
            
            options.append(wrong_answer)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_options = []
    for option in options:
        if option not in seen:
            seen.add(option)
            unique_options.append(option)
    
    # If we don't have enough unique options, generate more
    while len(unique_options) < num_options:
        if is_numeric:
            if is_integer:
                # For integer answers, use integer variations
                variation = random.randint(-int(variation_range * 2), int(variation_range * 2))
                wrong_answer = int(numeric_answer) + variation
            else:
                # For float answers, use float variations
                variation = random.uniform(-variation_range * 2, variation_range * 2)
                wrong_answer = numeric_answer + variation
                if abs(wrong_answer) < 1:
                    wrong_answer = round(wrong_answer, 2)
                elif abs(wrong_answer) < 10:
                    wrong_answer = round(wrong_answer, 1)
                else:
                    wrong_answer = round(wrong_answer)
            option = str(wrong_answer)
        else:
            option = str(correct_answer) + str(random.randint(10, 99))
        
        if option not in seen:
            seen.add(option)
            unique_options.append(option)
    
    # Take only the number of options we need
    unique_options = unique_options[:num_options]
    
    # Shuffle the options
    random.shuffle(unique_options)
    
    # Find the correct index
    correct_index = unique_options.index(str(correct_answer))
    
    return unique_options, correct_index
