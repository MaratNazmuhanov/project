from typing import List, Dict, Any


def filter_by_state(records: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """
    Возвращает новый список словарей, у которых ключ 'state' равен указанному значению.
    """
    return [record for record in records if record.get('state') == state]


def sort_by_date(records: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Возвращает новый список словарей, отсортированный по ключу 'date'.
    """
    # Используем функцию sorted() с ключом, преобразующим дату в формат, сравнимый по времени
    return sorted(records, key=lambda x: x.get('date', ''), reverse=descending)

