from datetime import datetime
from pydantic import BaseModel
from typing import List

### problem 

class ProblemBase(BaseModel):
    name: str

class ProblemCreate(ProblemBase):
    pass

class Problem(ProblemBase):
    id: int
    created_date: datetime
    suspended: bool = False
    suspend_reason: str | None = None
    
    class Config:
        from_attributes = True

### review 
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

class ProblemSuspendRequest(BaseModel):
    reason: str | None = None

### due 
class DueBase(BaseModel):
    problem_id: int
    due_date: datetime 


class DueCreate(DueBase):
    pass

class Due(DueBase):
    id: int
    
    class Config:
        from_attributes = True

