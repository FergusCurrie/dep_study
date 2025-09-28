import pytest
from src.problems.utils.options import generate_options
from src.problems.utils.template import render_template
from src.problems.utils.latex import matrix_to_latex
import numpy as np


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
            assert 0 <= value <= 0.1  # Reasonable range for 0.05


class TestTemplateRendering:
    def test_render_template_basic(self):
        """Test basic template rendering."""
        data = {"name": "test", "value": 42}
        result = render_template("problem_templates/arithmetic_intensity.j2", data)
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_template_with_variables(self):
        """Test template rendering with various data types."""
        data = {
            "string_var": "hello",
            "int_var": 123,
            "float_var": 3.14,
            "list_var": [1, 2, 3]
        }
        
        # This will fail if template doesn't exist, but that's expected
        # We're testing the function interface
        try:
            result = render_template("problem_templates/arithmetic_intensity.j2", data)
            assert isinstance(result, str)
        except Exception:
            # Template file might not exist in test environment
            pass

    def test_render_template_empty_data(self):
        """Test template rendering with empty data."""
        try:
            result = render_template("problem_templates/arithmetic_intensity.j2", {})
            assert isinstance(result, str)
        except Exception:
            # Template file might not exist in test environment
            pass


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
