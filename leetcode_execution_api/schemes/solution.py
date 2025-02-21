from pydantic import BaseModel

class Solution(BaseModel):
    question_id: int
    solution: str
