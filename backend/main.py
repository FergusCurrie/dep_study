
from database import Due as DueModel
from database import Problem as ProblemModel
from database import Review as ReviewModel
from database import create_tables, engine, get_db
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from pathlib import Path
from schemas import Problem, ProblemCreate, ProblemSuspendRequest, ProblemWithReviews, Review, ReviewCreate
from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.problems.dispatch import dispatch_problem
from src.scheduling.dispatch import dispatch_scheduler
from typing import List

app = FastAPI()

# Define static directory
static_dir = Path(__file__).parent / "dist"
logger.info(static_dir)

# Mount static assets (JS, CSS, images, etc.) with cache headers
if static_dir.exists():
    app.mount(
        "/assets", 
        StaticFiles(directory=static_dir / "assets"), 
        name="assets"
    )
    
    # Mount other static files if they exist (favicon, manifest, etc.)
    for static_file in ["favicon.ico", "manifest.json", "robots.txt"]:
        file_path = static_dir / static_file
        if file_path.exists():
            @app.get(f"/{static_file}")
            async def serve_static_file():
                return FileResponse(file_path)



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
    # Lightweight migration for SQLite: add suspended columns if missing
    try:
        with engine.connect() as conn:
            cols = conn.exec_driver_sql("PRAGMA table_info('problems')").fetchall()
            existing_cols = {row[1] for row in cols}
            if 'suspended' not in existing_cols:
                conn.exec_driver_sql("ALTER TABLE problems ADD COLUMN suspended BOOLEAN NOT NULL DEFAULT 0")
                logger.info("Added 'suspended' column to problems table")
            if 'suspend_reason' not in existing_cols:
                conn.exec_driver_sql("ALTER TABLE problems ADD COLUMN suspend_reason TEXT NULL")
                logger.info("Added 'suspend_reason' column to problems table")
    except Exception as e:
        logger.error(f"Migration check failed: {e}")

# Problem endpoints
@app.post("/api/problems/", response_model=Problem)
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    db_problem = ProblemModel(name=problem.name)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@app.get("/api/problems/")
def read_problems(db: Session = Depends(get_db)):
    query = (
        db.query(DueModel, ProblemModel)
        .outerjoin(DueModel, ProblemModel.id == DueModel.problem_id)
        .filter(
            ProblemModel.suspended == False,
            or_(
                DueModel.due_date == None,          
                DueModel.due_date <= datetime.now()     
            )
    )
    )
    problems_and_due = query.all() 
    if len(problems_and_due) == 0:
        logger.error('No problems found')
        return {}
    _, problem = problems_and_due[0]
    logger.info(f'Read problems! - found {len(problems_and_due)}, select {problem.name}')
    problem_data = dispatch_problem(problem.name)
    problem_data['id'] = problem.id
    return problem_data

@app.post("/api/problems/{problem_id}/suspend", response_model=Problem)
def suspend_problem(problem_id: int, payload: ProblemSuspendRequest, db: Session = Depends(get_db)):
    problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    problem.suspended = True
    problem.suspend_reason = payload.reason
    db.commit()
    db.refresh(problem)
    return problem

@app.get("/api/problems/suspended", response_model=List[Problem])
def list_suspended_problems(db: Session = Depends(get_db)):
    problems = db.query(ProblemModel).filter(ProblemModel.suspended == True).all()
    return problems

@app.post("/api/problems/{problem_id}/unsuspend", response_model=Problem)
def unsuspend_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    problem.suspended = False
    problem.suspend_reason = None
    db.commit()
    db.refresh(problem)
    return problem

@app.get("/api/problems/{problem_id}", response_model=ProblemWithReviews)
def read_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.delete("/api/problems/{problem_id}")
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(ProblemModel).filter(ProblemModel.id == problem_id).first()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    db.delete(problem)
    db.commit()
    return {"message": "Problem deleted"}

