from fastapi import FastAPI

from leetcode_execution_api.api.v1.endpoints.solutions import solution_router

app = FastAPI(title="Leetcode Execution API")
app.include_router(solution_router)
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Leetcode Execution API"}