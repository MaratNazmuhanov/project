import json
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []

            data = json.loads(content)

            if not isinstance(data, list):
                return []

            return data

    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return []
