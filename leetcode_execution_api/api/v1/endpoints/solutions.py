import time
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from leetcode_execution_api.bl.image_factory.image_generator import ImageGenerator, image_generator_parameters
from leetcode_execution_api.bl.k8s_handler.k8s_job_executor import K8sJobExecutor
from leetcode_execution_api.bl.k8s_handler.k8s_job_logs_fetcher import K8sJobLogsFetcher
from leetcode_execution_api.bl.log_parser.unitest_log_parser import UTestLogParser
from leetcode_execution_api.db.session import get_db
from leetcode_execution_api.schemes.solution import Solution
from leetcode_execution_api.services.test_service import get_tests_by_question_and_language
from leetcode_execution_api.constants import language_to_id
from sqlalchemy import text
solution_router = APIRouter()

@solution_router.get("/ping-db")
async def ping_db(session: AsyncSession = Depends(get_db)):
    result = await session.execute(text("SELECT 1"))
    return {"result": result.scalar()}

@solution_router.post("/execute_solution")
async def execute_solution(solution: Solution, db: AsyncSession = Depends(get_db)) -> dict:
    """
    execute solution as a k8s job
    :param solution: solution object
    :param db: db async session
    :return: response dict
    """

    language = solution.language.value
    image_name = f"{solution.question_id}-{language}--{time.time()}"

    # Fetch tests by question_id
    print(f"Fetching tests for question_id: {solution.question_id} and language: {language}")
    tests = await get_tests_by_question_and_language(solution.question_id, language_to_id.get(language),
                                                     db)

    # Generate Docker image for testing
    print(f"Generating Docker image for question_id: {solution.question_id} and language: {language}")
    (ImageGenerator(**(image_generator_parameters[language])).
     build_image(image_name=image_name, encoded_solution_code=solution.code,
                 encoded_tests_code=[test.code for test in tests]))

    # Execute k8s task with the docker image
    print(f"Executing k8s job for question_id: {solution.question_id} and language: {language}")
    K8sJobExecutor().execute_job(image_name)

    # Fetch logs from k8s
    print(f"Fetching logs for question_id: {solution.question_id} and language: {language}")
    logs = K8sJobLogsFetcher().fetch_logs(image_name)

    # Retrieve result from logs
    print(f"Parsing logs for question_id: {solution.question_id} and language: {language}")
    test_result = UTestLogParser(language=language).infer_solution_result_from_logs(logs)

    # Return to client
    print(f"Returning result for question_id: {solution.question_id} and language: {language}")
    return {"test_result": test_result, "logs": logs}
