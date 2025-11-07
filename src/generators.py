from typing import Dict, Generator, List, Optional


def filter_by_currency(transactions: List[Dict[str, float]], currency: str) -> Generator[Dict[str, float], None, None]:
    """
    Генератор транзакций с заданной валютой.

    Аргументы:
        transactions: Список словарей с транзакциями.
        currency: Код валюты (например, 'USD').

    Возвращает:
        Генератор, поочередно возвращающий совпадающие транзакции.
    """
    for transaction in transactions:
        if transaction.get("currency") == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Optional[float]]]) -> Generator[str, None, None]:
    """
    Генератор описаний транзакций.

    Аргументы:
        transactions: Список словарей с транзакциями.

    Возвращает:
        Генератор строк с описаниями транзакций.
    """
    for transaction in transactions:
        description = transaction.get("description", "Описание отсутствует")
        yield f"Транзакция: {description}"


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """
    Генератор банковских карт в формате XXXX XXXX XXXX XXXX.

    Аргументы:
        start: Начальное значение диапазона.
        end: Конечное значение диапазона.

    Возвращает:
        Генератор строк с номерами карт.
    """
    for number in range(start, end + 1):
        yield f"{number:016d}"
