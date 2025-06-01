import pytest
from src.masks import get_mask_card_number, get_mask_account

def test_get_mask_card_number():
    assert get_mask_card_number('7000792289606361') == '7000 79** **** 6361'
    assert get_mask_card_number('1234567890123456') == '1234 56** **** 3456'
    # Тест с пробелами
    assert get_mask_card_number('7000 79 22 89 60 63 61') == '7000 79** **** 6361'
    # Тест с некорректной длиной (должен поднять исключение)
    with pytest.raises(ValueError):
        get_mask_card_number('123456789012345')  # 15 цифр

def test_get_mask_account():
    assert get_mask_account('73654108430135874305') == '**4305'
    assert get_mask_account('12345678901234567890') == '**7890'
    # Тест с пробелами
    assert get_mask_account('1234 5678 9012 3456 7890') == '**7890'
    # Тест с некорректной длиной (меньше 20)
    with pytest.raises(ValueError):
        get_mask_account('1234567890')  # 10 цифр