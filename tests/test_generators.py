from typing import Dict, List, Optional

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    "transaction, expected_description",
    [
        ({"amount": 100.0, "currency": "USD", "description": "Обед"}, "Обед"),
        ({"amount": 200.0, "currency": "USD", "description": "Ужин"}, "Ужин"),
    ],
)
def test_transaction_descriptions(transaction: Dict[str, Optional[float]], expected_description: str) -> None:
    """Тест: проверка генератора описаний транзакций."""
    descriptions = list(transaction_descriptions([transaction]))
    assert descriptions[0] == f"Транзакция: {expected_description}"


@pytest.mark.parametrize("start, end, expected_count", [(1, 3, 3), (1000, 1005, 6)])
def test_card_number_generator(start: int, end: int, expected_count: int) -> None:
    """Тест: проверка генератора банковских карт."""
    card_numbers = list(card_number_generator(start, end))
    assert len(card_numbers) == expected_count

    # Проверяем форматирование
    for number in card_numbers:
        assert len(number.replace(" ", "")) == 16


def test_filter_by_currency_with_fixture(sample_transactions: List[Dict[str, float]]) -> None:
    """Тест: проверка фильтрации транзакций по валюте с использованием фикстуры."""
    usd_transactions = filter_by_currency(sample_transactions, "USD")

    assert len(list(usd_transactions)) == 2
