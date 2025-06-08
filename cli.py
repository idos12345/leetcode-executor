import argparse
import base64
import itertools
import sys
import threading
import time

import requests

API_URL = "http://127.0.0.1:8080/execute_solution/"


def encode_file_to_base64(file_path):
    """Reads a file and encodes its content to Base64."""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")

def execute_solution(question_id, file_path, language):
    """Sends a POST request with the encoded code to the API."""
    encoded_code = encode_file_to_base64(file_path)

    payload = {
        "question_id": question_id,
        "code": encoded_code,
        "language": language
    }

    print("\n⏳ Processing...\n")
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        result = response.json()
        test_result = result.get("test_result", False)
        logs = result.get("logs", "")

        if test_result:
            print("\n✅ Test Passed!\n")
        else:
            print("\n❌ Test Failed! Logs:\n")
            print(logs)
    else:
        print(f"⚠️ API Error: {response.status_code} - {response.text}")


def main():
    parser = argparse.ArgumentParser(description="Execute code solution via API.")
    parser.add_argument("question_id", type=int, help="Question ID")
    parser.add_argument("file", type=str, help="Path to the code file")
    parser.add_argument("language", type=str, help="Programming language")

    args = parser.parse_args()
    execute_solution(args.question_id, args.file, args.language)


if __name__ == "__main__":
    main()
