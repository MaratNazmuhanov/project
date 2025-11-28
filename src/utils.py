import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.
    """
    logger.debug("Начало загрузки транзакций из файла: %s", file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            logger.debug("Прочитано %d символов из файла", len(content))

            if not content:
                logger.warning("Файл %s пуст", file_path)
                return []

            data = json.loads(content)
            logger.debug("JSON успешно распарсен")

            if not isinstance(data, list):
                logger.warning("Данные в файле %s не являются списком", file_path)
                return []

            logger.info("Успешно загружено %d транзакций из файла %s", len(data), file_path)
            return data

    except FileNotFoundError:
        logger.error("Файл %s не найден", file_path)
        return []
    except json.JSONDecodeError as e:
        logger.error("Ошибка декодирования JSON в файле %s: %s", file_path, e)
        return []
    except PermissionError:
        logger.error("Нет прав на чтение файла %s", file_path)
        return []
    except Exception as e:
        logger.error("Неожиданная ошибка при загрузке файла %s: %s", file_path, e)
        return []
