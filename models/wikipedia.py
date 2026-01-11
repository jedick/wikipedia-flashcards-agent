"""Pydantic models for Wikipedia article data."""

from pydantic import BaseModel
from typing import List


class WikipediaArticle(BaseModel):
    """Represents a single Wikipedia article with title and content."""
    title: str
    content: str


class WikipediaSearchResult(BaseModel):
    """Contains the results of a Wikipedia search with a list of articles."""
    articles: List[WikipediaArticle]
