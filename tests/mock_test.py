from core.main import main


def test_health_check() -> None:
    if main() != "OK":
        raise AssertionError("Expected 'OK'")
