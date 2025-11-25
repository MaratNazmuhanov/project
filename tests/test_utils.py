import json
import tempfile
from typing import Any
from unittest.mock import patch

from src.utils import load_transactions


class TestLoadTransactions:
    """Тесты для функции load_transactions"""

    def test_load_valid_transactions(self) -> None:
        """Тест загрузки валидных транзакций"""
        test_data = [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            }
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            file_path = f.name

        try:
            result = load_transactions(file_path)
            assert result == test_data
        finally:
            import os

            os.unlink(file_path)

    def test_load_empty_file(self) -> None:
        """Тест загрузки пустого файла"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            file_path = f.name

        try:
            result = load_transactions(file_path)
            assert result == []
        finally:
            import os

            os.unlink(file_path)

    def test_file_not_found(self) -> None:
        """Тест обработки отсутствующего файла"""
        result = load_transactions("nonexistent_file.json")
        assert result == []

    def test_invalid_json(self) -> None:
        """Тест обработки невалидного JSON"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            file_path = f.name

        try:
            result = load_transactions(file_path)
            assert result == []
        finally:
            import os

            os.unlink(file_path)

    def test_not_list_content(self) -> None:
        """Тест обработки файла с содержимым не-списком"""
        test_data = {"id": 1, "name": "test"}

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_data, f)
            file_path = f.name

        try:
            result = load_transactions(file_path)
            assert result == []
        finally:
            import os

            os.unlink(file_path)

    @patch("builtins.open", side_effect=PermissionError("No permission"))
    def test_permission_error(self, mock_file: Any) -> None:
        """Тест обработки ошибки прав доступа"""
        result = load_transactions("test.json")
        assert result == []
