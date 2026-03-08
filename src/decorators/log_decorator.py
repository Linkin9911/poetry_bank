import functools
from datetime import datetime
from typing import Callable
from typing import Optional
from typing import ParamSpec
from typing import TypeVar

# Определяем универсальные типы для сохранения сигнатуры функции
P = ParamSpec("P")
R = TypeVar("R")


def log(filename: Optional[str] = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Декоратор для логирования вызовов функций.

    Args:
        filename: Имя файла для записи логов. Если None — вывод в консоль.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] {func_name}"

            try:
                result = func(*args, **kwargs)
                log_entry = f"{log_message} ok"
                _write_log(log_entry, filename)
                return result
            except Exception as e:
                error_type = type(e).__name__
                inputs = f"Inputs: {args}, {kwargs}"
                log_entry = f"{log_message} error: {error_type}. {inputs}"
                _write_log(log_entry, filename)
                raise

        return wrapper

    return decorator


def _write_log(message: str, filename: Optional[str]) -> None:
    """Записывает лог в файл или консоль."""
    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
