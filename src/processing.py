from typing import List, Dict


def filter_by_state(data: List[Dict], state: str = 'EXECUTED') -> List[Dict]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    filtered_list = [item for item in data if item.get('state') == state]
    return filtered_list


def sort_by_date(data: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует список словарей по дате в порядке убывания или возрастания.
    """
    # Используем сортировку по ключу 'date'
    sorted_list = sorted(
        data,
        key=lambda item: item.get('date', ''),
        reverse=reverse
    )
    return sorted_list