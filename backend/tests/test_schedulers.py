import pytest
from datetime import datetime, timedelta
from database import Review
from src.scheduling.simple import SimpleScheduler
from src.scheduling.spaced_repetition import SpacedRepetitionScheduler
from src.scheduling.dispatch import dispatch_scheduler


class TestSimpleScheduler:
    def test_no_reviews(self):
        """Test scheduler with no reviews."""
        scheduler = SimpleScheduler()
        result = scheduler.get_next_review_date([])
        
        # Should return current time
        assert isinstance(result, datetime)
        assert result <= datetime.now()

    def test_single_correct_review(self):
        """Test scheduler with one correct review."""
        scheduler = SimpleScheduler()
        
        review = Review(
            id=1,
            problem_id=1,
            created_date=datetime.now() - timedelta(days=1),
            correct=True
        )
        
        result = scheduler.get_next_review_date([review])
        
        # Should be 1 day after the review
        expected = review.created_date + timedelta(days=2)  # timer + 1
        assert abs((result - expected).total_seconds()) < 60  # Within 1 minute

    def test_multiple_correct_reviews(self):
        """Test scheduler with multiple correct reviews."""
        scheduler = SimpleScheduler()
        
        reviews = [
            Review(id=1, problem_id=1, created_date=datetime.now() - timedelta(days=3), correct=True),
            Review(id=2, problem_id=1, created_date=datetime.now() - timedelta(days=2), correct=True),
            Review(id=3, problem_id=1, created_date=datetime.now() - timedelta(days=1), correct=True),
        ]
        
        result = scheduler.get_next_review_date(reviews)
        
        # Should be 4 days after the latest review (timer=3, +1)
        expected = reviews[-1].created_date + timedelta(days=4)
        assert abs((result - expected).total_seconds()) < 60

    def test_incorrect_review_resets_timer(self):
        """Test that incorrect review resets the timer."""
        scheduler = SimpleScheduler()
        
        reviews = [
            Review(id=1, problem_id=1, created_date=datetime.now() - timedelta(days=3), correct=True),
            Review(id=2, problem_id=1, created_date=datetime.now() - timedelta(days=2), correct=True),
            Review(id=3, problem_id=1, created_date=datetime.now() - timedelta(days=1), correct=False),  # Incorrect
        ]
        
        result = scheduler.get_next_review_date(reviews)
        
        # Should be 1 day after the latest review (timer reset to 0, +1)
        expected = reviews[-1].created_date + timedelta(days=1)
        assert abs((result - expected).total_seconds()) < 60


