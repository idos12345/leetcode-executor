from fastapi import FastAPI

app = FastAPI(title="Leetcode Execution API")

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Leetcode Execution API"}