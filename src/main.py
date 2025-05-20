from masks import get_mask_card_number, get_mask_account
from widget import mask_account_card, get_date
from processing import filter_by_state, sort_by_date


def main():
    # Запрос у пользователя данных для номера карты
    card_number_input = input("Введите номер карты (16 цифр): ").strip()
    if not card_number_input.isdigit() or len(card_number_input) != 16:
        print("Некорректный номер карты. Ожидалось 16 цифр.")
        return
    card_number = int(card_number_input)

    # Запрос у пользователя данных для номера счета
    account_number_input = input("Введите номер счета (число): ").strip()
    if not account_number_input.isdigit():
        print("Некорректный номер счета.")
        return
    account_number = int(account_number_input)

    # Ввод строки с информацией о карте
    info_string_card = input("Введите строку с информацией о карте: ").strip()
    # Ввод строки с информацией о счете
    info_string_account = input("Введите строку с информацией о счете: ").strip()

    # Ввод даты в формате ГГГГ-ММ-ДД
    date_str = input("Введите дату в формате ГГГГ-ММ-ДД: ").strip()

    # Использование функций из masks.py
    masked_card = get_mask_card_number(card_number)
    masked_account = get_mask_account(account_number)
    print(f"\nМаскированный номер карты: {masked_card}")
    print(f"Маскированный номер счета: {masked_account}")

    # Обработка строк
    masked_info_card = mask_account_card(info_string_card)
    masked_info_account = mask_account_card(info_string_account)
    print(f"\nМаскированная строка карты: {masked_info_card}")
    print(f"Маскированная строка счета: {masked_info_account}")

    # Форматирование даты
    formatted_date = get_date(date_str)
    print(f"\nФорматированная дата: {formatted_date}")

    # Демонстрация обработки списка записей
    # Можно расширить, добавив ввод данных о транзакциях
    # Для простоты оставить пример фиксированного списка
    records = [
        {'date': '2023-10-15', 'amount': 5000, 'state': 'EXECUTED'},
        {'date': '2023-09-10', 'amount': 1500, 'state': 'PENDING'},
        {'date': '2023-08-01', 'amount': 2000, 'state': 'EXECUTED'},
    ]

    # Фильтрация по состоянию
    executed_records = filter_by_state(records)
    print("\nЗаписи со статусом EXECUTED:")
    for record in executed_records:
        print(record)

    # Сортировка по дате
    sorted_records = sort_by_date(records)
    print("\nОтсортированные записи по дате:")
    for record in sorted_records:
        print(record)


if __name__ == "__main__":
    main()