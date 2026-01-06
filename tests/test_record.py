from recorder.record import record

def test_record():
    record(
        base_url="https://practicetestautomation.com/practice-test-login/",
        username="student",
        password="Password123"
    )
