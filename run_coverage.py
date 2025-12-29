import pytest

pytest.main(["tests", "--cov=modules", "--cov-report=html", "--cov-fail-under=100"])
