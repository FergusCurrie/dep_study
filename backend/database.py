# database.py
import os
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Database setup
# Priority:
# 1) Respect explicit DATABASE_URL if provided
# 2) Otherwise select sqlite file based on env flag: BACKEND_ENV/APP_ENV/ENV
#    dev -> dev.db, prd|prod|production -> prd.db, default -> dev.db
_explicit_db_url = os.getenv("DATABASE_URL")
_env = (
    os.getenv("BACKEND_ENV")
    or os.getenv("APP_ENV")
    or os.getenv("ENV")
    or "dev"
).lower()

from loguru import logger

logger.info(f'DATABASE_URL: {_explicit_db_url} _env: {_env}')
if _explicit_db_url:
    SQLALCHEMY_DATABASE_URL = _explicit_db_url
else:
    _env_to_filename = {
        "dev": "dev.db",
        "development": "dev.db",
        "prd": "prd.db",
        "prod": "prd.db",
        "production": "prd.db",
    }
    _db_file = _env_to_filename.get(_env, "dev.db")
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{_db_file}"

logger.info(f'SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}')


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    name = Column(String, index=True)
    suspended = Column(Boolean, default=False, nullable=False)
    suspend_reason = Column(String, nullable=True)
    
    # Relationship to reviews
    reviews = relationship("Review", back_populates="problem")
    due = relationship("Due", back_populates="problem")
    tags = relationship("Tag", secondary="problem_tags", back_populates="problems")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    created_date = Column(DateTime, default=datetime.utcnow)
    correct = Column(Boolean, default=False)
    
    # Relationship to problem
    problem = relationship("Problem", back_populates="reviews")

class Due(Base):
    __tablename__ = "due"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"))
    due_date = Column(DateTime)
    
    # Relationship to problem
    problem = relationship("Problem", back_populates="due")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    problems = relationship("Problem", secondary="problem_tags", back_populates="tags")

class ProblemTag(Base):
    __tablename__ = "problem_tags"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), index=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), index=True)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
