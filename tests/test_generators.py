from typing import Any, Dict, Iterator, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# --- ТЕСТЫ ДЛЯ transaction_descriptions ---


@pytest.mark.parametrize(
    ("transactions,expected"),
    [
        # Случай 1: транзакции с description (из sample_transactions)
        (
            [
                {"description": "Оплата услуг"},
                {"description": "Перевод"},
                {"description": "Ожидает подтверждения"},
            ],
            ["Оплата услуг", "Перевод", "Ожидает подтверждения"],
        ),
        # Случай 2: нет поля description
        (
            [{"id": 1}, {"amount": 100}],
            ["", ""],
        ),
        # Случай 3: description = None
        (
            [{"description": None}, {"description": None}],
            ["", ""],
        ),
        # Случай 4: пустое description
        (
            [{"description": ""}, {"description": ""}],
            ["", ""],
        ),
        # Случай 5: смешанный набор (включая транзакции из sample_transactions)
        (
            [
                {"description": "Оплата"},
                {},
                {"description": None},
                {"description": ""},
                {"note": "без описания"},
            ],
            ["Оплата", "", "", "", ""],
        ),
        # Случай 6: пустой список
        (
            [],
            [],
        ),
    ],
)
def test_transaction_descriptions_parametrized(
    transactions: List[Dict[str, Any]],
    expected: List[str],
) -> None:
    """Параметризованный тест для transaction_descriptions."""
    result: List[str] = list(transaction_descriptions(transactions))
    assert result == expected


def test_transaction_descriptions_lazy_evaluation(
    sample_transactions: List[Dict[str, Any]],
) -> None:
    """Тест: ленивая оценка генератора (используем вашу фикстуру)."""
    gen: Iterator[str] = transaction_descriptions(sample_transactions)

    # Первые 3 транзакции имеют description
    assert next(gen) == "Оплата услуг"
    assert next(gen) == "Перевод"
    assert next(gen) == "Ожидает подтверждения"
    # 4-я: есть description → "Без суммы"
    assert next(gen) == "Без суммы"
    # 5-я: есть description → "Без валюты"
    assert next(gen) == "Без валюты"


def test_transaction_descriptions_empty_list(
    empty_transactions: List[Dict[str, Any]],
) -> None:
    """Тест: пустой список транзакций (используем фикстуру)."""
    result: List[str] = list(transaction_descriptions(empty_transactions))
    assert result == []


# --- ТЕСТЫ ДЛЯ card_number_generator ---


@pytest.mark.parametrize(
    ("start,end,expected"),
    [
        # Случай 1: базовый диапазон 1–3
        (
            1,
            3,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
            ],
        ),
        # Случай 2: одно число
        (
            1234567890123456,
            1234567890123456,
            ["1234 5678 9012 3456"],
        ),
        # Случай 3: переход через разряд
        (
            9999999999999997,
            9999999999999999,
            [
                "9999 9999 9999 9997",
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
        # Случай 4: минимальное значение
        (
            1,
            1,
            ["0000 0000 0000 0001"],
        ),
        # Случай 5: максимальное значение
        (
            9999999999999999,
            9999999999999999,
            ["9999 9999 9999 9999"],
        ),
    ],
)
def test_card_number_generator_valid_ranges(
    start: int,
    end: int,
    expected: List[str],
) -> None:
    """Параметризованный тест: корректные диапазоны для card_number_generator."""
    generator: Iterator[str] = card_number_generator(start, end)
    result: List[str] = list(generator)
    assert result == expected


@pytest.mark.parametrize(
    ("start,end,error_msg"),
    [
        # start < 1
        (0, 5, "start должен быть в диапазоне от 1 до 9999999999999999"),
        (-1, 5, "start должен быть в диапазоне от 1 до 9999999999999999"),
        # end > 9999999999999999
        (1, 10**16, "end должен быть в диапазоне от 1 до 9999999999999999"),
        # start > end
        (5, 1, "start не может быть больше end"),
    ],
)
def test_card_number_generator_invalid_ranges(
    start: int,
    end: int,
    error_msg: str,
) -> None:
    """Параметризованный тест: проверка исключений для некорректных диапазонов."""
    with pytest.raises(ValueError) as excinfo:
        list(card_number_generator(start, end))
    assert error_msg in str(excinfo.value)


def test_card_number_generator_lazy() -> None:
    """Тест: ленивая генерация (проверка через next)."""
    generator: Iterator[str] = card_number_generator(1, 3)

    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    # Проверяем, что генератор не завершается после двух вызовов
    assert next(generator) == "0000 0000 0000 0003"

    # Убеждаемся, что при исчерпании поднимается StopIteration
    with pytest.raises(StopIteration):
        next(generator)


def test_card_number_generator_with_fixture(
    card_numbers: List[str],
) -> None:
    """Тест: сравнение с предопределёнными номерами карт из фикстуры."""
    # Генерируем первые 5 номеров начиная с 1
    generator: Iterator[str] = card_number_generator(1, 5)
    result: List[str] = list(generator)

    # Сравниваем только первые 5 элементов (сколько есть в фикстуре)
    assert result[:5] == card_numbers[:5]


def test_card_number_generator_single_value() -> None:
    """Тест: генерация одного номера карты."""
    generator: Iterator[str] = card_number_generator(1234, 1234)
    result: List[str] = list(generator)
    assert result == ["0000 0000 0000 1234"]


def test_card_number_generator_max_value() -> None:
    """Тест: генерация максимального возможного номера."""
    generator: Iterator[str] = card_number_generator(9999999999999999, 9999999999999999)
    result: List[str] = list(generator)
    assert result == ["9999 9999 9999 9999"]


# --- ТЕСТЫ ДЛЯ filter_by_currency ---


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


@pytest.mark.parametrize(
    "currency_code,expected_ids",
    [
        ("USD", [1, 3]),
        ("EUR", [2]),
        ("RUB", []),
    ],
)
def test_parametrized_filter(
    sample_transactions: List[Dict[str, Any]], currency_code: str, expected_ids: List[int]
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
    """Тест: передача None в качестве кода валюты (ожидается пустой результат)."""
    result = list(filter_by_currency(sample_transactions, None))  # type: ignore
    assert len(result) == 0  # Должно вернуть пустой список
