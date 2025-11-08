from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по коду валюты.

    Args:
        transactions (list): Список словарей, представляющих транзакции.
        currency_code (str): Код валюты для фильтрации (например, "USD").

    Yields:
        dict: Транзакция, где валюта операции соответствует заданной.
    """
    for transaction in transactions:
        # Проверяем, что в транзакции есть поле operationAmount
        if "operationAmount" not in transaction:
            continue

        operation_amount = transaction["operationAmount"]

        # Проверяем, что в operationAmount есть поле currency
        if "currency" not in operation_amount:
            continue

        currency = operation_amount["currency"]

        # Проверяем соответствие кода валюты
        if currency.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """
    Извлекает описания транзакций.

    Для каждой транзакции возвращает:
    - значение поля "description", если оно есть и не None;
    - пустую строку "", если поля "description" нет или оно None.

    Args:
        transactions: Список транзакций (словарей).

    Yields:
        Строка с описанием транзакции или пустая строка.
    """
    for transaction in transactions:
        description = transaction.get("description")
        yield "" if description is None else description


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.


    Args:
        start: Начальное число диапазона (от 1 до 9999999999999999).
        end: Конечное число диапазона (от 1 до 9999999999999999), должно быть >= start.


    Yields:
        Строка с номером карты в формате "XXXX XXXX XXXX XXXX".


    Raises:
        ValueError: Если start/end вне диапазона [1, 9999999999999999] или start > end.
    """
    if not (1 <= start <= 9999999999999999):
        raise ValueError("start должен быть в диапазоне от 1 до 9999999999999999")
    if not (1 <= end <= 9999999999999999):
        raise ValueError("end должен быть в диапазоне от 1 до 9999999999999999")
    if start > end:
        raise ValueError("start не может быть больше end")

    for number in range(start, end + 1):
        num_str = f"{number:016d}"
        yield f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
