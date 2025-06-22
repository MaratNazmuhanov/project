from typing import Any, Dict, List, Tuple, Union

import pytest

from src.processing import filter_by_state, sort_by_date

# ============================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ filter_by_state
# ============================================================================


def test_filter_by_state_default(sample_data: List[Dict[str, Union[int, str]]]) -> None:
    """Тест фильтрации по состоянию по умолчанию ('EXECUTED')"""
    result = filter_by_state(sample_data)
    # Ожидаемые id: 1 и 3
    expected_ids = [1, 3]
    assert [item["id"] for item in result] == expected_ids
    # Все результаты имеют 'state' == 'EXECUTED'
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_with_fixture(
    sample_data: List[Dict[str, Union[int, str]]], filter_state_data: Tuple[str, List[int]]
) -> None:
    """Тест фильтрации с использованием параметризованной фикстуры"""
    state, expected_ids = filter_state_data
    result = filter_by_state(sample_data, state)
    actual_ids = [item["id"] for item in result]
    assert actual_ids == expected_ids
    # Проверяем, что все результаты имеют правильный state (если есть результаты)
    if result:
        assert all(item["state"] == state for item in result)


@pytest.mark.parametrize(
    "state,expected_count",
    [
        ("EXECUTED", 2),
        ("CANCELED", 2),
        ("PENDING", 1),
        ("FAILED", 0),
        ("UNKNOWN", 0),
    ],
)
def test_filter_by_state_parametrized(
    sample_data: List[Dict[str, Union[int, str]]], state: str, expected_count: int
) -> None:
    """Параметризованный тест для фильтрации по состоянию"""
    result = filter_by_state(sample_data, state)
    assert len(result) == expected_count
    if result:
        assert all(item["state"] == state for item in result)


def test_filter_by_state_extended_data(extended_sample_data: List[Dict[str, Union[int, str]]]) -> None:
    """Тест фильтрации с расширенными данными"""
    # Тест с EXECUTED
    executed = filter_by_state(extended_sample_data, "EXECUTED")
    assert len(executed) == 4  # В расширенных данных 4 записи с EXECUTED
    assert all(item["state"] == "EXECUTED" for item in executed)

    # Тест с FAILED
    failed = filter_by_state(extended_sample_data, "FAILED")
    assert len(failed) == 1
    assert failed[0]["id"] == 7


def test_filter_by_state_empty_data(empty_data: List[Any]) -> None:
    """Тест фильтрации пустого списка"""
    result = filter_by_state(empty_data)
    assert result == []


def test_filter_by_state_missing_keys(data_with_missing_keys: List[Dict[str, Union[int, str]]]) -> None:
    """Тест фильтрации данных с отсутствующими ключами"""
    result = filter_by_state(data_with_missing_keys, "EXECUTED")
    # Только один элемент имеет state='EXECUTED'
    assert len(result) == 1
    assert result[0]["id"] == 2


# ============================================================================
# ТЕСТЫ ДЛЯ ФУНКЦИИ sort_by_date
# ============================================================================


def test_sort_by_date_desc(sample_data: List[Dict[str, Union[int, str]]]) -> None:
    """Тест сортировки по дате по убыванию (по умолчанию)"""
    sorted_data = sort_by_date(sample_data)
    # Первый элемент должен иметь самую позднюю дату
    assert sorted_data[0]["date"] == "2023-10-03T08:45:00"
    # Последний - самую раннюю
    assert sorted_data[-1]["date"] == "2023-09-30T09:15:00"


def test_sort_by_date_asc(sample_data: List[Dict[str, Union[int, str]]]) -> None:
    """Тест сортировки по дате по возрастанию"""
    sorted_data = sort_by_date(sample_data, reverse=False)
    # Первый элемент - самая ранняя дата
    assert sorted_data[0]["date"] == "2023-09-30T09:15:00"
    # Последний - самая поздняя
    assert sorted_data[-1]["date"] == "2023-10-03T08:45:00"


