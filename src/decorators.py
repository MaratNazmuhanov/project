import functools
import datetime
from typing import Any, Callable, Optional, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """
    Декоратор для логирования выполнения функций.

    Args:
        filename: Имя файла для записи логов. Если None - вывод в консоль.

    Returns:
        Декорированную функцию с логированием.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Формируем базовую информацию
            func_name = func.__name__
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                success_message = f"{timestamp} - {func_name} ok\n"

                # Записываем лог
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(success_message)
                else:
                    print(success_message, end='')

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = (
                    f"{timestamp} - {func_name} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}\n"
                )

                # Записываем лог ошибки
                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(error_message)
                else:
                    print(error_message, end='')

                # Пробрасываем исключение дальше
                raise

        return cast(F, wrapper)

    return decorator
