import pytest

from utils import validate_email


@pytest.mark.parametrize(
    "value,is_valid", [("fail", False), ("", False), ("turtle@turtle.turtle", True)]
)
def test_validate_email(value: str, is_valid: bool) -> None:
    assert validate_email(value) is is_valid
