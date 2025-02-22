from sqlalchemy.ext.asyncio import AsyncSession
from leetcode_execution_api.db.models import Question


async def get_question_by_id(question_id: int, db: AsyncSession):
    result = await db.get(Question, question_id)
    return result
