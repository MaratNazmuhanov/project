import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def sample_data():
    """Фикстура, возвращающая тестовые данные"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-10-01T12:00:00'},
        {'id': 2, 'state': 'CANCELED', 'date': '2023-10-02T15:30:00'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-09-30T09:15:00'},
        {'id': 4, 'state': 'PENDING', 'date': '2023-10-03T08:45:00'},
        {'id': 5, 'state': 'CANCELED', 'date': '2023-10-01T20:00:00'}
    ]

def test_filter_by_state_default(sample_data):
    """Тест фильтрации по состоянию по умолчанию ('EXECUTED')"""
    result = filter_by_state(sample_data)
    # Ожидаемые id: 1 и 3
    expected_ids = [1, 3]
    assert [item['id'] for item in result] == expected_ids
    # Все результаты имеют 'state' == 'EXECUTED'
    assert all(item['state'] == 'EXECUTED' for item in result)

def test_filter_by_state_specific(sample_data):
    """Тест фильтрации по конкретному статусу ('CANCELED')"""
    result = filter_by_state(sample_data, 'CANCELED')
    expected_ids = [2, 5]
    assert [item['id'] for item in result] == expected_ids
    assert all(item['state'] == 'CANCELED' for item in result)

def test_filter_by_state_no_matches(sample_data):
    """Тест, когда фильтр не находит совпадений"""
    result = filter_by_state(sample_data, 'FAILED')
    assert result == []

def test_sort_by_date_desc(sample_data):
    """Тест сортировки по дате по убыванию (по умолчанию)"""
    sorted_data = sort_by_date(sample_data)
    # Первый элемент должен иметь самую позднюю дату
    assert sorted_data[0]['date'] == '2023-10-03T08:45:00'
    # Последний - самую раннюю
    assert sorted_data[-1]['date'] == '2023-09-30T09:15:00'

def test_sort_by_date_asc(sample_data):
    """Тест сортировки по дате по возрастанию"""
    sorted_data = sort_by_date(sample_data, reverse=False)
    # Первый элемент - самая ранняя дата
    assert sorted_data[0]['date'] == '2023-09-30T09:15:00'
    # Последний - самая поздняя
    assert sorted_data[-1]['date'] == '2023-10-03T08:45:00'

def test_sort_with_empty_list():
    """Тест сортировки пустого списка"""
    result = sort_by_date([])
    assert result == []

def test_filter_with_empty_list():
    """Тест фильтрации пустого списка"""
    result = filter_by_state([])
    assert result == []

def test_filter_with_missing_key():
    """Тест фильтрации, если у элементов отсутствует ключ 'state'"""
    data = [{'id': 1}, {'id': 2, 'state': 'EXECUTED'}]
    result = filter_by_state(data)
    # только второй элемент должен остаться
    assert result == [{'id': 2, 'state': 'EXECUTED'}]