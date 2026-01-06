from recorder.replay import replay

def test_replay():
    replay(
        base_url="https://practicetestautomation.com/practice-test-login/",
        username="student",
        password="Password123"
    )
