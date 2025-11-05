from typing import Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize("currency", ["USD", "EUR"])
def test_filter_by_currency(transactions: List[Dict], currency: str) -> None:
    """Тестирует функцию filter_by_currency"""
    result = list(filter_by_currency(transactions, "USD"))
    assert len(result) == 2
    assert all(transaction["currency"] == "USD" for transaction in result)


def test_transaction_descriptions() -> None:
    """Тестирует функцию transaction_descriptions"""
    transactions = [
        {"description": "Transaction 1"},
        {"description": "Transaction 2"},
        {},
    ]
    descriptions = list(transaction_descriptions(transactions))
    assert len(descriptions) == 3
    assert descriptions == ["Transaction 1", "Transaction 2", "No description"]


def test_card_number_generator() -> None:
    """Тестирует функцию card_number_generator"""
    generator = card_number_generator()
    numbers = [next(generator) for _ in range(5)]
    assert len(numbers) == 5
    assert all(len(number) == 16 and number.isdigit() for number in numbers)
