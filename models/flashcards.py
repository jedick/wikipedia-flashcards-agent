"""Pydantic models for flashcard data."""

from pydantic import BaseModel
from typing import List


class Flashcard(BaseModel):
    """Represents a single flashcard with question and answer."""
    question: str
    answer: str


class FlashcardsResult(BaseModel):
    """Contains the results of flashcard generation with a list of flashcards."""
    flashcards: List[Flashcard]
