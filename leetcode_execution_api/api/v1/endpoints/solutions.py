from fastapi import APIRouter, Depends
from leetcode_execution_api.db.session import get_db
from leetcode_execution_api.schemes.solution import Solution
from leetcode_execution_api.services.question_service import get_question_by_id
from leetcode_execution_api.services.test_service import get_tests_by_question_by_id

solution_router = APIRouter()


@solution_router.post("/execute_solution")
async def execute_solution(solution: Solution, db=Depends(get_db)) -> dict:
    # TODO Implement

    # Fetch question and tests by question_id
    question = await get_question_by_id(solution.question_id, db)
    tests = await get_tests_by_question_by_id(solution.question_id, db)
    return {"question_code": question.code,
            "tests_code": [test.code for test in tests]}

    # Generate Docker image for testing
    # Execute k8s task with the docker image
    # Retrieve answer
    # Return to client
