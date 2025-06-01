import pytest
from src.masks import get_mask_card_number, get_mask_account

@pytest.fixture(params=[
    ('7000792289606361', '7000 79** **** 6361'),
    ('1234567890123456', '1234 56** **** 3456'),
    ('7000 79 22 89 60 63 61', '7000 79** **** 6361'),
])
def valid_card_number_data(request):
    return request.param


@pytest.fixture(params=[
    ('123456789012345', ValueError),  # Некорректная длина
    ("invalid input", ValueError) # Некорректный тип
])
def invalid_card_number_data(request):
    return request.param


@pytest.fixture(params=[
    ('73654108430135874305', '**4305'),
    ('12345678901234567890', '**7890')
])
def valid_account_number_data(request):
    return request.param

@pytest.fixture
def invalid_account_number():
  return "invalid input"


def test_get_mask_card_number_valid(valid_card_number_data):
    input_number, expected_output = valid_card_number_data
    assert get_mask_card_number(input_number) == expected_output


def test_get_mask_card_number_invalid(invalid_card_number_data):
    input_number, expected_exception = invalid_card_number_data
    with pytest.raises(expected_exception):
        get_mask_card_number(input_number)


def test_get_mask_account_valid(valid_account_number_data):
    input_number, expected_output = valid_account_number_data
    assert get_mask_account(input_number) == expected_output


def test_get_mask_account_invalid(invalid_account_number):
  with pytest.raises(ValueError):
    get_mask_account(invalid_account_number)

@pytest.fixture
def sample_data():
    """возвращает тестовые данные"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2023-10-01T12:00:00'},
        {'id': 2, 'state': 'CANCELED', 'date': '2023-10-02T15:30:00'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2023-09-30T09:15:00'},
        {'id': 4, 'state': 'PENDING', 'date': '2023-10-03T08:45:00'},
        {'id': 5, 'state': 'CANCELED', 'date': '2023-10-01T20:00:00'}
    ]
