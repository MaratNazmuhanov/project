# 🏦 Банковское приложение

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Poetry](https://img.shields.io/badge/Poetry-dependency%20management-blue.svg)](https://python-poetry.org)
[![MyPy](https://img.shields.io/badge/MyPy-typed-green.svg)](http://mypy-lang.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Tests](https://img.shields.io/badge/tests-109%20passed-green.svg)](https://pytest.org)

Профессиональный проект для работы с банковскими данными с полной типизацией, комплексным тестированием и автоматизированной проверкой качества кода.

## ✨ Возможности

- 🔒 **Маскировка данных**: Безопасное скрытие номеров карт и счетов
- 📅 **Обработка дат**: Форматирование дат в удобочитаемый вид
- 🔍 **Фильтрация и сортировка**: Обработка банковских транзакций
- 🔍 **Фильтрация транзакций и генерация номеров карт
- 🧪 **Комплексное тестирование**: тесты с фикстурами и параметризацией
- 🔧 **Статическая типизация**: Полная поддержка MyPy
- 📋 **Качество кода**: Автоматизированные проверки с Black, isort, flake8

## 📁 Структура проекта

```
test_poetry/
├── src/                          # Исходный код
│   ├── masks.py                  # Маскировка номеров карт и счетов
│   ├── widget.py                 # Обработка строк и форматирование дат
│   ├── generators.py             # Генерация данных
│   ├── processing.py             # Фильтрация и сортировка данных
│   └── main.py                   # Пример использования
├── tests/                        # Тесты
│   ├── conftest.py              # Фикстуры pytest (15+ фикстур)
│   ├── test_masks.py            # Тесты маскировки (30+ тестов)
│   ├── test_widget.py           # Тесты виджетов (25+ тестов)
│   ├── test_generators.py       # Тесты генераторов
│   └── test_processing.py       # Тесты обработки (50+ тестов)
├── pyproject.toml               # Конфигурация Poetry и инструментов
├── lint.py                      # Скрипт проверки качества кода
└── README.md                    # Документация
```

## 🚀 Быстрый старт

### Установка зависимостей

```bash
# Установка Poetry (если не установлен)
pip install poetry

# Установка зависимостей проекта
poetry install

# Установка инструментов разработки
poetry install --with lint
```

### Запуск примера

```bash
  python src/main.py
```

## 📖 Примеры использования

### Маскировка номеров карт

```python
from src.masks import get_mask_card_number

# Маскировка номера карты
card_number = "7000792289606361"
masked = get_mask_card_number(card_number)
print(masked)  # 7000 79** **** 6361
```

### Маскировка номеров счетов

```python
from src.masks import get_mask_account

# Маскировка номера счета
account_number = "73654108430135874305"
masked = get_mask_account(account_number)
print(masked)  # **4305
```

### Обработка строк с информацией о картах/счетах

```python
from src.widget import mask_account_card, get_date

# Маскировка строки с картой
card_info = "Visa Platinum 7000792289606361"
masked_card = mask_account_card(card_info)
print(masked_card)  # Visa Platinum 7000 79** **** 6361

# Маскировка строки со счетом
account_info = "Счет 73654108430135874305"
masked_account = mask_account_card(account_info)
print(masked_account)  # Счет **4305

# Форматирование даты
date_str = "2024-03-11T02:26:18.671407"
formatted_date = get_date(date_str)
print(formatted_date)  # 11.03.2024
```

### Фильтрация и сортировка данных

```python
from src.processing import filter_by_state, sort_by_date

# Пример данных
transactions = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2023-10-01T12:00:00'},
    {'id': 2, 'state': 'CANCELED', 'date': '2023-10-02T15:30:00'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2023-09-30T09:15:00'},
]

# Фильтрация по статусу
executed = filter_by_state(transactions, 'EXECUTED')
print(f"Выполненных транзакций: {len(executed)}")

# Сортировка по дате (по убыванию)
sorted_desc = sort_by_date(transactions, reverse=True)
print("Последняя транзакция:", sorted_desc[0]['date'])
```

### Генераторы финансовых транзакций

```python
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Список транзакций
transactions = [
    {"amount": 100.0, "currency": "USD", "description": "Обед"},
    {"amount": 50.0, "currency": "EUR", "description": "Кофе"},
    {"amount": 200.0, "currency": "USD", "description": "Ужин"},
    {"amount": 75.5, "currency": "GBP", "description": "Кино"}
]

# Фильтрация транзакций по доллару
usd_transactions = filter_by_currency(transactions, "USD")
for transaction in usd_transactions:
    print(f"Долларовая транзакция: {transaction['description']}")

# Генерация описаний
descriptions = transaction_descriptions(transactions)
for desc in descriptions:
    print(desc)

# Создание карты
card_gen = card_number_generator(1234, 5678)
for card_num in card_gen:
    print(f"Номер карты: {card_num}")

```

## 🧪 Тестирование

Проект включает комплексное тестирование с использованием современных подходов:

### Особенности тестов

- **109 тестов** с полным покрытием функциональности
- **15+ фикстур** для переиспользования тестовых данных
- **Параметризация** для тестирования множественных сценариев
- **Типизированные тесты** с полной поддержкой MyPy

### Запуск тестов

```bash
# Запуск всех тестов
pytest tests/

# Запуск с подробным выводом
pytest tests/ -v

# Запуск конкретного модуля
pytest tests/test_masks.py

# Запуск с покрытием кода (если установлен pytest-cov)
pytest tests/ --cov=src
```

### Структура тестов

- **`test_masks.py`** - Тестирование маскировки (30+ тестов)
  - Валидные и невалидные номера карт
  - Валидные и невалидные номера счетов
  - Граничные случаи и обработка ошибок

- **`test_widget.py`** - Тестирование виджетов (25+ тестов)
  - Маскировка строк с картами и счетами
  - Форматирование дат
  - Обработка некорректных данных

- **`test_processing.py`** - Тестирование обработки данных (50+ тестов)
  - Фильтрация по различным состояниям
  - Сортировка по дате в разных направлениях
  - Комбинированные операции
  - Работа с пустыми данными и отсутствующими ключами

- **`test_generators.py`** - Тестирование генерации данных
  - Фильтрация по валюте
  - Генерация описания
  - Генерация номеров карт


## 🔧 Инструменты качества кода

Проект настроен с современными инструментами для поддержания высокого качества кода:

### Доступные инструменты

- **MyPy** - Статическая проверка типов
- **Black** - Автоматическое форматирование кода
- **isort** - Сортировка импортов
- **flake8** - Линтинг и проверка стиля кода

### Запуск проверок

```bash
# Проверка типов
poetry run mypy .

# Форматирование кода
poetry run black .

# Сортировка импортов
poetry run isort .

# Линтинг
poetry run flake8 .

# Запуск всех проверок одной командой
python lint.py
```

### Автоматизированная проверка

Скрипт `lint.py` запускает все проверки качества кода:

```bash
python lint.py
```

Результат:
```
🚀 Запуск проверки качества кода...

✅ MyPy (проверка типов) - OK
✅ Black (форматирование) - OK
✅ isort (сортировка импортов) - OK
✅ Flake8 (линтинг) - OK
✅ Pytest (тесты) - OK

🎉 Все проверки прошли успешно!
```

## 📋 Конфигурация

### Poetry (pyproject.toml)

Проект использует Poetry для управления зависимостями:

```toml
[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.group.dev.dependencies]
pytest = "^8.3.4"

[tool.poetry.group.lint.dependencies]
flake8 = "^7.2.0"
mypy = "^1.15.0"
black = "^25.1.0"
isort = "^6.0.1"
```

### Настройки инструментов

- **Black**: длина строки 119 символов
- **isort**: совместимость с Black
- **MyPy**: строгая проверка типов
- **flake8**: стандартные правила PEP 8

## 🏗️ Архитектура

### Принципы проекта

- **Типобезопасность**: Полная типизация с MyPy
- **Тестируемость**: Высокое покрытие тестами
- **Читаемость**: Чистый код с документацией
- **Надежность**: Обработка ошибок и граничных случаев
- **Масштабируемость**: Модульная архитектура

### Модули

1. **`masks.py`** - Базовые функции маскировки
   - `get_mask_card_number()` - маскировка номеров карт
   - `get_mask_account()` - маскировка номеров счетов

2. **`widget.py`** - Высокоуровневые функции обработки
   - `mask_account_card()` - обработка строк с картами/счетами
   - `get_date()` - форматирование дат

3. **`processing.py`** - Обработка данных
   - `filter_by_state()` - фильтрация по состоянию
   - `sort_by_date()` - сортировка по дате

4. **`generators.py`** - Обработка данных
   - `filter_by_currency` - Фильрация по валюте
   - `transaction_descriptions` - генерация описания
   - `card_number_generator` - генерация номера карты

## 🤝 Разработка

### Требования

- Python 3.8+
- Poetry для управления зависимостями
- Git для контроля версий

### Workflow разработки

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd test_poetry
   ```

2. **Установка зависимостей**
   ```bash
   poetry install --with lint
   ```

3. **Разработка**
   - Пишите код с типизацией
   - Добавляйте тесты для новой функциональности
   - Следуйте принципам чистого кода

4. **Проверка качества**
   ```bash
   python lint.py
   ```

5. **Коммит изменений**
   ```bash
   git add .
   git commit -m "feat: добавлена новая функциональность"
   ```

6. **Пуш в репозиторий**
   ```bash
   git push origin feature-branch
   ```

## 📊 Статистика проекта

- **Строк кода**: ~500+
- **Тестов**: 100+
- **Покрытие**: Высокое
- **Типизация**: 100%
- **Документация**: Полная

## 📄 Лицензия

Этот проект создан в образовательных целях.

---

**Создано с ❤️ для изучения современных практик Python разработки**