import os
from unittest.mock import MagicMock, patch

import pytest
import requests.exceptions

from src.external_api import convert_to_rub, get_amount_in_rub, get_exchange_rate


# Тесты для get_exchange_rate
@patch("src.external_api._API_KEY", "test_key")
@patch("src.external_api.requests.get")
def test_get_exchange_rate_success(mock_requests_get: MagicMock) -> None:
    """Тест успешного получения курса валют"""
    # Настраиваем мок ответа API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "rates": {"RUB": 91.45}}
    mock_requests_get.return_value = mock_response

    rate = get_exchange_rate("USD")

    assert rate == 91.45
    mock_requests_get.assert_called_once()
    call_args = mock_requests_get.call_args
    assert call_args[0][0] == "https://api.apilayer.com/exchangerates_data/latest"
    assert call_args[1]["params"] == {"base": "USD", "symbols": "RUB"}
    assert call_args[1]["headers"]["apikey"] == "test_key"


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_get_exchange_rate_timeout(mock_requests_get: MagicMock) -> None:
    """Тест таймаута при запросе"""
    # Используем правильное исключение из requests
    mock_requests_get.side_effect = requests.exceptions.Timeout("Timeout")

    rate = get_exchange_rate("USD")

    assert rate is None


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_get_exchange_rate_connection_error(mock_requests_get: MagicMock) -> None:
    """Тест ошибки соединения"""
    # Используем правильное исключение из requests
    mock_requests_get.side_effect = requests.exceptions.ConnectionError("Connection failed")

    rate = get_exchange_rate("USD")

    assert rate is None


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_get_exchange_rate_unauthorized(mock_requests_get: MagicMock) -> None:
    """Тест ошибки авторизации API"""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_requests_get.return_value = mock_response

    rate = get_exchange_rate("USD")

    assert rate is None


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_get_exchange_rate_rate_limit(mock_requests_get: MagicMock) -> None:
    """Тест превышения лимита запросов"""
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_requests_get.return_value = mock_response

    rate = get_exchange_rate("USD")

    assert rate is None


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_get_exchange_rate_invalid_json(mock_requests_get: MagicMock) -> None:
    """Тест невалидного JSON в ответе"""
    mock_response = MagicMock()
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_requests_get.return_value = mock_response

    rate = get_exchange_rate("USD")

    assert rate is None


@patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"})
@patch("src.external_api.requests.get")
def test_get_exchange_rate_api_error(mock_requests_get: MagicMock) -> None:
    """Тест ошибки API в ответе"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
    mock_requests_get.return_value = mock_response

    rate = get_exchange_rate("USD")

    assert rate is None


@patch.dict(os.environ, {}, clear=True)
def test_get_exchange_rate_no_api_key() -> None:
    """Тест отсутствия API ключа"""
    # Перезагружаем модуль, чтобы обновить кэшированную переменную
    import importlib

    import src.external_api

    importlib.reload(src.external_api)

    from src.external_api import get_exchange_rate

    rate = get_exchange_rate("USD")

    assert rate is None


# Тесты для convert_to_rub
def test_convert_to_rub_rub() -> None:
    """Тест конвертации RUB в RUB (без изменений)"""
    result = convert_to_rub(100.0, "RUB")
    assert result == 100.0


@patch("src.external_api.get_exchange_rate")
def test_convert_to_rub_usd_success(mock_get_rate: MagicMock) -> None:
    """Тест успешной конвертации USD в RUB"""
    mock_get_rate.return_value = 91.45

    result = convert_to_rub(100.0, "USD")

    assert result == 9145.0
    mock_get_rate.assert_called_once_with("USD")


@patch("src.external_api.get_exchange_rate")
def test_convert_to_rub_eur_success(mock_get_rate: MagicMock) -> None:
    """Тест успешной конвертации EUR в RUB"""
    mock_get_rate.return_value = 99.50

    result = convert_to_rub(50.0, "EUR")

    assert result == 4975.0
    mock_get_rate.assert_called_once_with("EUR")


@patch("src.external_api.get_exchange_rate")
def test_convert_to_rub_api_failure(mock_get_rate: MagicMock) -> None:
    """Тест конвертации при ошибке API"""
    mock_get_rate.return_value = None

    result = convert_to_rub(100.0, "USD")

    assert result is None


def test_get_amount_in_rub_rub() -> None:
    """Тест транзакции в рублях"""
    transaction = {"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB"}}}

    result = get_amount_in_rub(transaction)
    assert result == 1000.50


@patch("src.external_api.convert_to_rub")
def test_get_amount_in_rub_usd_success(mock_convert: MagicMock) -> None:
    """Тест успешной конвертации USD транзакции"""
    mock_convert.return_value = 9145.0

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    result = get_amount_in_rub(transaction)
    assert result == 9145.0
    mock_convert.assert_called_once_with(100.0, "USD")


@patch("src.external_api.convert_to_rub")
def test_get_amount_in_rub_eur_success(mock_convert: MagicMock) -> None:
    """Тест успешной конвертации EUR транзакции"""
    mock_convert.return_value = 10123.0

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "EUR"}}}

    result = get_amount_in_rub(transaction)
    assert result == 10123.0
    mock_convert.assert_called_once_with(100.0, "EUR")


@patch("src.external_api.convert_to_rub")
def test_get_amount_in_rub_usd_failure(mock_convert: MagicMock) -> None:
    """Тест неудачной конвертации USD транзакции"""
    mock_convert.return_value = None

    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    with pytest.raises(ValueError, match="Не удалось конвертировать USD в RUB"):
        get_amount_in_rub(transaction)


def test_get_amount_in_rub_unknown_currency() -> None:
    """Тест транзакции с неизвестной валютой"""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "GBP"}}}

    result = get_amount_in_rub(transaction)
    assert result == 100.00


def test_get_amount_in_rub_invalid_amount_format() -> None:
    """Тест невалидного формата суммы"""
    transaction = {"operationAmount": {"amount": "invalid", "currency": {"code": "RUB"}}}

    with pytest.raises(ValueError, match="Ошибка при обработке транзакции"):
        get_amount_in_rub(transaction)


def test_get_amount_in_rub_empty_currency() -> None:
    """Тест транзакции с пустой валютой"""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {}}}

    result = get_amount_in_rub(transaction)
    assert result == 100.00  # Должен использовать RUB по умолчанию


def test_get_amount_in_rub_currency_without_code() -> None:
    """Тест транзакции с валютой без кода"""
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"name": "Рубль"}}}  # Нет поля code

    result = get_amount_in_rub(transaction)
    assert result == 100.00  # Должен использовать RUB по умолчанию


def test_get_amount_in_rub_integer_amount() -> None:
    """Тест транзакции с целочисленной суммой"""
    transaction = {"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}  # Без десятичной части

    result = get_amount_in_rub(transaction)
    assert result == 100.0


def test_get_amount_in_rub_decimal_amount() -> None:
    """Тест транзакции с десятичной суммой"""
    transaction = {"operationAmount": {"amount": "123.45", "currency": {"code": "RUB"}}}

    result = get_amount_in_rub(transaction)
    assert result == 123.45


# Параметризованные тесты для лучшего покрытия
@pytest.mark.parametrize(
    "amount,currency,expected_rate,expected_result",
    [
        (100.0, "RUB", None, 100.0),  # RUB - без конвертации
        (50.0, "USD", 91.45, 4572.5),  # USD - с конвертацией
        (200.0, "EUR", 99.50, 19900.0),  # EUR - с конвертацией
    ],
)
@patch("src.external_api.get_exchange_rate")
def test_convert_to_rub_parametrized(
    mock_get_rate: MagicMock, amount: float, currency: str, expected_rate: float, expected_result: float
) -> None:
    """Параметризованный тест для convert_to_rub"""
    if currency != "RUB":
        mock_get_rate.return_value = expected_rate

    result = convert_to_rub(amount, currency)

    if currency != "RUB":
        mock_get_rate.assert_called_once_with(currency)

    assert result == expected_result


# тесты для get_amount_in_rub - убираем проверки обязательных полей
@pytest.mark.parametrize(
    "transaction,expected_amount",
    [
        # RUB транзакция
        ({"operationAmount": {"amount": "100.00", "currency": {"code": "RUB"}}}, 100.00),
        # GBP транзакция (неизвестная валюта)
        ({"operationAmount": {"amount": "50.00", "currency": {"code": "GBP"}}}, 50.00),
        # JPY транзакция (неизвестная валюта)
        ({"operationAmount": {"amount": "200.00", "currency": {"code": "JPY"}}}, 200.00),
        # Транзакция без currency (использует RUB по умолчанию)
        ({"operationAmount": {"amount": "100.00"}}, 100.00),
        # Транзакция с пустым currency (использует RUB по умолчанию)
        ({"operationAmount": {"amount": "100.00", "currency": {}}}, 100.00),
    ],
)
def test_get_amount_in_rub_success_cases(transaction: dict, expected_amount: float) -> None:
    """Параметризованный тест для успешных случаев get_amount_in_rub"""
    result = get_amount_in_rub(transaction)
    assert result == expected_amount


# Тесты для edge cases
@patch("src.external_api.convert_to_rub")
def test_get_amount_in_rub_zero_amount(mock_convert: MagicMock) -> None:
    """Тест транзакции с нулевой суммой"""
    mock_convert.return_value = 0.0

    transaction = {"operationAmount": {"amount": "0.00", "currency": {"code": "USD"}}}

    result = get_amount_in_rub(transaction)
    assert result == 0.0
    mock_convert.assert_called_once_with(0.0, "USD")


@patch("src.external_api.convert_to_rub")
def test_get_amount_in_rub_large_amount(mock_convert: MagicMock) -> None:
    """Тест транзакции с большой суммой"""
    mock_convert.return_value = 9145000.0

    transaction = {"operationAmount": {"amount": "100000.00", "currency": {"code": "USD"}}}

    result = get_amount_in_rub(transaction)
    assert result == 9145000.0
    mock_convert.assert_called_once_with(100000.0, "USD")


# ТЕСТ ДЛЯ ПРОВЕРКИ ТРАНЗАКЦИИ БЕЗ operationAmount
def test_get_amount_in_rub_no_operation_amount() -> None:
    """Тест как обрабатывается транзакция без operationAmount в текущей реализации"""
    transaction = {"id": 1, "description": "Test"}

    result = get_amount_in_rub(transaction)
    assert result == 0.0


# ТЕСТ ДЛЯ ПРОВЕРКИ ТРАНЗАКЦИИ БЕЗ amount
def test_get_amount_in_rub_no_amount() -> None:
    """Тест как обрабатывается транзакция без amount в текущей реализации"""
    transaction = {"operationAmount": {"currency": {"code": "RUB"}}}

    result = get_amount_in_rub(transaction)
    assert result == 0.0


# ТЕСТ ДЛЯ ПРОВЕРКИ ТРАНЗАКЦИИ БЕЗ currency
def test_get_amount_in_rub_no_currency() -> None:
    """Тест как обрабатывается транзакция без currency в текущей реализации"""
    transaction = {"operationAmount": {"amount": "100.00"}}

    result = get_amount_in_rub(transaction)
    assert result == 100.00
