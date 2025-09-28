from abc import ABC, abstractmethod
from database import Review
from datetime import datetime


class Scheduler(ABC):
    @abstractmethod
    def get_next_review_date(self, reviews: list[Review]) -> datetime:
        pass

