from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """
    Обрабатывает строку с типом и номером карты или счета и возвращает маскированную строку.

    Args:
        info: Строка в формате "Тип номер" (например, "Visa 1234567890123456" или "Счет 12345678901234567890")

    Returns:
        Маскированная строка с типом и замаскированным номером

    Raises:
        ValueError: Если строка пустая, имеет неверный формат или номер невалиден
    """
    # Проверка на пустую строку
    if not info or not info.strip():
        raise ValueError("Строка не может быть пустой")

    # Разделяем строку по пробелам
    parts = info.strip().split()

    # Проверка, что есть хотя бы два элемента (тип и номер)
    if len(parts) < 2:
        raise ValueError("Некорректный формат строки")

    # Определяем тип (последний элемент)
    last_part = parts[-1]

    # Проверка, что последний элемент — это номер карты или счета
    if last_part.isdigit():
        number = last_part
        # Формируем название типа (остальные части)
        type_name = " ".join(parts[:-1])

        if type_name.lower() == "счет":
            # Маскируем счет
            masked_number = get_mask_account(number)
            return f"{type_name} {masked_number}"
        else:
            # Маскируем карту
            masked_number = get_mask_card_number(number)
            return f"{type_name} {masked_number}"
    else:
        # В случае, если формат не соответствует ожиданиям
        raise ValueError("Некорректный формат строки")


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формате "YYYY-MM-DDTHH:MM:SS.ffffff" в формат "ДД.ММ.ГГГГ".

    Args:
        date_str: Строка с датой в ISO формате

    Returns:
        Дата в формате "ДД.ММ.ГГГГ"

    Raises:
        ValueError: Если строка не является валидной датой в ISO формате
    """
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%d.%m.%Y")
