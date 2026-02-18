#!/usr/bin/env python3
"""Скрипт для запуска приложения."""
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from word_collocation_dict.main import main

if __name__ == '__main__':
    main()
