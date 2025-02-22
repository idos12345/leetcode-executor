from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from leetcode_execution_api.db.models import Test


async def get_tests_by_question_by_id(question_id: int, db: AsyncSession):
    result = await db.execute(select(Test).where(Test.question_id == question_id))
    return result.scalars().all()
