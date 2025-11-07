from typing import Dict, List, Any, Iterator

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    ("transactions" ,"expected"),
            [
                # Случай 1: нормальные транзакции с описанием
                (
                        [
                            {"description": "Перевод организации"},
                            {"description": "Перевод со счета на счет"},
                        ],
                        ["Перевод организации", "Перевод со счета на счет"],
                ),
                # Случай 2: транзакции без описания
                (
                        [
                            {"id": 1},
                            {"amount": 100},
                        ],
                        ["", ""],
                ),
                # Случай 3: смешанные транзакции (есть/нет описания)
                (
                        [
                            {"description": "Оплата услуг"},
                            {"id": 999},
                            {"description": "Поступление"},
                        ],
                        ["Оплата услуг", "", "Поступление"],
                ),
                # Случай 4: пустой список
                (
                        [],
                        [],
                ),
                # Случай 5: одна транзакция с описанием
                (
                        [{"description": "Единственный перевод"}],
                        ["Единственный перевод"],
                ),
                # Случай 6: одна транзакция без описания
                (
                        [{"id": 1}],
                        [""],
                ),
                # Случай 7: полностью пустые словари
                (
                        [{}, {}, {}],
                        ["", "", ""],
                ),
            ],
    )

def test_transaction_descriptions_parametrized(
        transactions: List[Dict[str, Any]],
        expected: List[str],
) -> None:
    """
    Параметризованный тест для функции transaction_descriptions.

    Проверяет различные сценарии:
    - Нормальные транзакции с описанием
    - Транзакции без поля description
    - Смешанные случаи
    - Пустой список
    - Одиночные транзакции
    - Полностью пустые словари
    """
    descriptions = transaction_descriptions(transactions)
    result = list(descriptions)

    assert result == expected


def test_transaction_descriptions_lazy_evaluation(
        sample_transactions: List[Dict[str, Any]]
) -> None:
    """Тест: ленивая оценка — генератор должен выдавать значения по запросу."""
    descriptions = transaction_descriptions(sample_transactions)

    # Получаем только первые два значения
    first = next(descriptions)
    second = next(descriptions)

    assert first == "Перевод организации"
    assert second == "Перевод со счета на счет"


def test_transaction_descriptions_empty_list(
        empty_transactions: List[Dict[str, Any]]
) -> None:
    """Тест: пустой список транзакций — должен вернуть пустой итератор."""
    descriptions = transaction_descriptions(empty_transactions)
    result = list(descriptions)
    assert len(result) == 0


@pytest.mark.parametrize(
    ("start", "end" , "expected"),
            [
                # Случай 1: диапазон 1–5 (базовый пример)
                (
                        1, 5,
                        [
                            "0000 0000 0000 0001",
                            "0000 0000 0000 0002",
                            "0000 0000 0000 0003",
                            "0000 0000 0000 0004",
                            "0000 0000 0000 0005",
                        ],
                ),
                # Случай 2: одно число (start == end)
                (
                        1234567890123456, 1234567890123456,
                        ["1234 5678 9012 3456"],
                ),
                # Случай 3: диапазон с «переходом» через разряд
                (
                        9999999999999998, 10000000000000001,
                        [
                            "9999 9999 9999 9998",
                            "9999 9999 9999 9999",
                            "1000 0000 0000 0000",
                            "1000 0000 0000 0001",
                        ],
                ),
                # Случай 4: минимальное значение
                (
                        1, 1,
                        ["0000 0000 0000 0001"],
                ),
                # Случай 5: максимальное значение
                (
                        9999999999999999, 9999999999999999,
                        ["9999 9999 9999 9999"],
                ),
            ],
    )

def test_card_number_generator_valid_ranges(
        start: int,
        end: int,
        expected: List[str],
) -> None:
    """
    Параметризованный тест: проверка корректной работы генератора для разных диапазонов.

    Проверяет:
    - Базовый случай (1–5)
    - Одиночное число
    - Переход через разряд (999... → 1000...)
    - Минимальное и максимальное значения
    """
    generator: Iterator[str] = card_number_generator(start, end)
    result: List[str] = list(generator)

    assert result == expected


def test_card_number_generator_empty_range() -> None:
    """Тест: start > end — должен вызвать ValueError."""
    with pytest.raises(ValueError, match="start не может быть больше end"):
        list(card_number_generator(5, 1))


def test_card_number_generator_start_out_of_range() -> None:
    """Тест: start < 1 — должен вызвать ValueError."""
    with pytest.raises(ValueError, match="start должен быть в диапазоне"):
        list(card_number_generator(0, 5))


def test_card_number_generator_end_out_of_range() -> None:
    """Тест: end > 9999999999999999 — должен вызвать ValueError."""
    with pytest.raises(ValueError, match="end должен быть в диапазоне"):
        list(card_number_generator(1, 10000000000000000))


def test_card_number_generator_lazy_evaluation() -> None:
    """Тест: ленивая оценка — генератор должен выдавать значения по запросу."""
    generator = card_number_generator(1, 3)

    # Получаем только первое значение
    first = next(generator)
    assert first == "0000 0000 0000 0001"

    # Получаем второе значение
    second = next(generator)
    assert second == "0000 0000 0000 0002"

    # Останавливаемся, не запрашивая третье


def test_filter_usd(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест: фильтрация по USD."""
    usd_iter = filter_by_currency(sample_transactions, "USD")
    result = list(usd_iter)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 3

def test_filter_eur(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест: фильтрация по EUR."""
    eur_iter = filter_by_currency(sample_transactions, "EUR")
    result = list(eur_iter)
    assert len(result) == 1
    assert result[0]["id"] == 2

def test_filter_rub_no_matches(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест: валюта RUB отсутствует — должен вернуть пустой итератор."""
    rub_iter = filter_by_currency(sample_transactions, "RUB")
    result = list(rub_iter)
    assert len(result) == 0

def test_empty_list(empty_transactions: List[Dict[str, Any]]) -> None:
    """Тест: пустой список транзакций."""
    usd_iter = filter_by_currency(empty_transactions, "USD")
    result = list(usd_iter)
    assert len(result) == 0

def test_no_operation_amount(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест: транзакция без operationAmount пропускается."""
    usd_iter = filter_by_currency(sample_transactions, "USD")
    result = list(usd_iter)
    assert all(t["id"] != 4 for t in result)

def test_no_currency_field(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест: транзакция с operationAmount, но без currency пропускается."""
    usd_iter = filter_by_currency(sample_transactions, "USD")
    result = list(usd_iter)
    assert all(t["id"] != 5 for t in result)

@pytest.mark.parametrize("currency_code,expected_ids", [
    ("USD", [1, 3]),
    ("EUR", [2]),
    ("RUB", []),
])
def test_parametrized_filter(
    sample_transactions: List[Dict[str, Any]],
    currency_code: str,
    expected_ids: List[int]
) -> None:
    """Параметризованный тест: проверка фильтрации для разных валют."""
    filtered = filter_by_currency(sample_transactions, currency_code)
    result_ids = [t["id"] for t in filtered]
    assert result_ids == expected_ids

def test_case_sensitive(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест: фильтрация чувствительна к регистру."""
    usd_lower = filter_by_currency(sample_transactions, "usd")
    result = list(usd_lower)
    assert len(result) == 0

def test_none_currency_code(sample_transactions: List[Dict[str, Any]]) -> None:
    """Тест: передача None в качестве кода валюты."""
    with pytest.raises(TypeError):
        list(filter_by_currency(sample_transactions, None))  # type: ignore
