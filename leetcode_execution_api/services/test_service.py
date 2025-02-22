from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from leetcode_execution_api.db.models import Test


async def get_tests_by_question_and_language(question_id: int, language_id: int, db: AsyncSession):
    result = await db.execute(select(Test).where(Test.question_id == question_id and Test.language_id == language_id))
    return result.scalars().all()
