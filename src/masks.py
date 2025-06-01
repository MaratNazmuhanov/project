def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате: XXXX XX** **** XXXX
    """
    # Убираем все пробелы, если есть
    digits = card_number.replace(" ", "")

    # Проверка длины номера карты
    if len(digits) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Распределяем части
    first_part = digits[:4]  # первые 4 цифры
    second_part = digits[4:6]  # 5-6
    # Средняя часть маскируется: 2 звезды, 4 звездочки
    middle_mask = "** ****"
    # Последние 4 цифры
    last_part = digits[-4:]

    # Формируем строку
    masked_card = f"{first_part} {second_part}{middle_mask} {last_part}"
    return masked_card


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате: **XXXX
    """
    # Убираем все пробелы, если есть
    digits = account_number.replace(" ", "")

    # Проверка длины номера счета
    if len(digits) < 20:
        raise ValueError("Номер счета должен содержать 20 цифры")

    last_four = digits[-4:]
    masked_account = f"**{last_four}"
    return masked_account