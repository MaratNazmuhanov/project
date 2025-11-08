from datetime import datetime
from typing import Any, Dict, List, Tuple, Union, cast

import pytest

# ============================================================================
# ФИКСТУРЫ ДЛЯ МОДУЛЯ MASKS
# ============================================================================


@pytest.fixture(
    params=[
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("7000 79 22 89 60 63 61", "7000 79** **** 6361"),
        ("9876543210987654", "9876 54** **** 7654"),
        ("1111222233334444", "1111 22** **** 4444"),
    ]
)
def valid_card_number_data(request: pytest.FixtureRequest) -> Tuple[str, str]:
    """Фикстура с валидными данными для номеров карт"""
    return cast(Tuple[str, str], request.param)


@pytest.fixture(
    params=[
        ("123456789012345", ValueError),  # 15 цифр
        ("12345678901234567", ValueError),  # 17 цифр
        ("invalid input", ValueError),  # Не цифры
        ("", ValueError),  # Пустая строка
    ]
)
def invalid_card_number_data(request: pytest.FixtureRequest) -> Tuple[str, type]:
    """Фикстура с невалидными данными для номеров карт"""
    return cast(Tuple[str, type], request.param)


@pytest.fixture(
    params=[
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("1234 5678 9012 3456 7890", "**7890"),
        ("98765432109876543210", "**3210"),
        ("11111111111111111111", "**1111"),
    ]
)
def valid_account_number_data(request: pytest.FixtureRequest) -> Tuple[str, str]:
    """Фикстура с валидными данными для номеров счетов"""
    return cast(Tuple[str, str], request.param)


@pytest.fixture(
    params=[
        ("1234567890", ValueError),  # Меньше 20 цифр
        ("invalid input", ValueError),  # Не цифры
        ("", ValueError),  # Пустая строка
    ]
)
def invalid_account_number_data(request: pytest.FixtureRequest) -> Tuple[str, type]:
    """Фикстура с невалидными данными для номеров счетов"""
    return cast(Tuple[str, type], request.param)


# ============================================================================
# ФИКСТУРЫ ДЛЯ МОДУЛЯ WIDGET
# ============================================================================


@pytest.fixture(
    params=[
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("American Express 1234567890123456", "American Express 1234 56** **** 3456"),
    ]
)
def valid_card_widget_data(request: pytest.FixtureRequest) -> Tuple[str, str]:
    """Фикстура с валидными данными для маскировки карт в виджете"""
    return cast(Tuple[str, str], request.param)


@pytest.fixture(
    params=[
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("счет 12345678901234567890", "счет **7890"),
    ]
)
def valid_account_widget_data(request: pytest.FixtureRequest) -> Tuple[str, str]:
    """Фикстура с валидными данными для маскировки счетов в виджете"""
    return cast(Tuple[str, str], request.param)


@pytest.fixture(
    params=[
        "Некорректная строка без номера",
        "Visa",
        "Счет",
        "Visa abc123def456",
    ]
)
def invalid_widget_data(request: pytest.FixtureRequest) -> str:
    """Фикстура с невалидными данными для виджета"""
    return cast(str, request.param)


@pytest.fixture(
    params=[
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2021-12-25T15:45:00.000000", "25.12.2021"),
        ("2023-01-01T00:00:00.000000", "01.01.2023"),
        ("2022-06-15T12:30:45.123456", "15.06.2022"),
        ("2020-02-29T23:59:59.999999", "29.02.2020"),  # Високосный год
    ]
)
def valid_date_data(request: pytest.FixtureRequest) -> Tuple[str, str]:
    """Фикстура с валидными данными для дат"""
    return cast(Tuple[str, str], request.param)


@pytest.fixture(
    params=[
        "invalid-date",
        "2024-13-01T00:00:00",  # Неверный месяц
        "2024-02-30T00:00:00",  # Неверный день
        "",
        "not-a-date",
    ]
)
def invalid_date_data(request: pytest.FixtureRequest) -> str:
    """Фикстура с невалидными данными для дат"""
    return cast(str, request.param)


# ============================================================================
# ФИКСТУРЫ ДЛЯ МОДУЛЯ PROCESSING
# ============================================================================


