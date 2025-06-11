from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from leetcode_execution_api.db.models import Test
import asyncio


async def get_tests_by_question_and_language(
    question_id: int, language_id: int, db: AsyncSession
):
    try:
        async with db.begin():
            result = await asyncio.wait_for(
                db.execute(
                    select(Test).where(
                        Test.question_id == question_id, Test.language_id == language_id
                    )
                ),
                timeout=3,
            )
    except asyncio.TimeoutError:
        print("❌ Query timed out")
        raise
    print("✅ After query")
    return result.scalars().all()
