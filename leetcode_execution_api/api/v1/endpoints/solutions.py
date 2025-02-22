from fastapi import APIRouter, Depends

from leetcode_execution_api.bl.k8s_handler.k8s_job_executor import K8sJobExecutor
from leetcode_execution_api.db.session import get_db
from leetcode_execution_api.bl.image_factory.python_image import PythonImageGenerator
from leetcode_execution_api.schemes.solution import Solution
from leetcode_execution_api.services.test_service import get_tests_by_question_by_id

solution_router = APIRouter()


@solution_router.post("/execute_solution")
async def execute_solution(solution: Solution, db=Depends(get_db)) -> dict:

    # Fetch tests by question_id
    tests = await get_tests_by_question_by_id(solution.question_id, db)

    # Generate Docker image for testing
    PythonImageGenerator().build_image(image_tag="abc", encoded_solution_code=solution.code,
                                       encoded_tests_code=[test.code for test in tests])
    # Execute k8s task with the docker image
    K8sJobExecutor().execute_job("abc")

    # Retrieve answer
    # Return to client
    return {"message": "Solution executed successfully"}
