from typing import Any

import pytest
from decorators.log_decorator import log


@log()
def successful_function(x: Any, y: Any) -> Any:
    return x + y


@log(filename="test_log.txt")
def error_function() -> None:
    raise ValueError("Test error")


def test_successful_function_with_log(capsys: Any) -> None:
    @log()
    def test_func(a: int, b: int) -> int:
        return a + b

    result = test_func(2, 3)
    assert result == 5
    captured = capsys.readouterr()
    assert "test_func ok" in captured.out


def test_error_function_with_log() -> None:
    @log(filename="error_test.log")
    def error_func() -> None:
        raise ValueError("Test exception")

    with pytest.raises(ValueError):
        error_func()

    with open("error_test.log", "r", encoding="utf-8") as f:
        content = f.read()
    assert "error_func error: ValueError" in content


def test_error_function() -> None:
    with pytest.raises(ValueError, match="Test error"):
        error_function()
    with open("test_log.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "error_function error: ValueError" in content
    assert "Inputs: (), {}" in content


def test_file_logging() -> None:
    @log(filename="another_log.txt")
    def simple_func() -> str:
        return "OK"

    simple_func()
    with open("another_log.txt", "r", encoding="utf-8") as f:
        content = f.read()
    assert "simple_func ok" in content
