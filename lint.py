#!/usr/bin/env python3
"""
Скрипт для запуска всех инструментов проверки качества кода.
"""

import subprocess
import sys
from typing import List, Tuple


def run_command(command: List[str], description: str) -> Tuple[bool, str]:
    """
    Запускает команду и возвращает результат.

    Args:
        command: Список аргументов команды
        description: Описание команды для вывода

    Returns:
        Кортеж (успех, вывод)
    """
    print(f"🔍 Запуск {description}...")
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"✅ {description} - OK")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Вывод: {e.stdout}")
        print(f"Ошибки: {e.stderr}")
        return False, e.stdout


def main() -> None:
    """Основная функция для запуска всех проверок."""
    print("🚀 Запуск проверки качества кода...\n")

    checks = [
        (["poetry", "run", "mypy", "."], "MyPy (проверка типов)"),
        (["poetry", "run", "black", "--check", "."], "Black (форматирование)"),
        (["poetry", "run", "isort", "--check-only", "."], "isort (сортировка импортов)"),
        (["poetry", "run", "flake8", "."], "Flake8 (линтинг)"),
        (["pytest", "tests/", "--tb=short"], "Pytest (тесты)"),
    ]

    all_passed = True
    results = []

    for command, description in checks:
        success, output = run_command(command, description)
        results.append((description, success))
        if not success:
            all_passed = False

    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ:")
    print("=" * 60)

    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description:<30} {status}")

    print("=" * 60)

    if all_passed:
        print("🎉 Все проверки прошли успешно!")
        sys.exit(0)
    else:
        print("💥 Некоторые проверки не прошли!")
        sys.exit(1)


if __name__ == "__main__":
    main()
