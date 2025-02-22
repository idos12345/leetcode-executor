python_dockerfile = """
FROM python:3.11-slim

WORKDIR /app

COPY test.py .

CMD ["python", "-m", "unittest", "test.py"]
"""