# helpers for using db from cli 

# Problem endpoints
# @app.post("/problems/", response_model=Problem)
# def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
#     db_problem = ProblemModel(name=problem.name)
#     db.add(db_problem)
#     db.commit()
#     db.refresh(db_problem)
#     return db_problem

from database import Problem, get_db

if __name__ == "__main__":
    db = next(get_db())
    p = Problem(name='batch_norm')
    db.add(p)
    db.commit()

