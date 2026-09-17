# Гайд по Wit.ai для лабораторных 2 и 3

## 1. Создание приложения

1. Перейти на [wit.ai](https://wit.ai/)
2. Войти через Facebook
3. Создать новое приложение:
   - **Name**: `Science` (или любое другое)
   - **Language**: `Russian`
   - **Privacy**: `Private`

## 2. Создание Intents (классов сообщений)

Перейти во вкладку **Management → Intents** и создать 4 intent'а:

| Intent | Описание |
|--------|----------|
| `greeting` | Приветственное сообщение |
| `about_entity` | Вопрос "Что такое X?" |
| `question_theories` | Вопрос "Какие есть теории в области X?" |
| `question_discovery` | Вопрос "Кто сделал открытие X?" |

**Важно**: имена intent'ов должны **точно совпадать** со значениями `nrel_wit_ai_idtf` в SCs-файлах (`classification/messages/*.scs`).

## 3. Создание Entities (сущностей)

Перейти во вкладку **Entities** и создать одну сущность:

| Entity | Описание |
|--------|----------|
| `rrel_entity` | Научная сущность (физика, химия, Ньютон и т.д.) |

Сущность и роль в wit.ai имеют одно имя — `rrel_entity`. Это описано в SCs-файле `entities/concept_entity.scs`.

## 4. Обучение классификатора

Перейти во вкладку **Understanding** и вводить сообщения для обучения.

### Группа 1: Приветствия (intent: `greeting`)
```
Привет
Здравствуйте
Добрый день
Приветствую
Хай
Йо
```
Для каждого сообщения выбрать intent `greeting`.

### Группа 2: Вопросы "Что такое?" (intent: `about_entity`, entity: `entity`)
```
Что такое физика
Что такое химия
Что такое биология
Что такое математика
Что такое информатика
Что такое инженерия
Что такое теория относительности
Что такое квантовая механика
Что такое теория эволюции
Что такое периодический закон
Что такое закон тяготения
Что такое модель атома
Что такое научная конференция
Что такое диссертация
Что такое парадигма
```
Для каждого сообщения:
1. Выбрать intent `about_entity`
2. Выделить сущность (например, слово "физика")

### Группа 3: Вопросы о теориях (intent: `question_theories`, entity: `entity`)
```
Какие есть теории в области физики
Какие теории есть в физике
Какие существуют теории в области химии
Перечисли теории в области биологии
Какие теории известны в математике
```
Для каждого сообщения:
1. Выбрать intent `question_theories`
2. Выделить сущность (область науки)

### Группа 4: Вопросы об открытиях (intent: `question_discovery`, entity: `entity`)
```
Кто сделал открытие пенициллина
Кто открыл пенициллин
Кто сделал открытие структуры ДНК
Кто открыл закон тяготения
Кто сделал открытие электромагнитной индукции
Кто создал периодическую таблицу
```
Для каждого сообщения:
1. Выбрать intent `question_discovery`
2. Выделить сущность (объект открытия)

## 5. Проверка

После обучения ввести тестовые сообщения в поле **Utterance** и проверить:
- Определяется ли intent правильно
- Выделяется ли entity

Тестовые сообщения:
```
Привет
Здравствуйте
Что такое физика
Что такое Ньютон
Какие теории есть в химии
Кто открыл пенициллин
```

## 6. Получение токена

Перейти в **Settings** → скопировать **Server Access Token**.

Записать токен в файл `nika.ini`:
```ini
[wit-ai]
server_token = ВАШ_ТОКЕН
url = https://api.wit.ai/message
```

## 7. Экспорт данных

1. Перейти в **Settings → Export**
2. Скачать ZIP-архив
3. Распаковать в корень `classification/`

### Структура экспорта

```
classification/
├── app.json                      ← метаданные приложения (app_id, access_token, lang)
├── intents/
│   ├── about_entity.json         ← intent +史料
│   ├── greeting.json
│   ├── question_discovery.json
│   └── question_theories.json
├── entities/
│   └── rrel_entity.json          ← entity с keywords (синонимы)
└── utterances/
    └── utterances-1.json         ← все обученные utterances
```

**Важно**: файлы экспорта (.json) и SCs-файлы (.scs) сосуществуют в одной директории — они дополняют друг друга.

### Что в экспорте

| Файл | Содержание |
|------|------------|
| `app.json` | Метаданные приложения: `app_id`, `access_token`, `lang` |
| `intents/*.json` | Описания intents + stories (цепочки сообщений) |
| `entities/*.json` | Описания entities + keywords (синонимы для распознавания) |
| `utterances/*.json` | Все обученные utterances: `{text, intent, entities}` |

## 8. Соответствие wit.ai и SCs

| Wit.ai | SCs-файл | Значение |
|--------|----------|----------|
| Intent `greeting` | `messages/concept_greeting_message.scs` | `nrel_wit_ai_idtf: [greeting]` |
| Intent `about_entity` | `messages/concept_message_about_entity.scs` | `nrel_wit_ai_idtf: [about_entity]` |
| Intent `question_theories` | `messages/concept_question_theories.scs` | `nrel_wit_ai_idtf: [question_theories]` |
| Intent `question_discovery` | `messages/concept_question_discovery.scs` | `nrel_wit_ai_idtf: [question_discovery]` |
| Entity `rrel_entity` | `entities/concept_entity.scs` | `nrel_wit_ai_idtf: [rrel_entity]` |

**Критически важно**: содержимое `nrel_wit_ai_idtf` в SCs **должно точно совпадать** с именами в wit.ai. Даже один символ расхождения — и NIKA не сможет классифицировать сообщения.
