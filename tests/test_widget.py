import pytest
from src.widget import mask_account_card, get_date

def test_mask_account_card_cards():
    assert mask_account_card("Visa Platinum 7000792289606361") == "Visa Platinum 7000 79** **** 6361"
    assert mask_account_card("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"
    assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"

def test_mask_account_card_schemes():
    assert mask_account_card("Счет 73654108430135874305") == "Счет **4305"
    assert mask_account_card("Счет 64686473678894779589") == "Счет **9589"

def test_mask_account_card_invalid_format():
    with pytest.raises(ValueError):
        mask_account_card("Некорректная строка без номера")

def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("2021-12-25T15:45:00.000000") == "25.12.2021"