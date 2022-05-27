import pytest
from app.calculation import add


@pytest.fixture
def zero_bank_account():
    return 12


@pytest.mark.parametrize(
    "num1, num2, result", [(3, 2, 5), (7, 1, 8), (12, 4, 16)]
)
def test_add(num1, num2, result):
    """Testing ad func"""
    assert add(num1, num2) == result
