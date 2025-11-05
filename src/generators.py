from typing import Dict, Generator, List


def filter_by_currency(transactions: List[Dict], currency: str) -> List[Dict]:
    """Фильтрует транзакции по указанной валюте и возвращает список этих транзакций.

    Аргументы:
        transactions (List[Dict]): Список транзакций.
        currency (str): Валюта, по которой фильтруем транзакции.

    Возвращает:
        List[Dict]: Список транзакций указанной валюты.
    """
    return [transaction for transaction in transactions if transaction["currency"] == currency]


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """Возвращает описание каждой операции по очереди.
    Если транзакция не имеет описания, то выводится 'No description'.

    Аргументы:
        transactions (List[Dict]): Список транзакций.

    Возвращает:
        Generator[str, None, None]: Генератор описаний транзакций.
    """
    for transaction in transactions:
        yield transaction.get("description", "No description")


def card_number_generator(start: int = 10**15, end: int = 10**16) -> Generator[str, None, None]:
    """Генерирует номера банковских карт в формате XXXX XXXX XXXX XXXX.
    Генератор может сгенерировать номера карт в заданном диапазоне от start до end.

    Аргументы:
        start (int): Начальное значение для генерации. По умолчанию 10**15.
        end (int): Конечное значение для генерации. По умолчанию 10**16.

    Возвращает:
        Generator[str, None, None]: Генератор номеров карт в формате XXXX XXXX XXXX XXXX.
    """
    current = start
    while current < end:
        yield f"{current:016}"
        current += 1