# Review endpoints
@app.post("/api/reviews/", response_model=Review)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # Check if problem exists
    problem = db.query(ProblemModel).filter(ProblemModel.id == review.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    db_review = ReviewModel(problem_id=review.problem_id, correct=review.correct)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # find new due date 
    try:
        all_reviews = db.query(ReviewModel).filter(ReviewModel.problem_id == review.problem_id).all()
        scheduler = dispatch_scheduler("spaced_repetition")
        next_review_date = scheduler.get_next_review_date(all_reviews)

        # Delete old due date 
        current_due = db.query(DueModel).filter(DueModel.problem_id == review.problem_id).first()
        if current_due:
            current_due.due_date = next_review_date  
            logger.info(f'Updated due date to {current_due.due_date}')
        else:
            current_due = DueModel(due_date=next_review_date, problem_id=review.problem_id)
            db.add(current_due)
            logger.info(f'Created new due date {current_due.due_date}')

        db.commit()
        db.refresh(current_due)
    except Exception as e:
        logger.error(f'Found {e}')
    # logger.info(db_review)
    return db_review

@app.get("/api/reviews/", response_model=List[Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = db.query(ReviewModel).offset(skip).limit(limit).all()
    return reviews

@app.get("/api/reviews/problem/{problem_id}", response_model=List[Review])
def read_problem_reviews(problem_id: int, db: Session = Depends(get_db)):
    reviews = db.query(ReviewModel).filter(ReviewModel.problem_id == problem_id).all()
    return reviews

@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return {"message": "Review deleted"}

# Analytics endpoint
@app.get("/api/analytics/")
def get_analytics(db: Session = Depends(get_db)):
    """Get comprehensive analytics data for visualization."""
    
    # Get all problems with their due dates
    problems_query = (
        db.query(ProblemModel, DueModel)
        .outerjoin(DueModel, ProblemModel.id == DueModel.problem_id)
        .all()
    )
    
    # Get all reviews
    all_reviews = db.query(ReviewModel).all()
    
    # Calculate analytics
    total_problems = len(problems_query)
    problems_due_today = 0
    problems_due_this_week = 0
    problems_due_this_month = 0
    problems_overdue = 0
    
    # Group reviews by problem
    reviews_by_problem = {}
    for review in all_reviews:
        if review.problem_id not in reviews_by_problem:
            reviews_by_problem[review.problem_id] = []
        reviews_by_problem[review.problem_id].append(review)
    
    # Calculate ease factors and intervals for each problem
    problem_analytics = []
    scheduler = dispatch_scheduler("spaced_repetition")
    
    for problem, due in problems_query:
        problem_reviews = reviews_by_problem.get(problem.id, [])
        
        # Calculate next review date using scheduler
        if problem_reviews:
            next_review_date = scheduler.get_next_review_date(problem_reviews)
        else:
            next_review_date = datetime.now() + timedelta(days=1)
        
        # Calculate ease factor (simplified)
        if len(problem_reviews) > 0:
            recent_reviews = problem_reviews[-10:] if len(problem_reviews) > 10 else problem_reviews
            correct_count = sum(1 for r in recent_reviews if r.correct)
            ease_factor = 2.5 + (correct_count - len(recent_reviews) + correct_count) * 0.1
            ease_factor = max(1.3, min(3.0, ease_factor))
        else:
            ease_factor = 2.5
        
        # Calculate current interval
        if len(problem_reviews) == 0:
            current_interval = 1
        elif len(problem_reviews) == 1 and problem_reviews[0].correct:
            current_interval = 6
        else:
            # Simplified interval calculation
            correct_streak = 0
            for review in reversed(problem_reviews):
                if review.correct:
                    correct_streak += 1
                else:
                    break
            
            if correct_streak <= 1:
                current_interval = 6 if correct_streak == 1 else 1
            else:
                current_interval = min(365, int(6 * (ease_factor ** (correct_streak - 2))))
        
        # Check due status
        now = datetime.now()
        if due and due.due_date:
            days_until_due = (due.due_date - now).days
            if days_until_due < 0:
                problems_overdue += 1
            elif days_until_due == 0:
                problems_due_today += 1
            elif days_until_due <= 7:
                problems_due_this_week += 1
            elif days_until_due <= 30:
                problems_due_this_month += 1
        else:
            # No due date set, consider it due today
            problems_due_today += 1
        
        problem_analytics.append({
            "problem_id": problem.id,
            "problem_name": problem.name,
            "total_reviews": len(problem_reviews),
            "correct_reviews": sum(1 for r in problem_reviews if r.correct),
            "ease_factor": round(ease_factor, 2),
            "current_interval": current_interval,
            "next_review_date": next_review_date.isoformat(),
            "due_date": due.due_date.isoformat() if due and due.due_date else None,
            "days_until_due": (due.due_date - now).days if due and due.due_date else 0
        })
    
    # Calculate overall statistics
    total_reviews = len(all_reviews)
    correct_reviews = sum(1 for r in all_reviews if r.correct)
    overall_accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
    
    # Calculate average ease factor
    avg_ease_factor = sum(p["ease_factor"] for p in problem_analytics) / len(problem_analytics) if problem_analytics else 2.5
    
    return {
        "summary": {
            "total_problems": total_problems,
            "total_reviews": total_reviews,
            "overall_accuracy": round(overall_accuracy, 1),
            "average_ease_factor": round(avg_ease_factor, 2),
            "problems_due_today": problems_due_today,
            "problems_due_this_week": problems_due_this_week,
            "problems_due_this_month": problems_due_this_month,
            "problems_overdue": problems_overdue
        },
        "problems": problem_analytics,
        "generated_at": datetime.now().isoformat()
    }


# @app.get("/")
# def read_root():
#     return {"problem": generate_problem()}

# Serve React app for all non-API routes
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """
    Serve the React app for all routes that don't start with /api
    This enables client-side routing to work properly
    """
    # Skip API routes - they should be handled by explicit routes above
    logger.info(full_path)
    if full_path.startswith("api"):
        logger.info('IS api request')
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Skip already mounted static routes
    if full_path.startswith("assets"):
        raise HTTPException(status_code=404, detail="Static file not found")
    
    # For root or any other path, serve index.html (SPA routing)
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(
            index_file,
            media_type="text/html",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    
    raise HTTPException(status_code=404, detail="React app not found")

@app.post("/{full_path:path}")
async def catch_all_post(full_path: str):
    """
    Ensure non-API POST requests don't interfere with API routing.
    Return 404 for any POST that isn't an explicit API route.
    """
    if full_path.startswith("api"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)