from enum import Enum

from pydantic import BaseModel

class Languages(Enum):
    python = "python"
    java = "java"

class Solution(BaseModel):
    question_id: int
    solution: str
    language: Languages
