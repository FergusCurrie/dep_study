import pytest
from src.problems.arithmetic_intensity import ArithmeticIntensity
from src.problems.bytes2bits import Bytes2Bits
from src.problems.dispatch import dispatch_problem
from src.problems.ram_bandwidth import RamBandwidth
from src.problems.rec_sys_matrix_fact import RecSysMatrixFact
from src.problems.roofline import Roofline


class TestArithmeticIntensity:
    def test_generate_problem_structure(self):
        """Test that problem generation returns correct structure."""
        problem = ArithmeticIntensity()
        result = problem.generate_problem()
        
        assert "question" in result
        assert "options" in result
        assert "correct" in result
        assert isinstance(result["options"], list)
        assert len(result["options"]) == 4
        assert isinstance(result["correct"], int)
        assert 0 <= result["correct"] < 4

    def test_solve_method(self):
        """Test the solve method with known inputs."""
        problem = ArithmeticIntensity()
        result = problem.solve(10, 32, 5)  # 10 flops, 32 bits, 5 accesses
        
        # 10 flops / (32/8 * 5) bytes = 10 / 20 = 0.5
        assert result == 0.5

    def test_solve_edge_cases(self):
        """Test solve method with edge cases."""
        problem = ArithmeticIntensity()
        
        # Test with zero memory access
        result = problem.solve(10, 32, 0)
        assert result == float('inf') or result > 1000  # Should be very large
        
        # Test with small values
        result = problem.solve(1, 8, 1)
        assert result == 1.0  # 1 / (8/8 * 1) = 1


class TestBytes2Bits:
    def test_generate_problem_structure(self):
        """Test that problem generation returns correct structure."""
        problem = Bytes2Bits()
        result = problem.generate_problem()
        
        assert "question" in result
        assert "options" in result
        assert "correct" in result
        assert len(result["options"]) == 4

    def test_solve_method(self):
        """Test the solve method with known inputs."""
        problem = Bytes2Bits()
        
        assert problem.solve(1) == 8
        assert problem.solve(5) == 40
        assert problem.solve(0) == 0

    def test_integer_options(self):
        """Test that all options are integers for integer answers."""
        problem = Bytes2Bits()
        result = problem.generate_problem()
        
        # Find the correct answer
        correct_answer = result["options"][result["correct"]]
        
        # All options should be integers
        for option in result["options"]:
            assert option.isdigit() or (option.startswith('-') and option[1:].isdigit())


class TestRamBandwidth:
    def test_generate_problem_structure(self):
        """Test that problem generation returns correct structure."""
        problem = RamBandwidth()
        result = problem.generate_problem()
        
        assert "question" in result
        assert "options" in result
        assert "correct" in result

    def test_solve_method(self):
        """Test the solve method with known inputs."""
        problem = RamBandwidth()
        
        # 64 bits, 1 GHz, 2 data rate = (64/8) * 1 * 2 = 16 GB/s
        result = problem.solve(64, 1, 2)
        assert result == 16.0


class TestRecSysMatrixFact:
    def test_generate_problem_structure(self):
        """Test that problem generation returns correct structure."""
        problem = RecSysMatrixFact()
        result = problem.generate_problem()
        
        assert "question" in result
        assert "options" in result
        assert "correct" in result

    def test_solve_method(self):
        """Test the solve method with known inputs."""
        import numpy as np
        problem = RecSysMatrixFact()
        
        # Simple 2x2 matrices
        user_features = np.array([[1, 2], [3, 4]])
        item_features = np.array([[5, 6], [7, 8]])
        
        # Dot product of [1, 3] and [5, 7] = 1*5 + 3*7 = 5 + 21 = 26
        result = problem.solve(user_features, item_features, 0, 0)
        assert result == 26


class TestRoofline:
    def test_generate_problem_structure(self):
        """Test that problem generation returns correct structure."""
        problem = Roofline()
        result = problem.generate_problem()
        
        assert "question" in result
        assert "options" in result
        assert "correct" in result

    def test_solve_method(self):
        """Test the solve method with known inputs."""
        problem = Roofline()
        
        # Test memory-bound case
        result = problem.solve(5, 32, 10, 100, 500)  # Low AI, high peak flops
        assert result == 1  # Memory bound
        
        # Test compute-bound case  
        result = problem.solve(100, 8, 1, 100, 50)  # High AI, low peak flops
        assert result == 0  # Compute bound


class TestProblemDispatch:
    def test_dispatch_all_problem_types(self):
        """Test that all problem types can be dispatched."""
        problem_types = [
            "arithmetic_intensity",
            "bytes2bits", 
            "ram_bandwidth",
            "rec_sys_matrix_fact",
            "roofline"
        ]
        
        for problem_type in problem_types:
            result = dispatch_problem(problem_type)
            assert "question" in result
            assert "options" in result
            assert "correct" in result

    def test_dispatch_invalid_problem_type(self):
        """Test that invalid problem types raise appropriate errors."""
        with pytest.raises(ValueError):
            dispatch_problem("invalid_problem_type")
