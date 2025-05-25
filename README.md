# LeetCode Execution API

A FastAPI-based service for executing coding solutions inside a Kubernetes environment.

## 🚀 Installation & Usage

### 1️⃣ Launch Docker Desktop and Start Kubernetes

Ensure Docker Desktop is running and Kubernetes is enabled.
  
### 2️⃣ Clone the Repository

```sh
git clone https://github.com/idos12345/leetcode-executor.git
```

### 3️⃣ Copy the `.env` File

Copy the `.env` file to the project folder before running the application.


### 4️⃣ Create a Virtual Environment

```sh
python -m venv venv
```

### 5️⃣ Activate the Virtual Environment

- **Windows**:
  ```sh
  venv\Scripts\activate
  ```
- **Linux/macOS**:
  ```sh
  source venv/bin/activate
  ```

### 6️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 7️⃣ Run the FastAPI Server in Development Mode

```sh
cd leetcode_execution_api
fastapi dev main.py
```

### 8️⃣ Execute a Solution Using the CLI

```sh
cd ..
python cli.py 1 examples/bad_java_sol.txt java
```

## 🛠 Features

- 🏗 **Execute solutions as Kubernetes jobs**
- 📜 **Fetch logs from K8s job execution**
- 🧪 **Infer test results from unit test logs**
- 🖼 **Dynamically generate Docker images for testing**
- 🌐 **REST API built with FastAPI**

## 📄 API Endpoints

- **POST** `/execute_solution/` → Run a coding solution inside a Kubernetes job

## 📌 Example Payload:

```json
{
    "question_id": 1,
    "code": "ZGVmIGFkZChzZWxmLCBhLCBiKToNCglyZXR1cm4gYS1i",
    "language": "python"
}
```

## 🔧 Troubleshooting

- **ModuleNotFoundError: No module named 'fastapi'**\
  → Run: `pip install fastapi`
- **Command 'fastapi' not found**\
  → Ensure the virtual environment is activated before running commands.
