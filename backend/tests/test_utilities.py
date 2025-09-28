import numpy as np
from src.problems.utils.latex import matrix_to_latex
from src.problems.utils.options import generate_options


class TestOptionsGeneration:
    def test_generate_options_integer_answer(self):
        """Test options generation for integer answers."""
        options, correct_index = generate_options(42)
        
        assert len(options) == 4
        assert 0 <= correct_index < 4
        assert "42" in options
        assert options[correct_index] == "42"
        
        # All options should be integers
        for option in options:
            assert option.isdigit() or (option.startswith('-') and option[1:].isdigit())

    def test_generate_options_float_answer(self):
        """Test options generation for float answers."""
        options, correct_index = generate_options(3.14)
        
        assert len(options) == 4
        assert 0 <= correct_index < 4
        assert "3.14" in options
        assert options[correct_index] == "3.14"

    def test_generate_options_string_answer(self):
        """Test options generation for string answers."""
        options, correct_index = generate_options("hello")
        
        assert len(options) == 4
        assert 0 <= correct_index < 4
        assert "hello" in options
        assert options[correct_index] == "hello"

    def test_generate_options_custom_num_options(self):
        """Test options generation with custom number of options."""
        options, correct_index = generate_options(10, num_options=6)
        
        assert len(options) == 6
        assert 0 <= correct_index < 6
        assert "10" in options

    def test_generate_options_custom_variation_range(self):
        """Test options generation with custom variation range."""
        options, correct_index = generate_options(100, variation_range=10)
        
        assert len(options) == 4
        assert "100" in options
        
        # All options should be within reasonable range
        for option in options:
            value = float(option)
            assert 90 <= value <= 110  # 100 ± 10

    def test_generate_options_zero_answer(self):
        """Test options generation with zero answer."""
        options, correct_index = generate_options(0)
        
        assert len(options) == 4
        assert "0" in options
        assert options[correct_index] == "0"

    def test_generate_options_negative_answer(self):
        """Test options generation with negative answer."""
        options, correct_index = generate_options(-5)
        
        assert len(options) == 4
        assert "-5" in options
        assert options[correct_index] == "-5"

    def test_generate_options_randomization(self):
        """Test that options are randomized (correct answer not always first)."""
        correct_positions = []
        
        for _ in range(10):
            options, correct_index = generate_options(50)
            correct_positions.append(correct_index)
        
        # Should have some variation in positions
        assert len(set(correct_positions)) > 1

    def test_generate_options_unique_values(self):
        """Test that all options are unique."""
        options, correct_index = generate_options(25)
        
        assert len(options) == len(set(options))  # All unique

    def test_generate_options_small_float(self):
        """Test options generation with small float values."""
        options, correct_index = generate_options(0.05)
        
        assert len(options) == 4
        assert "0.05" in options
        
        # Should maintain appropriate precision
        for option in options:
            value = float(option)
            assert -2.0 <= value <= 2.0  # Reasonable range for 0.05 with variation


class TestStringTemplating:
    def test_string_templating_basic(self):
        """Test basic string templating functionality."""
        name = "test"
        value = 42
        result = f"Hello {name}, value is {value}"
        
        assert isinstance(result, str)
        assert "test" in result
        assert "42" in result

    def test_string_templating_with_multiline(self):
        """Test multiline string templating."""
        flop_per_thread = 10
        memory_access_size_bits = 32
        memory_access_per_thread = 5
        
        result = f"""## Arithmetic Intensity Problem

Calculate the arithmetic intensity for a thread that performs **{flop_per_thread}** floating-point operations while accessing **{memory_access_size_bits}** bits of memory **{memory_access_per_thread}** times.

**Formula:** Arithmetic Intensity = FLOPs per thread / (Memory access size in bytes × Memory accesses per thread)

**Note:** 1 byte = 8 bits

What is the arithmetic intensity? (Round to 2 decimal places)"""
        
        assert isinstance(result, str)
        assert "10" in result
        assert "32" in result
        assert "5" in result
        assert "Arithmetic Intensity Problem" in result

    def test_string_templating_with_formatting(self):
        """Test string templating with different formatting options."""
        answer = 3.14159
        result = f"Answer: {answer:.2f}"
        
        assert result == "Answer: 3.14"


class TestLatexUtils:
    def test_matrix_to_latex_2x2(self):
        """Test LaTeX conversion for 2x2 matrix."""
        matrix = np.array([[1, 2], [3, 4]])
        result = matrix_to_latex(matrix)
        
        assert isinstance(result, str)
        assert "\\begin{bmatrix}" in result
        assert "\\end{bmatrix}" in result
        assert "1 & 2" in result
        assert "3 & 4" in result
        assert "\\\\" in result  # Line break

    def test_matrix_to_latex_1x3(self):
        """Test LaTeX conversion for 1x3 matrix."""
        matrix = np.array([[1, 2, 3]])
        result = matrix_to_latex(matrix)
        
        assert isinstance(result, str)
        assert "\\begin{bmatrix}" in result
        assert "\\end{bmatrix}" in result
        assert "1 & 2 & 3" in result
        assert "\\\\" not in result  # No line breaks for single row

    def test_matrix_to_latex_3x1(self):
        """Test LaTeX conversion for 3x1 matrix."""
        matrix = np.array([[1], [2], [3]])
        result = matrix_to_latex(matrix)
        
        assert isinstance(result, str)
        assert "\\begin{bmatrix}" in result
        assert "\\end{bmatrix}" in result
        assert "1" in result
        assert "2" in result
        assert "3" in result
        assert result.count("\\\\") == 2  # Two line breaks

    def test_matrix_to_latex_float_values(self):
        """Test LaTeX conversion with float values."""
        matrix = np.array([[1.5, 2.7], [3.14, 4.0]])
        result = matrix_to_latex(matrix)
        
        assert isinstance(result, str)
        assert "1.5" in result
        assert "2.7" in result
        assert "3.14" in result
        assert "4.0" in result

    def test_matrix_to_latex_negative_values(self):
        """Test LaTeX conversion with negative values."""
        matrix = np.array([[-1, 2], [3, -4]])
        result = matrix_to_latex(matrix)
        
        assert isinstance(result, str)
        assert "-1" in result
        assert "-4" in result

    def test_matrix_to_latex_zero_values(self):
        """Test LaTeX conversion with zero values."""
        matrix = np.array([[0, 1], [2, 0]])
        result = matrix_to_latex(matrix)
        
        assert isinstance(result, str)
        assert "0" in result
        assert "1" in result
        assert "2" in result