def test_sort_by_date_with_fixture(
    sample_data: List[Dict[str, Union[int, str]]], sort_order_data: Tuple[bool, List[str]]
) -> None:
    """Тест сортировки с использованием параметризованной фикстуры"""
    reverse, expected_order = sort_order_data
    sorted_data = sort_by_date(sample_data, reverse=reverse)
    actual_dates = [item["date"] for item in sorted_data]
    assert actual_dates == expected_order


@pytest.mark.parametrize(
    "reverse,first_date,last_date",
    [
        (True, "2023-10-03T08:45:00", "2023-09-30T09:15:00"),
        (False, "2023-09-30T09:15:00", "2023-10-03T08:45:00"),
    ],
)
def test_sort_by_date_parametrized(
    sample_data: List[Dict[str, Union[int, str]]], reverse: bool, first_date: str, last_date: str
) -> None:
    """Параметризованный тест для сортировки по дате"""
    sorted_data = sort_by_date(sample_data, reverse=reverse)
    assert sorted_data[0]["date"] == first_date
    assert sorted_data[-1]["date"] == last_date


def test_sort_by_date_extended_data(extended_sample_data: List[Dict[str, Union[int, str]]]) -> None:
    """Тест сортировки с расширенными данными"""
    sorted_desc = sort_by_date(extended_sample_data, reverse=True)
    sorted_asc = sort_by_date(extended_sample_data, reverse=False)

    # Проверяем, что сортировка работает правильно
    assert sorted_desc[0]["date"] == "2023-10-05T16:45:00"  # Самая поздняя
    assert sorted_desc[-1]["date"] == "2023-09-28T14:20:00"  # Самая ранняя

    assert sorted_asc[0]["date"] == "2023-09-28T14:20:00"  # Самая ранняя
    assert sorted_asc[-1]["date"] == "2023-10-05T16:45:00"  # Самая поздняя


def test_sort_by_date_empty_data(empty_data: List[Any]) -> None:
    """Тест сортировки пустого списка"""
    result = sort_by_date(empty_data)
    assert result == []


def test_sort_by_date_missing_keys(data_with_missing_keys: List[Dict[str, Union[int, str]]]) -> None:
    """Тест сортировки данных с отсутствующими ключами"""
    sorted_data = sort_by_date(data_with_missing_keys)
    # Проверяем, что сортировка не падает
    assert len(sorted_data) == len(data_with_missing_keys)


# ============================================================================
# КОМБИНИРОВАННЫЕ ТЕСТЫ
# ============================================================================


def test_filter_and_sort_combination(extended_sample_data: List[Dict[str, Union[int, str]]]) -> None:
    """Тест комбинации фильтрации и сортировки"""
    # Сначала фильтруем по EXECUTED
    filtered = filter_by_state(extended_sample_data, "EXECUTED")
    # Затем сортируем по дате
    sorted_filtered = sort_by_date(filtered, reverse=False)

    # Проверяем результат
    assert len(sorted_filtered) == 4  # В расширенных данных 4 записи с EXECUTED
    assert all(item["state"] == "EXECUTED" for item in sorted_filtered)
    # Проверяем порядок дат (по возрастанию)
    dates = [item["date"] for item in sorted_filtered]
    assert dates == sorted(dates)


@pytest.mark.parametrize(
    "state,expected_count",
    [
        ("EXECUTED", 4),  # Исправлено: в расширенных данных 4 записи с EXECUTED
        ("CANCELED", 2),
        ("PENDING", 1),
        ("FAILED", 1),
    ],
)
def test_filter_sort_parametrized(
    extended_sample_data: List[Dict[str, Union[int, str]]], state: str, expected_count: int
) -> None:
    """Параметризованный тест комбинации фильтрации и сортировки"""
    filtered = filter_by_state(extended_sample_data, state)
    sorted_data = sort_by_date(filtered)

    assert len(sorted_data) == expected_count
    if sorted_data:
        assert all(item["state"] == state for item in sorted_data)
        # Проверяем, что сортировка по убыванию работает
        dates = [item["date"] for item in sorted_data]
        assert dates == sorted(dates, reverse=True)
