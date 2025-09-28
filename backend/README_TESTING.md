# Testing Guide

This document describes the testing setup and how to run tests for the backend application.

## Test Structure

The test suite is organized into the following modules:

- `tests/test_problems.py` - Tests for problem generators and solving logic
- `tests/test_schedulers.py` - Tests for scheduler algorithms and edge cases  
- `tests/test_utilities.py` - Tests for utility functions (options, templates, LaTeX)
- `tests/test_api.py` - Tests for API endpoints with database integration
- `tests/test_analytics.py` - Tests for analytics calculations and data integrity
- `tests/conftest.py` - Test configuration and fixtures

## Running Tests

### Basic Test Commands

```bash
# Run all tests
poe test

# Run tests with verbose output
poe test-verbose

# Run tests with coverage report
poe test-coverage
```

### Running Specific Test Modules

```bash
# Test only problem generators
pytest tests/test_problems.py -v

# Test only schedulers
pytest tests/test_schedulers.py -v

# Test only API endpoints
pytest tests/test_api.py -v
```

### Running Specific Tests

```bash
# Test a specific class
pytest tests/test_problems.py::TestArithmeticIntensity -v

# Test a specific method
pytest tests/test_problems.py::TestArithmeticIntensity::test_solve_method -v
```

## Test Categories

### Unit Tests
- **Problem Generators**: Test individual problem types, solving logic, and edge cases
- **Schedulers**: Test scheduling algorithms, ease factor calculations, and interval logic
- **Utilities**: Test option generation, template rendering, and LaTeX formatting

### Integration Tests
- **API Endpoints**: Test full request/response cycles with database integration
- **Database Operations**: Test CRUD operations, relationships, and data integrity
- **Analytics**: Test complex calculations and data aggregation

### Key Test Areas

#### Problem Generation Tests
- Verify correct problem structure (question, options, correct index)
- Test solving logic with known inputs and edge cases
- Ensure integer answers generate integer-only options
- Test randomization of multiple choice options

#### Scheduler Tests
- Test interval calculations for different review patterns
- Verify ease factor adjustments based on performance
- Test edge cases (no reviews, all correct/incorrect)
- Ensure proper date calculations and timezone handling

#### API Tests
- Test all CRUD operations for problems and reviews
- Verify proper error handling and status codes
- Test database integration and data persistence
- Test analytics endpoint with various data scenarios

#### Analytics Tests
- Test accuracy calculations and statistical aggregations
- Verify due date classifications (overdue, today, this week, etc.)
- Test ease factor and interval calculations
- Ensure data consistency and integrity

## Test Database

Tests use a separate SQLite database (`test.db`) to avoid interfering with development data. The test database is created and destroyed for each test session.

## Fixtures

Common test fixtures are defined in `conftest.py`:

- `client`: FastAPI test client
- `db_session`: Database session for tests
- `sample_problem_data`: Sample problem creation data
- `sample_review_data`: Sample review creation data

## Coverage

The test suite aims for comprehensive coverage of:

- All problem generator classes and methods
- All scheduler algorithms and edge cases
- All API endpoints and error conditions
- All utility functions
- Analytics calculations and data integrity

## Continuous Integration

Tests should be run:
- Before committing code changes
- In CI/CD pipelines
- When adding new features
- When fixing bugs

## Debugging Tests

To debug failing tests:

```bash
# Run with detailed output
pytest tests/test_problems.py::TestArithmeticIntensity::test_solve_method -v -s

# Run with pdb debugger
pytest tests/test_problems.py::TestArithmeticIntensity::test_solve_method --pdb

# Run with logging
pytest tests/test_problems.py -v --log-cli-level=DEBUG
```

## Adding New Tests

When adding new features:

1. Add unit tests for new classes/methods
2. Add integration tests for new API endpoints
3. Update existing tests if interfaces change
4. Ensure test coverage for edge cases
5. Add performance tests for critical paths

## Test Data

Tests use minimal, focused test data to:
- Keep tests fast and reliable
- Make test failures easy to diagnose
- Avoid dependencies on external data
- Ensure tests are deterministic
