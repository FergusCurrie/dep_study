from .scheduler_base import Scheduler
from database import Review
from datetime import datetime, timedelta


class SpacedRepetitionScheduler(Scheduler):
    """
    An advanced spaced repetition scheduler based on the SM-2 algorithm with modifications.
    
    This scheduler implements a more sophisticated approach to spaced repetition that:
    - Uses exponential backoff for successful reviews
    - Applies different intervals for different difficulty levels
    - Gradually increases intervals for consistent success
    - Resets progress more gracefully on failures
    
    Algorithm:
    1. First review: 1 day
    2. Second review: 6 days  
    3. Subsequent reviews: Previous interval * ease factor
    4. Ease factor starts at 2.5 and adjusts based on performance
    5. Failed reviews reset to shorter intervals but don't completely restart
    
    Ease Factor Adjustments:
    - Correct answer: ease_factor += 0.1 (up to max 3.0)
    - Incorrect answer: ease_factor -= 0.2 (down to min 1.3)
    
    Interval Progression:
    - Interval 1: 1 day
    - Interval 2: 6 days
    - Interval 3+: Previous interval * ease_factor
    
    This creates a more natural learning curve that adapts to individual performance.
    """
    
    def __init__(self, initial_ease_factor: float = 2.5, min_ease_factor: float = 1.3, max_ease_factor: float = 3.0):
        self.initial_ease_factor = initial_ease_factor
        self.min_ease_factor = min_ease_factor
        self.max_ease_factor = max_ease_factor
    
    def get_next_review_date(self, reviews: list[Review]) -> datetime:
        reviews.sort(key=lambda x: x.created_date)
        
        if len(reviews) == 0:
            # First review: 1 day
            return datetime.now() + timedelta(days=1)
        
        # Calculate ease factor based on recent performance
        ease_factor = self._calculate_ease_factor(reviews)
        
        # Determine current interval based on review history
        interval_days = self._calculate_interval(reviews, ease_factor)
        
        # Get the most recent review date
        latest_review_date = max(reviews, key=lambda r: r.created_date).created_date
        
        return latest_review_date + timedelta(days=interval_days)
    
    def _calculate_ease_factor(self, reviews: list[Review]) -> float:
        """Calculate the current ease factor based on recent performance."""
        ease_factor = self.initial_ease_factor
        
        # Look at the last 10 reviews for performance calculation
        recent_reviews = reviews[-10:] if len(reviews) > 10 else reviews
        
        for review in recent_reviews:
            if review.correct:
                ease_factor += 0.1
            else:
                ease_factor -= 0.2
        
        # Clamp to valid range
        return max(self.min_ease_factor, min(self.max_ease_factor, ease_factor))
    
    def _calculate_interval(self, reviews: list[Review], ease_factor: float) -> int:
        """Calculate the next interval in days based on review history and ease factor."""
        correct_streak = 0
        
        # Count consecutive correct answers from the end
        for review in reversed(reviews):
            if review.correct:
                correct_streak += 1
            else:
                break
        
        if correct_streak == 0:
            # Failed the last review: short interval
            return 1
        if correct_streak == 1:
            # First correct review: 6 days
            return 6
        # Subsequent correct reviews: exponential backoff
        # Start with 6 days for the second review, then multiply by ease factor
        base_interval = 6
        for _ in range(correct_streak - 2):
            base_interval = int(base_interval * ease_factor)

        # Cap at 365 days to prevent extremely long intervals
        return min(base_interval, 365)
