from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        data: Список словарей с данными транзакций
        state: Состояние для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        Отфильтрованный список словарей
    """
    filtered_list = [item for item in data if item.get("state") == state]
    return filtered_list


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по дате в порядке убывания или возрастания.

    Args:
        data: Список словарей с данными транзакций
        reverse: Порядок сортировки (True - по убыванию, False - по возрастанию)

    Returns:
        Отсортированный список словарей
    """
    # Используем сортировку по ключу 'date'
    sorted_list = sorted(data, key=lambda item: item.get("date", ""), reverse=reverse)
    return sorted_list
