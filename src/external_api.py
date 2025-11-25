import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv  # type: ignore

# Загружаем переменные окружения один раз при импорте
load_dotenv()

# Константы модуля
_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
_BASE_URL = "https://api.apilayer.com/exchangerates_data"


def get_exchange_rate(from_currency: str, to_currency: str = "RUB") -> Optional[float]:
    """
    Получает текущий курс обмена валют.
    """
    if not _API_KEY:
        print("⚠️  API ключ не найден. Убедитесь, что файл .env содержит EXCHANGE_RATE_API_KEY")
        return None

    url = f"{_BASE_URL}/latest"
    params = {"base": from_currency, "symbols": to_currency}
    headers = {"apikey": _API_KEY}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.status_code == 401:
            print("❌ Ошибка авторизации API. Проверьте API ключ.")
            return None
        elif response.status_code == 429:
            print("❌ Превышен лимит запросов API.")
            return None

        response.raise_for_status()

        data: Dict[str, Any] = response.json()

        if not data.get("success", True):
            print(f"❌ Ошибка API: {data.get('error', {}).get('info', 'Unknown error')}")
            return None

        rates = data.get("rates", {})
        rate = rates.get(to_currency)

        if rate is None:
            return None

        return float(rate)

    except requests.exceptions.Timeout:
        print("Таймаут при запросе к API")
        return None
    except requests.exceptions.ConnectionError:
        print("Ошибка соединения с API")
        return None
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Ошибка при получении курса валют: {e}")
        return None


def convert_to_rub(amount: float, from_currency: str) -> Optional[float]:
    """
    Конвертирует сумму в рубли.
    """
    if from_currency == "RUB":
        return amount

    rate = get_exchange_rate(from_currency)
    if rate is None:
        return None

    return amount * rate


def get_amount_in_rub(transaction: dict) -> float:
    """
    Возвращает сумму транзакции в рублях.
    """
    try:
        # Получаем данные о сумме и валюте
        operation_amount = transaction.get("operationAmount", {})
        amount_str = operation_amount.get("amount", "0")
        currency_info = operation_amount.get("currency", {})
        currency_code = currency_info.get("code", "RUB")

        # Преобразуем сумму в float
        amount = float(amount_str)

        # Если валюта уже рубли, возвращаем как есть
        if currency_code == "RUB":
            return amount

        # Конвертируем USD и EUR
        if currency_code in ["USD", "EUR"]:
            print(f"Конвертируем {amount} {currency_code} в RUB...")
            converted_amount = convert_to_rub(amount, currency_code)
            if converted_amount is not None:
                print(f"Успешно: {amount} {currency_code} = {converted_amount:.2f} RUB")
                return converted_amount
            else:
                raise ValueError(
                    f"Не удалось конвертировать {currency_code} в RUB. Проверьте API ключ и подключение к интернету."
                )
        else:
            # Для других валют возвращаем исходную сумму
            print(f"Неизвестная валюта {currency_code}, возвращаем исходную сумму")
            return amount

    except (ValueError, TypeError, KeyError) as e:
        raise ValueError(f"Ошибка при обработке транзакции: {e}")
