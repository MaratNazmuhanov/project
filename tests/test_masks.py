from typing import Tuple

import pytest

from src.masks import get_mask_account, get_mask_card_number

# ============================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ get_mask_card_number
# ============================================================================


def test_get_mask_card_number_valid(valid_card_number_data: Tuple[str, str]) -> None:
    """Тест маскировки валидных номеров карт с использованием фикстуры"""
    input_number, expected_output = valid_card_number_data
    assert get_mask_card_number(input_number) == expected_output


def test_get_mask_card_number_invalid(invalid_card_number_data: Tuple[str, type]) -> None:
    """Тест маскировки невалидных номеров карт с использованием фикстуры"""
    input_number, expected_exception = invalid_card_number_data
    with pytest.raises(expected_exception):
        get_mask_card_number(input_number)


@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("9999888877776666", "9999 88** **** 6666"),
    ],
)
def test_get_mask_card_number_parametrized(card_number: str, expected: str) -> None:
    """Параметризованный тест для маскировки номеров карт"""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "123456789012345",  # 15 цифр
        "12345678901234567",  # 17 цифр
        "invalid",  # Не цифры
        "",  # Пустая строка
    ],
)
def test_get_mask_card_number_invalid_parametrized(invalid_input: str) -> None:
    """Параметризованный тест для невалидных номеров карт"""
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_input)


# ============================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ get_mask_account
# ============================================================================


def test_get_mask_account_valid(valid_account_number_data: Tuple[str, str]) -> None:
    """Тест маскировки валидных номеров счетов с использованием фикстуры"""
    input_number, expected_output = valid_account_number_data
    assert get_mask_account(input_number) == expected_output


def test_get_mask_account_invalid(invalid_account_number_data: Tuple[str, type]) -> None:
    """Тест маскировки невалидных номеров счетов с использованием фикстуры"""
    input_number, expected_exception = invalid_account_number_data
    with pytest.raises(expected_exception):
        get_mask_account(input_number)


@pytest.mark.parametrize(
    "account_number,expected",
    [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("98765432109876543210", "**3210"),
    ],
)
def test_get_mask_account_parametrized(account_number: str, expected: str) -> None:
    """Параметризованный тест для маскировки номеров счетов"""
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "1234567890",  # Меньше 20 цифр
        "invalid",  # Не цифры
        "",  # Пустая строка
    ],
)
def test_get_mask_account_invalid_parametrized(invalid_input: str) -> None:
    """Параметризованный тест для невалидных номеров счетов"""
    with pytest.raises(ValueError):
        get_mask_account(invalid_input)


# ============================================================================
# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ
# ============================================================================


def test_get_mask_card_number_with_spaces() -> None:
    """Тест обработки номеров карт с пробелами"""
    assert get_mask_card_number("7000 79 22 89 60 63 61") == "7000 79** **** 6361"
    assert get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"


def test_get_mask_account_with_spaces() -> None:
    """Тест обработки номеров счетов с пробелами"""
    assert get_mask_account("1234 5678 9012 3456 7890") == "**7890"
    assert get_mask_account("7365 4108 4301 3587 4305") == "**4305"
