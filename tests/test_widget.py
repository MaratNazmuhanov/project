from typing import Tuple

import pytest

from src.widget import get_date, mask_account_card

# ============================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ mask_account_card
# ============================================================================


def test_mask_account_card_cards_with_fixture(valid_card_widget_data: Tuple[str, str]) -> None:
    """Тест маскировки карт с использованием фикстуры"""
    input_string, expected_output = valid_card_widget_data
    assert mask_account_card(input_string) == expected_output


def test_mask_account_card_accounts_with_fixture(valid_account_widget_data: Tuple[str, str]) -> None:
    """Тест маскировки счетов с использованием фикстуры"""
    input_string, expected_output = valid_account_widget_data
    assert mask_account_card(input_string) == expected_output


def test_mask_account_card_invalid_with_fixture(invalid_widget_data: str) -> None:
    """Тест невалидных данных с использованием фикстуры"""
    with pytest.raises(ValueError):
        mask_account_card(invalid_widget_data)


@pytest.mark.parametrize(
    "input_string,expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("American Express 1234567890123456", "American Express 1234 56** **** 3456"),
        ("UnionPay 9876543210987654", "UnionPay 9876 54** **** 7654"),
    ],
)
def test_mask_account_card_cards_parametrized(input_string: str, expected: str) -> None:
    """Параметризованный тест для маскировки карт"""
    assert mask_account_card(input_string) == expected


@pytest.mark.parametrize(
    "input_string,expected",
    [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("счет 12345678901234567890", "счет **7890"),
        ("СЧЕТ 98765432109876543210", "СЧЕТ **3210"),
    ],
)
def test_mask_account_card_accounts_parametrized(input_string: str, expected: str) -> None:
    """Параметризованный тест для маскировки счетов"""
    assert mask_account_card(input_string) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "Некорректная строка без номера",
        "Visa",
        "Счет",
        "Visa abc123def456",
        "123456789012345",  # Только номер без типа
    ],
)
def test_mask_account_card_invalid_parametrized(invalid_input: str) -> None:
    """Параметризованный тест для невалидных данных"""
    with pytest.raises(ValueError):
        mask_account_card(invalid_input)


# ============================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ get_date
# ============================================================================


def test_get_date_with_fixture(valid_date_data: Tuple[str, str]) -> None:
    """Тест форматирования дат с использованием фикстуры"""
    input_date, expected_output = valid_date_data
    assert get_date(input_date) == expected_output


def test_get_date_invalid_with_fixture(invalid_date_data: str) -> None:
    """Тест невалидных дат с использованием фикстуры"""
    with pytest.raises(ValueError):
        get_date(invalid_date_data)


@pytest.mark.parametrize(
    "input_date,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2021-12-25T15:45:00.000000", "25.12.2021"),
        ("2023-01-01T00:00:00.000000", "01.01.2023"),
        ("2022-06-15T12:30:45.123456", "15.06.2022"),
        ("2020-02-29T23:59:59.999999", "29.02.2020"),  # Високосный год
        ("1999-12-31T23:59:59.000000", "31.12.1999"),
    ],
)
def test_get_date_parametrized(input_date: str, expected: str) -> None:
    """Параметризованный тест для форматирования дат"""
    assert get_date(input_date) == expected


@pytest.mark.parametrize(
    "invalid_date",
    [
        "invalid-date",
        "2024-13-01T00:00:00",  # Неверный месяц
        "2024-02-30T00:00:00",  # Неверный день
        "",
        "not-a-date",
        "2024/03/11 12:30:45",  # Неверный формат
    ],
)
def test_get_date_invalid_parametrized(invalid_date: str) -> None:
    """Параметризованный тест для невалидных дат"""
    with pytest.raises(ValueError):
        get_date(invalid_date)


# ============================================================================
# ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ
# ============================================================================


def test_mask_account_card_edge_cases() -> None:
    """Тест граничных случаев"""
    # Тест с минимальной длиной номера карты
    assert mask_account_card("Test 1234567890123456") == "Test 1234 56** **** 3456"

    # Тест с минимальной длиной номера счета
    assert mask_account_card("Счет 12345678901234567890") == "Счет **7890"


def test_get_date_edge_cases() -> None:
    """Тест граничных случаев для дат"""
    # Начало года
    assert get_date("2023-01-01T00:00:00.000000") == "01.01.2023"

    # Конец года
    assert get_date("2023-12-31T23:59:59.999999") == "31.12.2023"

    # Високосный год
    assert get_date("2020-02-29T12:00:00.000000") == "29.02.2020"


def test_mask_account_card_empty_string() -> None:
    """Отдельный тест для пустой строки"""
    with pytest.raises(ValueError):
        mask_account_card("")
