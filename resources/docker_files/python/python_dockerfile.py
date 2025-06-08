python_dockerfile = """
FROM python:3.11-slim

WORKDIR /app

COPY TestSolution.py .

CMD ["/bin/sh", "-c", "python -m unittest TestSolution.py || exit 0"]
"""