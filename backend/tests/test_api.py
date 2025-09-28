import pytest
from fastapi.testclient import TestClient
from database import Problem, Review, Due
from datetime import datetime, timedelta


class TestProblemEndpoints:
    def test_create_problem(self, client: TestClient):
        """Test creating a new problem."""
        response = client.post("/api/problems/", json={"name": "test_problem"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "test_problem"
        assert "id" in data
        assert "created_date" in data

    def test_create_problem_invalid_data(self, client: TestClient):
        """Test creating problem with invalid data."""
        response = client.post("/api/problems/", json={})
        
        assert response.status_code == 422  # Validation error

    def test_read_problems_empty(self, client: TestClient):
        """Test reading problems when none exist."""
        response = client.get("/api/problems/")
        
        assert response.status_code == 200
        data = response.json()
        assert data == {}  # Empty response when no problems

    def test_read_problems_with_data(self, client: TestClient, db_session):
        """Test reading problems when data exists."""
        # Create a problem and due date
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        due = Due(problem_id=problem.id, due_date=datetime.now() - timedelta(days=1))
        db_session.add(due)
        db_session.commit()
        
        response = client.get("/api/problems/")
        
        assert response.status_code == 200
        data = response.json()
        assert "question" in data
        assert "options" in data
        assert "correct" in data
        assert "id" in data

    def test_read_problem_by_id(self, client: TestClient, db_session):
        """Test reading a specific problem by ID."""
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        response = client.get(f"/api/problems/{problem.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "test_problem"
        assert data["id"] == problem.id

    def test_read_problem_not_found(self, client: TestClient):
        """Test reading a non-existent problem."""
        response = client.get("/api/problems/999")
        
        assert response.status_code == 404

    def test_delete_problem(self, client: TestClient, db_session):
        """Test deleting a problem."""
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        response = client.delete(f"/api/problems/{problem.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Problem deleted"
        
        # Verify problem is deleted
        deleted_problem = db_session.query(Problem).filter(Problem.id == problem.id).first()
        assert deleted_problem is None

    def test_delete_problem_not_found(self, client: TestClient):
        """Test deleting a non-existent problem."""
        response = client.delete("/api/problems/999")
        
        assert response.status_code == 404


class TestReviewEndpoints:
    def test_create_review(self, client: TestClient, db_session):
        """Test creating a new review."""
        # First create a problem
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        response = client.post("/api/reviews/", json={
            "problem_id": problem.id,
            "correct": True
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["problem_id"] == problem.id
        assert data["correct"] is True
        assert "id" in data
        assert "created_date" in data

    def test_create_review_problem_not_found(self, client: TestClient):
        """Test creating review for non-existent problem."""
        response = client.post("/api/reviews/", json={
            "problem_id": 999,
            "correct": True
        })
        
        assert response.status_code == 404

    def test_create_review_invalid_data(self, client: TestClient):
        """Test creating review with invalid data."""
        response = client.post("/api/reviews/", json={
            "problem_id": "invalid",
            "correct": "invalid"
        })
        
        assert response.status_code == 422  # Validation error

    def test_read_reviews(self, client: TestClient, db_session):
        """Test reading all reviews."""
        # Create a problem and review
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        review = Review(problem_id=problem.id, correct=True)
        db_session.add(review)
        db_session.commit()
        
        response = client.get("/api/reviews/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["problem_id"] == problem.id

    def test_read_reviews_with_pagination(self, client: TestClient, db_session):
        """Test reading reviews with pagination."""
        # Create multiple reviews
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        for i in range(5):
            review = Review(problem_id=problem.id, correct=True)
            db_session.add(review)
        db_session.commit()
        
        response = client.get("/api/reviews/?skip=2&limit=2")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 2

    def test_read_problem_reviews(self, client: TestClient, db_session):
        """Test reading reviews for a specific problem."""
        # Create a problem and reviews
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        for i in range(3):
            review = Review(problem_id=problem.id, correct=True)
            db_session.add(review)
        db_session.commit()
        
        response = client.get(f"/api/reviews/problem/{problem.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        for review in data:
            assert review["problem_id"] == problem.id

    def test_delete_review(self, client: TestClient, db_session):
        """Test deleting a review."""
        # Create a problem and review
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        review = Review(problem_id=problem.id, correct=True)
        db_session.add(review)
        db_session.commit()
        db_session.refresh(review)
        
        response = client.delete(f"/api/reviews/{review.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Review deleted"
        
        # Verify review is deleted
        deleted_review = db_session.query(Review).filter(Review.id == review.id).first()
        assert deleted_review is None

    def test_delete_review_not_found(self, client: TestClient):
        """Test deleting a non-existent review."""
        response = client.delete("/api/reviews/999")
        
        assert response.status_code == 404


class TestAnalyticsEndpoint:
    def test_analytics_empty_database(self, client: TestClient):
        """Test analytics endpoint with empty database."""
        response = client.get("/api/analytics/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "summary" in data
        assert "problems" in data
        assert "generated_at" in data
        
        summary = data["summary"]
        assert summary["total_problems"] == 0
        assert summary["total_reviews"] == 0
        assert summary["overall_accuracy"] == 0
        assert summary["problems_due_today"] == 0

    def test_analytics_with_data(self, client: TestClient, db_session):
        """Test analytics endpoint with sample data."""
        # Create problems and reviews
        problem1 = Problem(name="arithmetic_intensity")
        problem2 = Problem(name="bytes2bits")
        db_session.add_all([problem1, problem2])
        db_session.commit()
        db_session.refresh(problem1)
        db_session.refresh(problem2)
        
        # Create reviews
        reviews = [
            Review(problem_id=problem1.id, correct=True),
            Review(problem_id=problem1.id, correct=False),
            Review(problem_id=problem2.id, correct=True),
        ]
        db_session.add_all(reviews)
        db_session.commit()
        
        # Create due dates
        due1 = Due(problem_id=problem1.id, due_date=datetime.now() - timedelta(days=1))
        due2 = Due(problem_id=problem2.id, due_date=datetime.now() + timedelta(days=1))
        db_session.add_all([due1, due2])
        db_session.commit()
        
        response = client.get("/api/analytics/")
        
        assert response.status_code == 200
        data = response.json()
        
        summary = data["summary"]
        assert summary["total_problems"] == 2
        assert summary["total_reviews"] == 3
        assert summary["overall_accuracy"] == 66.7  # 2/3 correct
        assert summary["problems_overdue"] == 1
        assert summary["problems_due_this_week"] == 1
        
        problems = data["problems"]
        assert len(problems) == 2
        
        # Check problem analytics structure
        for problem in problems:
            assert "problem_id" in problem
            assert "problem_name" in problem
            assert "total_reviews" in problem
            assert "correct_reviews" in problem
            assert "ease_factor" in problem
            assert "current_interval" in problem
            assert "next_review_date" in problem
            assert "due_date" in problem
            assert "days_until_due" in problem


class TestStaticFileServing:
    def test_serve_react_app_root(self, client: TestClient):
        """Test serving React app for root path."""
        response = client.get("/")
        
        # Should return 404 if no static files exist
        assert response.status_code == 404

    def test_serve_react_app_unknown_path(self, client: TestClient):
        """Test serving React app for unknown path."""
        response = client.get("/unknown/path")
        
        # Should return 404 if no static files exist
        assert response.status_code == 404

    def test_api_routes_not_served_as_static(self, client: TestClient):
        """Test that API routes are not served as static files."""
        response = client.get("/api/unknown")
        
        # Should return 404 for unknown API routes
        assert response.status_code == 404
        assert "API endpoint not found" in response.json()["detail"]
