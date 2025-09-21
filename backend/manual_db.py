# helpers for using db from cli 

# # Problem endpoints
# @app.post("/problems/", response_model=Problem)
# def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
#     db_problem = ProblemModel(name=problem.name)
#     db.add(db_problem)
#     db.commit()
#     db.refresh(db_problem)
#     return db_problem

from database import get_db, Review
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
    return latest_review_day + timedelta(days=timer)
    
    return timer  

if __name__ == "__main__":
    db = next(get_db())
    # p = Problem(name='rec_sys_matrix_fact')
    # db.add(p)
    # db.commit()
    reviews = db.query(Review).all()
    
    print(get_next_review_date(reviews))
    print(datetime.now() >= get_next_review_date(reviews))
    for x in reviews:
        print(x.correct, x.created_date)
    
    reviews.sort(key=lambda x: x.created_date)
    print('\n\n')
    for x in reviews:
        print(x.correct, x.created_date)