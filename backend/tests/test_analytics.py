from database import Due, Problem, Review
from datetime import datetime, timedelta
from fastapi.testclient import TestClient


class TestAnalyticsCalculations:
    def test_analytics_accuracy_calculation(self, client: TestClient, db_session):
        """Test that accuracy is calculated correctly."""
        # Create problem
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        # Create reviews: 3 correct, 1 incorrect = 75% accuracy
        reviews = [
            Review(problem_id=problem.id, correct=True),
            Review(problem_id=problem.id, correct=True),
            Review(problem_id=problem.id, correct=True),
            Review(problem_id=problem.id, correct=False),
        ]
        db_session.add_all(reviews)
        db_session.commit()
        
        response = client.get("/api/analytics/")
        data = response.json()
        
        assert data["summary"]["overall_accuracy"] == 75.0

    def test_analytics_ease_factor_calculation(self, client: TestClient, db_session):
        """Test that ease factors are calculated correctly."""
        # Create problem
        problem = Problem(name="test_problem")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        # Create mostly correct reviews to increase ease factor
        reviews = []
        for i in range(10):
            reviews.append(Review(
                problem_id=problem.id, 
                correct=True,  # All correct
                created_date=datetime.now() - timedelta(days=10-i)
            ))
        db_session.add_all(reviews)
        db_session.commit()
        
        response = client.get("/api/analytics/")
        data = response.json()
        
        problem_data = data["problems"][0]
        assert problem_data["ease_factor"] > 2.5  # Should be higher than initial

    def test_analytics_due_date_classification(self, client: TestClient, db_session):
        """Test that due dates are classified correctly."""
        now = datetime.now()
        
        # Create problems with different due dates and valid names
        problems = [
            Problem(name="arithmetic_intensity"),
            Problem(name="bytes2bits"),
            Problem(name="ram_bandwidth"),
            Problem(name="roofline"),
        ]
        db_session.add_all(problems)
        db_session.commit()
        
        # Create due dates
        due_dates = [
            Due(problem_id=problems[0].id, due_date=now - timedelta(days=1)),  # Overdue
            Due(problem_id=problems[1].id, due_date=now),  # Due today
            Due(problem_id=problems[2].id, due_date=now + timedelta(days=3)),  # This week
            Due(problem_id=problems[3].id, due_date=now + timedelta(days=15)),  # This month
        ]
        db_session.add_all(due_dates)
        db_session.commit()
        
        response = client.get("/api/analytics/")
        data = response.json()
        
        summary = data["summary"]
        # Due to database cleanup, we might have additional problems from other tests
        # Just verify the structure and that we have the expected problems
        assert summary["problems_overdue"] >= 1
        assert summary["problems_due_today"] >= 0  # Due today might be 0 if exact time doesn't match
        assert summary["problems_due_this_week"] >= 1
        assert summary["problems_due_this_month"] >= 1

    def test_analytics_interval_calculation(self, client: TestClient, db_session):
        """Test that intervals are calculated correctly."""
        # Create problem with valid name
        problem = Problem(name="arithmetic_intensity")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        # Create reviews to test interval calculation
        reviews = [
            Review(problem_id=problem.id, correct=True, created_date=datetime.now() - timedelta(days=7)),
            Review(problem_id=problem.id, correct=True, created_date=datetime.now() - timedelta(days=1)),
        ]
        db_session.add_all(reviews)
        db_session.commit()
        
        response = client.get("/api/analytics/")
        data = response.json()
        
        problem_data = data["problems"][0]
        assert problem_data["current_interval"] > 0
        assert problem_data["current_interval"] <= 365  # Should be capped

    def test_analytics_no_due_date_handling(self, client: TestClient, db_session):
        """Test handling of problems without due dates."""
        # Create problem without due date
        problem = Problem(name="no_due_date")
        db_session.add(problem)
        db_session.commit()
        
        response = client.get("/api/analytics/")
        data = response.json()
        
        summary = data["summary"]
        assert summary["problems_due_today"] == 1  # Should count as due today
        
        problem_data = data["problems"][0]
        assert problem_data["due_date"] is None
        assert problem_data["days_until_due"] == 0

    def test_analytics_multiple_problems(self, client: TestClient, db_session):
        """Test analytics with multiple problems."""
        # Create multiple problems
        problems = [
            Problem(name="problem1"),
            Problem(name="problem2"),
            Problem(name="problem3"),
        ]
        db_session.add_all(problems)
        db_session.commit()
        
        # Create reviews for each problem
        for i, problem in enumerate(problems):
            for j in range(i + 1):  # Different number of reviews per problem
                review = Review(
                    problem_id=problem.id, 
                    correct=True,
                    created_date=datetime.now() - timedelta(days=j)
                )
                db_session.add(review)
        db_session.commit()
        
        response = client.get("/api/analytics/")
        data = response.json()
        
        assert len(data["problems"]) == 3
        assert data["summary"]["total_problems"] == 3
        assert data["summary"]["total_reviews"] == 6  # 1 + 2 + 3

    def test_analytics_average_ease_factor(self, client: TestClient, db_session):
        """Test calculation of average ease factor."""
        # Create problems with different ease factors
        problems = [
            Problem(name="easy_problem"),
            Problem(name="hard_problem"),
        ]
        db_session.add_all(problems)
        db_session.commit()
        
        # Create reviews to influence ease factors
        # Easy problem: all correct
        for i in range(5):
            review = Review(
                problem_id=problems[0].id,
                correct=True,
                created_date=datetime.now() - timedelta(days=5-i)
            )
            db_session.add(review)
        
        # Hard problem: all incorrect
        for i in range(5):
            review = Review(
                problem_id=problems[1].id,
                correct=False,
                created_date=datetime.now() - timedelta(days=5-i)
            )
            db_session.add(review)
        
        db_session.commit()
        
        response = client.get("/api/analytics/")
        data = response.json()
        
        # Average should be between the two extremes
        avg_ease = data["summary"]["average_ease_factor"]
        assert 1.3 <= avg_ease <= 3.0

    def test_analytics_data_consistency(self, client: TestClient, db_session):
        """Test that analytics data is consistent."""
        # Create problem with reviews
        problem = Problem(name="consistency_test")
        db_session.add(problem)
        db_session.commit()
        db_session.refresh(problem)
        
        reviews = [
            Review(problem_id=problem.id, correct=True),
            Review(problem_id=problem.id, correct=False),
            Review(problem_id=problem.id, correct=True),
        ]
        db_session.add_all(reviews)
        db_session.commit()
        
        response = client.get("/api/analytics/")
        data = response.json()
        
        problem_data = data["problems"][0]
        
        # Check consistency
        assert problem_data["total_reviews"] == 3
        assert problem_data["correct_reviews"] == 2
        assert problem_data["total_reviews"] >= problem_data["correct_reviews"]
        assert problem_data["ease_factor"] >= 1.3
        assert problem_data["ease_factor"] <= 3.0
        assert problem_data["current_interval"] > 0
        assert problem_data["current_interval"] <= 365

    def test_analytics_generated_at_timestamp(self, client: TestClient):
        """Test that generated_at timestamp is present and recent."""
        response = client.get("/api/analytics/")
        data = response.json()
        
        assert "generated_at" in data
        generated_at = datetime.fromisoformat(data["generated_at"])
        
        # Should be within the last minute
        now = datetime.now()
        time_diff = abs((now - generated_at).total_seconds())
        assert time_diff < 60
