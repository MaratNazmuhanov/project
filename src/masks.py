import logging

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты в формате: XXXX XX** **** XXXX
    """
    logger.debug("Начало маскирования номера карты: %s", card_number)

    digits = card_number.replace(" ", "")
    logger.debug("Номер карты после удаления пробелов: %s", digits)

    if not digits.isdigit():
        error_msg = "Номер карты должен содержать только цифры"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if len(digits) != 16:
        error_msg = "Номер карты должен содержать 16 цифр"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Распределяем части
    first_part = digits[:4]  # первые 4 цифры
    second_part = digits[4:6]  # 5-6
    # Средняя часть маскируется: 2 звезды, 4 звездочки
    middle_mask = "** ****"
    # Последние 4 цифры
    last_part = digits[-4:]

    # Формируем строку
    masked_card = f"{first_part} {second_part}{middle_mask} {last_part}"

    logger.info("Номер карты успешно замаскирован: %s", masked_card)
    return masked_card


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета в формате: **XXXX
    """
    logger.debug("Начало маскирования номера счета: %s", account_number)

    digits = account_number.replace(" ", "")
    logger.debug("Номер счета после удаления пробелов: %s", digits)

    if not digits.isdigit():
        error_msg = "Номер счета должен содержать только цифры"
        logger.error(error_msg)
        raise ValueError(error_msg)

    if len(digits) < 20:
        error_msg = "Номер счета должен содержать 20 цифр"
        logger.error(error_msg)
        raise ValueError(error_msg)

    last_four = digits[-4:]
    masked_account = f"**{last_four}"

    logger.info("Номер счета успешно замаскирован: %s", masked_account)
    return masked_account
