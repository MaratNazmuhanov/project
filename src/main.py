from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date


def main() -> None:
    print("Добро пожаловать! Эта программа поможет вам маскировать номера карт и счетов, а также работать с датами и "
          "транзакциями.")

    # Запрос номера карты
    card_number_input = input("Введите номер карты (16 цифр): ").strip()
    while not (card_number_input.isdigit() and len(card_number_input) == 16):
        print("Некорректный ввод. Пожалуйста, введите 16 цифр.")
        card_number_input = input("Введите номер карты (16 цифр): ").strip()

    # Запрос номера счета
    account_number_input = input("Введите номер счета (20 цифр): ").strip()
    while not (account_number_input.isdigit() and len(account_number_input) == 20):
        print("Некорректный ввод. Пожалуйста, введите 20 цифр.")
        account_number_input = input("Введите номер счета (20 цифр): ").strip()

    # Запрос строки с информацией о карте
    info_string_card = input("Введите строку с информацией о карте (например: 'Visa 1234 56** **** 7890'): ").strip()

    # Запрос строки с информацией о счете
    info_string_account = input("Введите строку с информацией о счете (например: 'счет 1234 56** **** 7890'): ").strip()

    # Запрос даты
    date_str = input("Введите дату в формате ГГГГ-ММ-ДД (например: 2023-10-15): ").strip()

    # Маскировка номера карты и счета
    masked_card = get_mask_card_number(card_number_input)
    masked_account = get_mask_account(account_number_input)
    print(f"\nМаскированный номер карты: {masked_card}")
    print(f"Маскированный номер счета: {masked_account}")

    # Обработка строк с информацией
    try:
        masked_info_card = mask_account_card(info_string_card)
        print(f"\nМаскированная строка о карте: {masked_info_card}")
    except ValueError as e:
        print(f"Ошибка при обработке строки о карте: {e}")

    try:
        masked_info_account = mask_account_card(info_string_account)
        print(f"\nМаскированная строка о счете: {masked_info_account}")
    except ValueError as e:
        print(f"Ошибка при обработке строки о счете: {e}")

    # Форматирование даты
    try:
        formatted_date = get_date(date_str)
        print(f"\nФорматированная дата: {formatted_date}")
    except Exception as e:
        print(f"Ошибка при форматировании даты: {e}")

    # Пример работы с транзакциями
    transactions = [
        {'date': '2023-10-15', 'amount': 5000, 'state': 'EXECUTED'},
        {'date': '2023-09-10', 'amount': 1500, 'state': 'PENDING'},
        {'date': '2023-08-01', 'amount': 2000, 'state': 'EXECUTED'},
    ]

    # Фильтрация по состоянию
    executed_transactions = filter_by_state(transactions)
    print("\nТранзакции со статусом EXECUTED:")
    for t in executed_transactions:
        print(t)

    # Сортировка по дате
    sorted_transactions = sort_by_date(transactions)
    print("\nОтсортированные транзакции по дате (по убыванию):")
    for t in sorted_transactions:
        print(t)

if __name__ == "__main__":
    main()