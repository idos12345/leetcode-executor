from fastapi import APIRouter
from leetcode_execution_api.schemes.solution import Solution

router = APIRouter()


@router.post("/execute_solution")
async def execute_solution(solution: Solution) -> None:
    pass

    # TODO Implement

    # Fetch question and tests by question_id
    # Generate Docker image for testing
    # Execute k8s task with the docker image
    # Retrieve answer
    # Return to client
