from pydantic import BaseModel
from datetime import datetime
from typing import List

class ProblemBase(BaseModel):
    name: str

class ProblemCreate(ProblemBase):
    pass

class Problem(ProblemBase):
    id: int
    created_date: datetime
    
    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    problem_id: int
    correct: bool

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    created_date: datetime
    
    class Config:
        from_attributes = True

class ProblemWithReviews(Problem):
    reviews: List[Review] = []