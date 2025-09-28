from dataclasses import dataclass


@dataclass
class Problem:
    question: str
    options: list[str]
    correct: int


    