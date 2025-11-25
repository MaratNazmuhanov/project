import os
import tempfile
from typing import Any, Callable

import pytest

from src.decorators import log


class TestLogDecorator:
    """Тесты для декоратора log"""

    def test_log_success_console(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест успешного выполнения с выводом в консоль"""

        @log()
        def successful_function(x: int, y: int) -> int:
            return x + y

        result = successful_function(2, 3)

        # Проверяем результат
        assert result == 5

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "successful_function ok" in captured.out

    def test_log_error_console(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест ошибки с выводом в консоль"""

        @log()
        def failing_function(x: int, y: int) -> float:
            return x / y

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ZeroDivisionError):
            failing_function(5, 0)

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "failing_function error: ZeroDivisionError" in captured.out
        assert "Inputs: (5, 0), {}" in captured.out

    def test_log_success_file(self) -> None:
        """Тест успешного выполнения с записью в файл"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp_file:
            filename = tmp_file.name

        try:

            @log(filename=filename)
            def test_function(a: str, b: str) -> str:
                return a + b

            result = test_function("Hello, ", "World!")

            # Проверяем результат
            assert result == "Hello, World!"

            # Проверяем запись в файл
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                assert "test_function ok" in content

        finally:
            # Удаляем временный файл
            if os.path.exists(filename):
                os.unlink(filename)

    def test_log_error_file(self) -> None:
        """Тест ошибки с записью в файл"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp_file:
            filename = tmp_file.name

        try:

            @log(filename=filename)
            def error_function(items: list, index: int) -> Any:
                return items[index]

            # Проверяем, что исключение пробрасывается
            with pytest.raises(IndexError):
                error_function([1, 2, 3], 10)

            # Проверяем запись в файл
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
                assert "error_function error: IndexError" in content
                assert "Inputs: ([1, 2, 3], 10), {}" in content

        finally:
            # Удаляем временный файл
            if os.path.exists(filename):
                os.unlink(filename)

    def test_log_preserves_function_metadata(self) -> None:
        """Тест сохранения метаданных функции"""

        @log()
        def sample_function(x: int) -> int:
            """Тестовая функция"""
            return x * 2

        assert sample_function.__name__ == "sample_function"
        assert sample_function.__doc__ == "Тестовая функция"

    def test_log_with_keyword_arguments(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест с именованными аргументами"""

        @log()
        def kw_function(name: str, age: int = 0) -> str:
            return f"{name} is {age} years old"

        result = kw_function("Alice", age=25)

        assert result == "Alice is 25 years old"

        captured = capsys.readouterr()
        assert "kw_function ok" in captured.out

    @pytest.mark.parametrize(
        "func,args,kwargs,expected_result,expected_error",
        [
            (lambda x, y: x + y, (1, 2), {}, 3, None),  # Успешное выполнение
            (lambda x: x / 0, (5,), {}, None, ZeroDivisionError),  # Ошибка
            (lambda: "constant", (), {}, "constant", None),  # Без аргументов
        ],
    )
    def test_log_parametrized(
        self,
        func: Callable[..., Any],
        args: tuple,
        kwargs: dict[str, Any],
        expected_result: Any,
        expected_error: type[Exception] | None,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Параметризованный тест декоратора log"""

        decorated_func = log()(func)

        if expected_error:
            with pytest.raises(expected_error):
                decorated_func(*args, **kwargs)

            captured = capsys.readouterr()
            assert f"{func.__name__} error: {expected_error.__name__}" in captured.out
        else:
            result = decorated_func(*args, **kwargs)
            assert result == expected_result

            captured = capsys.readouterr()
            assert f"{func.__name__} ok" in captured.out
