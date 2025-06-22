def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате: XXXX XX** **** XXXX

    Args:
        card_number: Номер банковской карты (16 цифр, пробелы игнорируются)

    Returns:
        Маскированный номер карты

    Raises:
        ValueError: Если номер карты содержит не только цифры или имеет неверную длину
    """
    # Убираем все пробелы, если есть
    digits = card_number.replace(" ", "")

    # Проверка, что строка содержит только цифры
    if not digits.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

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

    Args:
        account_number: Номер банковского счета (минимум 20 цифр, пробелы игнорируются)

    Returns:
        Маскированный номер счета

    Raises:
        ValueError: Если номер счета содержит не только цифры или имеет неверную длину
    """
    # Убираем все пробелы, если есть
    digits = account_number.replace(" ", "")

    # Проверка, что строка содержит только цифры
    if not digits.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    # Проверка длины номера счета
    if len(digits) < 20:
        raise ValueError("Номер счета должен содержать 20 цифр")

    last_four = digits[-4:]
    masked_account = f"**{last_four}"
    return masked_account
