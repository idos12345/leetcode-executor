FROM python:3.12

WORKDIR /leetcode_execution_api
COPY . /leetcode_execution_api

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

CMD ["uvicorn", "leetcode_execution_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
