import requests


def test_python_execution():
    resp = requests.post(
        "http://localhost:8080/execute_solution",
        json={
            "question_id": 1,
            "code": "ZGVmIGFkZChzZWxmLCBhLCBiKToNCiAgICByZXR1cm4gYSArIGI=",
            "language": "python",
        },
        timeout=30
    )
    assert resp.json()["test_result"] is True