class TestSpacedRepetitionScheduler:
    def test_no_reviews(self):
        """Test scheduler with no reviews."""
        scheduler = SpacedRepetitionScheduler()
        result = scheduler.get_next_review_date([])
        
        # Should return 1 day from now
        expected = datetime.now() + timedelta(days=1)
        assert abs((result - expected).total_seconds()) < 60

    def test_first_review_correct(self):
        """Test scheduler with first correct review."""
        scheduler = SpacedRepetitionScheduler()
        
        review = Review(
            id=1,
            problem_id=1,
            created_date=datetime.now() - timedelta(days=1),
            correct=True
        )
        
        result = scheduler.get_next_review_date([review])
        
        # Should be 6 days after the review
        expected = review.created_date + timedelta(days=6)
        assert abs((result - expected).total_seconds()) < 60

    def test_second_review_correct(self):
        """Test scheduler with second correct review."""
        scheduler = SpacedRepetitionScheduler()
        
        reviews = [
            Review(id=1, problem_id=1, created_date=datetime.now() - timedelta(days=7), correct=True),
            Review(id=2, problem_id=1, created_date=datetime.now() - timedelta(days=1), correct=True),
        ]
        
        result = scheduler.get_next_review_date(reviews)
        
        # Should be 6 * ease_factor days after the latest review
        # With default ease_factor of 2.5, that's 15 days
        expected = reviews[-1].created_date + timedelta(days=15)
        assert abs((result - expected).total_seconds()) < 60

    def test_incorrect_review_resets_interval(self):
        """Test that incorrect review resets to short interval."""
        scheduler = SpacedRepetitionScheduler()
        
        reviews = [
            Review(id=1, problem_id=1, created_date=datetime.now() - timedelta(days=7), correct=True),
            Review(id=2, problem_id=1, created_date=datetime.now() - timedelta(days=1), correct=False),
        ]
        
        result = scheduler.get_next_review_date(reviews)
        
        # Should be 1 day after the latest review
        expected = reviews[-1].created_date + timedelta(days=1)
        assert abs((result - expected).total_seconds()) < 60

    def test_ease_factor_adjustment(self):
        """Test that ease factor adjusts based on performance."""
        scheduler = SpacedRepetitionScheduler()
        
        # Create reviews with mostly correct answers
        reviews = []
        for i in range(10):
            reviews.append(Review(
                id=i+1,
                problem_id=1,
                created_date=datetime.now() - timedelta(days=10-i),
                correct=True  # All correct
            ))
        
        ease_factor = scheduler._calculate_ease_factor(reviews)
        
        # Should be higher than initial 2.5 due to all correct answers
        assert ease_factor > 2.5
        assert ease_factor <= 3.0  # Should not exceed max

    def test_ease_factor_with_incorrect_answers(self):
        """Test that ease factor decreases with incorrect answers."""
        scheduler = SpacedRepetitionScheduler()
        
        # Create reviews with mostly incorrect answers
        reviews = []
        for i in range(10):
            reviews.append(Review(
                id=i+1,
                problem_id=1,
                created_date=datetime.now() - timedelta(days=10-i),
                correct=False  # All incorrect
            ))
        
        ease_factor = scheduler._calculate_ease_factor(reviews)
        
        # Should be lower than initial 2.5 due to all incorrect answers
        assert ease_factor < 2.5
        assert ease_factor >= 1.3  # Should not go below min

    def test_interval_calculation_edge_cases(self):
        """Test interval calculation with edge cases."""
        scheduler = SpacedRepetitionScheduler()
        
        # Test with no reviews
        interval = scheduler._calculate_interval([], 2.5)
        assert interval == 1
        
        # Test with one incorrect review
        reviews = [Review(id=1, problem_id=1, created_date=datetime.now(), correct=False)]
        interval = scheduler._calculate_interval(reviews, 2.5)
        assert interval == 1
        
        # Test with one correct review
        reviews = [Review(id=1, problem_id=1, created_date=datetime.now(), correct=True)]
        interval = scheduler._calculate_interval(reviews, 2.5)
        assert interval == 6

    def test_interval_cap(self):
        """Test that intervals are capped at 365 days."""
        scheduler = SpacedRepetitionScheduler()
        
        # Create many correct reviews to test cap
        reviews = []
        for i in range(20):
            reviews.append(Review(
                id=i+1,
                problem_id=1,
                created_date=datetime.now() - timedelta(days=20-i),
                correct=True
            ))
        
        interval = scheduler._calculate_interval(reviews, 2.5)
        assert interval <= 365


class TestSchedulerDispatch:
    def test_dispatch_simple_scheduler(self):
        """Test dispatching simple scheduler."""
        scheduler = dispatch_scheduler("simple")
        assert isinstance(scheduler, SimpleScheduler)

    def test_dispatch_spaced_repetition_scheduler(self):
        """Test dispatching spaced repetition scheduler."""
        scheduler = dispatch_scheduler("spaced_repetition")
        assert isinstance(scheduler, SpacedRepetitionScheduler)

    def test_dispatch_invalid_scheduler(self):
        """Test that invalid scheduler names raise errors."""
        with pytest.raises(ValueError):
            dispatch_scheduler("invalid_scheduler")
