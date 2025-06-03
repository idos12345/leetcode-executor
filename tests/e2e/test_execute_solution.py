import requests


def test_health_check():
    resp = requests.get("http://localhost:8080/health")
    assert resp.status_code == 200


def test_python_execution():
    resp = requests.post(
        "http://localhost:8080/execute_solution",
        json={
            "question_id": 1,
            "code": "ZGVmIGFkZChzZWxmLCBhLCBiKToNCiAgICByZXR1cm4gYSArIGI=",
            "language": "python",
        },
    )
    assert resp.json()["test_result"] is True
