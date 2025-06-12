FROM python:3.11

WORKDIR /leetcode_execution_api
COPY . /leetcode_execution_api

# Ensure system packages are updated
RUN apt-get update && apt-get install -y python3-setuptools && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install setuptools (which includes distutils)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gnupg \
        ca-certificates \
        debian-archive-keyring && \
    apt-get install -y --no-install-recommends \
        python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI application
CMD ["python", "-m", "uvicorn", "leetcode_execution_api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
