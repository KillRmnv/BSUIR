# Code Style — EYAZIS/2_2

## Импорты

**Все импорты — только вверху файла.** Никаких lazy imports внутри функций.

```python
# ✅ Правильно
import os
from flask import Flask, jsonify
from services import translation_service
from translator.nmt_engine import translate_text

# ❌ Неправильно
def my_func():
    from translator.nmt_engine import translate_text  # НЕЛЬЗЯ
```

Исключения — только если импорт вызывает circular dependency, которого невозможно избежать.

## Controller Error Handling

Используй **errorhandler** на Blueprint, а не try/except в каждом endpoint.

```python
# ✅ Правильно
my_bp = Blueprint("my", __name__)

@my_bp.errorhandler(ValidationError)
def handle_validation(e):
    return jsonify({"error": e.message}), e.status_code

@my_bp.errorhandler(Exception)
def handle_generic(e):
    return jsonify({"error": "Internal server error"}), 500

@my_bp.route("/api/my-endpoint", methods=["POST"])
def api_my_endpoint():
    data = request.get_json(force=True)
    return jsonify(my_service.do_something(data.get("text", "")))
```

## Хранение данных

**PostgreSQL** — для метаданных, индексов, словарей (структурированные данные).
**S3 (MinIO)** — для больших текстов, файлов, бинарных данных.

Не храните тексты документов в `TEXT NOT NULL` колонках PostgreSQL.
Используйте `s3_key VARCHAR` для ссылки на объект в S3.

## Форматирование

- 4 пробела для отступов
- Максимальная длина строки: 120 символов
- Python 3.11+
- type hints для публичных функций
