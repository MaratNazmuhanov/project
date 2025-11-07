from typing import Dict, List, Iterator, Any


def filter_by_currency(
    transactions: List[Dict[str, Any]],
    currency_code: str
) -> Iterator[Dict[str, Any]]:
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
        if 'operationAmount' not in transaction:
            continue

        operation_amount = transaction['operationAmount']

        # Проверяем, что в operationAmount есть поле currency
        if 'currency' not in operation_amount:
            continue

        currency = operation_amount['currency']

        # Проверяем соответствие кода валюты
        if currency.get('code') == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, возвращающий описания транзакций по очереди.
    """
    for transaction in transactions:
        # Проверяем наличие поля description в транзакции
        if "description" in transaction:
            yield transaction["description"]
        else:
            # Если описание отсутствует, возвращаем строку
            yield "Описание отсутствует"


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    Args:
        start: Начальное число диапазона.
        end: Конечное число диапазона, должно быть >= start.

    Yields:
        Строка с номером карты в формате "XXXX XXXX XXXX XXXX", где каждая группа — 4 цифры.

    Raises:
        ValueError: Если start или end вне допустимого диапазона или start > end.
    """
    # Проверка корректности входных данных
    if not (1 <= start <= 9999999999999999):
        raise ValueError("start должен быть в диапазоне от 1 до 9999999999999999")
    if not (1 <= end <= 9999999999999999):
        raise ValueError("end должен быть в диапазоне от 1 до 9999999999999999")
    if start > end:
        raise ValueError("start не может быть больше end")

    for number in range(start, end + 1):
        # Формируем строку из 16 цифр с ведущими нулями
        num_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры и объединяем пробелами
        formatted = f"{num_str[:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
        yield formatted
