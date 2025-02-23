python_dockerfile = """
FROM python:3.11-slim

WORKDIR /app

COPY TestSolution.py .

CMD ["python", "-m", "unittest", "TestSolution.py"]
"""