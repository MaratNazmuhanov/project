from .masks import get_mask_card_number, get_mask_account
from datetime import datetime


def mask_account_card(info: str) -> str:
    """
    Обрабатывает строку с типом и номером карты или счета и возвращает маскированную строку.
    """
    # Разделяем строку по пробелам
    parts = info.strip().split()

    # Определяем тип (последний элемент)
    last_part = parts[-1]

    # Проверка, что последний элемент — это номер карты или счета
    if last_part.isdigit():
        number = last_part
        # Формируем название типа (остальные части)
        type_name = ' '.join(parts[:-1])

        if type_name.lower() == 'счет':
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
    """
    dt = datetime.fromisoformat(date_str)
    return dt.strftime("%d.%m.%Y")