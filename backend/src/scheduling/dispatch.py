from .simple import SimpleScheduler
from .spaced_repetition import SpacedRepetitionScheduler


def dispatch_scheduler(name: str):
    if name == "simple":
        return SimpleScheduler()
    if name == "spaced_repetition":
        return SpacedRepetitionScheduler()
    raise ValueError(f"Unknown scheduler: {name}")
