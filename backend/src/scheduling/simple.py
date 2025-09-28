

from .scheduler_base import Scheduler
from database import Review
from datetime import datetime, timedelta


class SimpleScheduler(Scheduler):
    """
    A simple scheduler that implements a basic spaced repetition algorithm.
    
    Logic:
    - If there are no reviews, schedule for immediate review (now)
    - For each correct review, increment a counter by 1 day
    - For each incorrect review, reset the counter to 0
    - The next review date is the latest review date + (counter + 1) days
    
    This creates a simple progression where correct answers lead to longer intervals,
    but any mistake resets the progress back to immediate review.
    
    Example:
    - Review 1 (correct): Next review in 1 day
    - Review 2 (correct): Next review in 2 days  
    - Review 3 (incorrect): Next review in 1 day (reset)
    - Review 4 (correct): Next review in 2 days
    """
    
    def get_next_review_date(self, reviews: list[Review]) -> datetime:
        reviews.sort(key=lambda x: x.created_date)

        if len(reviews) == 0:
            return datetime.now()
        
        # calculate days to next review 
        timer = 0
        for i, review in enumerate(reviews):
            if not review.correct:
                timer = 0
            else:
                timer += 1

        # calculate that day 
        latest_review_day = max([x.created_date for x in reviews])
        return latest_review_day + timedelta(days=timer + 1)