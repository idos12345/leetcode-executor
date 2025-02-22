import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from leetcode_execution_api.bl.image_factory.image_generator import ImageGenerator, image_generator_parameters
from leetcode_execution_api.bl.k8s_handler.k8s_job_executor import K8sJobExecutor
from leetcode_execution_api.bl.k8s_handler.k8s_job_logs_fetcher import K8sJobLogsFetcher
from leetcode_execution_api.db.session import get_db
from leetcode_execution_api.schemes.solution import Solution
from leetcode_execution_api.services.test_service import get_tests_by_question_and_language
from leetcode_execution_api.constants import language_to_id

solution_router = APIRouter()


@solution_router.post("/execute_solution")
async def execute_solution(solution: Solution, db: AsyncSession = Depends(get_db)) -> dict:
    """
    execute solution as a k8s job
    :param solution: solution object
    :param db: db async session
    :return: response dict
    """

    image_name = f"{solution.question_id}-{solution.language.value}--{time.time()}"

    # Fetch tests by question_id
    tests = await get_tests_by_question_and_language(solution.question_id, language_to_id.get(solution.language.value),
                                                     db)

    # Generate Docker image for testing
    (ImageGenerator(**(image_generator_parameters[solution.language.value])).
     build_image(image_name=image_name, encoded_solution_code=solution.code,
                 encoded_tests_code=[test.code for test in tests]))

    # Execute k8s task with the docker image
    K8sJobExecutor().execute_job(image_name)

    logs = K8sJobLogsFetcher().fetch_logs(image_name)

    # Retrieve answer
    # Return to client
    return {"logs": logs}
