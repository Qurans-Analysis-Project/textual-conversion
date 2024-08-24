from typing import Dict
from dataclasses import dataclass


@dataclass
class Chapter():
    name: str
    num_verses: int
    verses: Dict[int, str]


@dataclass
class Recitation():
    chapters: Dict[int, Chapter]