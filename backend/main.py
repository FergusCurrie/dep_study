
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.problems.dispatch import dispatch_problem
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db, create_tables, Problem as ProblemModel, Review as ReviewModel
from schemas import Problem, ProblemCreate, Review, ReviewCreate, ProblemWithReviews
import random 
from loguru import logger 

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    #allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"],  # Add this line
)

# Create tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# Problem endpoints
@app.post("/problems/", response_model=Problem)
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    db_problem = ProblemModel(name=problem.name)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@app.get("/problems/")
def read_problems(db: Session = Depends(get_db)):
    problems = db.query(ProblemModel).all()
    problem = random.choice(problems)
    logger.info(f'Read problems! - found {len(problems)}, select {problem.name}')
    problem_data = dispatch_problem(problem.name)
    problem_data['id'] = problem.id
    return problem_data

@app.get("/problems/{problem_id}", response_model=ProblemWithReviews)
def read_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.delete("/problems/{problem_id}")
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    db.delete(problem)
    db.commit()
    return {"message": "Problem deleted"}

# Review endpoints
@app.post("/reviews/", response_model=Review)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # Check if problem exists
    problem = db.query(ProblemModel).filter(ProblemModel.id == review.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    db_review = ReviewModel(problem_id=review.problem_id, correct=review.correct)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@app.get("/reviews/", response_model=List[Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = db.query(ReviewModel).offset(skip).limit(limit).all()
    return reviews

@app.get("/reviews/problem/{problem_id}", response_model=List[Review])
def read_problem_reviews(problem_id: int, db: Session = Depends(get_db)):
    reviews = db.query(ReviewModel).filter(ReviewModel.problem_id == problem_id).all()
    return reviews

@app.delete("/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}


@app.get("/")
def read_root():
    return {"problem": generate_problem()}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)