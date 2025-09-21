


from database import Review
from datetime import datetime, timedelta


def get_next_review_date(reviews: list[Review]):
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
    latest_review_day = min([x.created_date for x in reviews])
    return latest_review_day + timedelta(days=timer + 1)