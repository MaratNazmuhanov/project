from masks import get_mask_account, get_mask_card_number


def mask_account_card(info_string: str) -> str | None:
    """Функция для бработки строки и возврата маскированного номера"""
    parts = info_string.split()
    number_str = parts[-1]
    account_type = " ".join(parts[:-1])
    number = int(number_str)
    if len(number_str) == 16:
        masked_number = get_mask_card_number(number)
        return f"{account_type} {masked_number}"
    elif len(number_str) > 4:
        masked_number = get_mask_account(number)
        return f"{account_type} {masked_number}"
    return None


def get_date(date_string: str) -> str:
    """Функция для форматирования даты"""
    year_str = date_string[0:4]
    month_str = date_string[5:7]
    day_str = date_string[8:10]
    formatted_date = f"{day_str}.{month_str}.{year_str}"
    return formatted_date
