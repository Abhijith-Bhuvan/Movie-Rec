from pydantic import BaseModel
from typing import List


class Director_Movies(BaseModel):
    title: str
    year: int
    genres: List[str]
    imdbRating: float
    director: str