@pytest.fixture
def sample_data() -> List[Dict[str, Union[int, str]]]:
    """Базовые тестовые данные для обработки"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2023-10-02T15:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2023-09-30T09:15:00"},
        {"id": 4, "state": "PENDING", "date": "2023-10-03T08:45:00"},
        {"id": 5, "state": "CANCELED", "date": "2023-10-01T20:00:00"},
    ]


@pytest.fixture
def extended_sample_data() -> List[Dict[str, Union[int, str]]]:
    """Расширенные тестовые данные с большим количеством записей"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-10-01T12:00:00", "amount": 1000},
        {"id": 2, "state": "CANCELED", "date": "2023-10-02T15:30:00", "amount": 2000},
        {"id": 3, "state": "EXECUTED", "date": "2023-09-30T09:15:00", "amount": 1500},
        {"id": 4, "state": "PENDING", "date": "2023-10-03T08:45:00", "amount": 3000},
        {"id": 5, "state": "CANCELED", "date": "2023-10-01T20:00:00", "amount": 500},
        {"id": 6, "state": "EXECUTED", "date": "2023-09-28T14:20:00", "amount": 2500},
        {"id": 7, "state": "FAILED", "date": "2023-10-04T11:30:00", "amount": 1200},
        {"id": 8, "state": "EXECUTED", "date": "2023-10-05T16:45:00", "amount": 800},
    ]


@pytest.fixture(
    params=[
        ("EXECUTED", [1, 3]),
        ("CANCELED", [2, 5]),
        ("PENDING", [4]),
        ("FAILED", []),  # Нет записей с таким статусом в базовых данных
    ]
)
def filter_state_data(request: pytest.FixtureRequest) -> Tuple[str, List[int]]:
    """Параметризованная фикстура для тестирования фильтрации по состоянию"""
    return cast(Tuple[str, List[int]], request.param)


@pytest.fixture
def empty_data() -> List[Any]:
    """Пустой список для тестирования граничных случаев"""
    return []


@pytest.fixture
def data_with_missing_keys() -> List[Dict[str, Union[int, str]]]:
    """Данные с отсутствующими ключами для тестирования обработки ошибок"""
    return [
        {"id": 1},  # Нет ключа 'state'
        {"id": 2, "state": "EXECUTED"},  # Нет ключа 'date'
        {"id": 3, "state": "CANCELED", "date": "2023-10-01T12:00:00"},  # Полная запись
        {"state": "PENDING", "date": "2023-10-02T15:30:00"},  # Нет ключа 'id'
    ]


@pytest.fixture(
    params=[
        (
            True,
            [
                "2023-10-03T08:45:00",
                "2023-10-02T15:30:00",
                "2023-10-01T20:00:00",
                "2023-10-01T12:00:00",
                "2023-09-30T09:15:00",
            ],
        ),
        (
            False,
            [
                "2023-09-30T09:15:00",
                "2023-10-01T12:00:00",
                "2023-10-01T20:00:00",
                "2023-10-02T15:30:00",
                "2023-10-03T08:45:00",
            ],
        ),
    ]
)
def sort_order_data(request: pytest.FixtureRequest) -> Tuple[bool, List[str]]:
    """Параметризованная фикстура для тестирования сортировки"""
    return cast(Tuple[bool, List[str]], request.param)


# ============================================================================
# ФИКСТУРЫ ДЛЯ МОДУЛЯ GENERATORS
# ============================================================================


@pytest.fixture
def sample_transactions() -> List[Dict[str, Any]]:
    """Фикстура: набор тестовых транзакций с разными валютами."""
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2023-01-01T10:00:00",
            "operationAmount": {"amount": "1000.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Оплата услуг",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2023-01-02T11:00:00",
            "operationAmount": {"amount": "2000.00", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Перевод",
        },
        {
            "id": 3,
            "state": "PENDING",
            "date": "2023-01-03T12:00:00",
            "operationAmount": {"amount": "3000.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "Ожидает подтверждения",
        },
        # Транзакция без operationAmount
        {"id": 4, "state": "EXECUTED", "date": "2023-01-04T13:00:00", "description": "Без суммы"},
        # Транзакция с operationAmount, но без currency
        {
            "id": 5,
            "state": "EXECUTED",
            "date": "2023-01-05T14:00:00",
            "operationAmount": {"amount": "4000.00"},
            "description": "Без валюты",
        },
    ]


@pytest.fixture
def empty_transactions() -> List[Dict[str, Any]]:
    """Фикстура: пустой список транзакций."""
    return []


@pytest.fixture
def card_numbers() -> List[str]:
    """Фикстура: предопределенные номера карт для тестирования."""
    return [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]


# ============================================================================
# ОБЩИЕ ФИКСТУРЫ
# ============================================================================


@pytest.fixture
def mock_datetime() -> datetime:
    """Фикстура для мокирования datetime"""
    return datetime(2023, 10, 15, 12, 30, 45)


@pytest.fixture(scope="session")
def test_config() -> Dict[str, Union[int, str]]:
    """Конфигурация для тестов"""
    return {"card_length": 16, "account_min_length": 20, "date_format": "%d.%m.%Y", "default_state": "EXECUTED"}
