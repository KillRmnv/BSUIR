# Лабораторная работа №2. Обучение классификатора сообщений Wit.ai системы NIKA

## Цель

Изучить принципы работы классификатора сообщений, приобрести навыки определения классов сообщений, выделения сущностей и признаков в них, формально специфицировать сценарий диалога.

## Задание

1. Описать сценарий диалога по предметной области "Наука" (8 сообщений)
2. Обучить классификатор сообщений Wit.ai на вопрос "Что такое ...?" для каждой формализованной сущности
3. Выделить классы и сущности сообщений, используемых в сценарии диалога
4. Составить отчёт с тестированием сценария диалога

## Предметная область

Предметная область "Наука" — систематизированная деятельность человека, направленная на развитие знаний о мире. Включает классы: естественные науки (физика, химия, биология), формальные науки (математика, информатика), прикладные науки (инженерия, медицина), гуманитарные науки, а также учёных, теории, гипотезы, законы, эксперименты, открытия, методы, учреждения, журналы.

## Сценарий диалога

| # | Роль | Сообщение | Класс (intent) | Сущность (entity) |
|---|------|-----------|----------------|-------------------|
| 1 | Студент | "Привет!" | `greeting` | — |
| 2 | Ника | "Привет! Я Ника. Задавайте вопросы о науке!" | `answer` | — |
| 3 | Студент | "Что такое физика?" | `about_entity` | `rrel_entity` → concept_physics |
| 4 | Ника | "Физика — наука о природных явлениях и строении материи" | `answer` | — |
| 5 | Студент | "Какие есть теории в области физики?" | `question_theories` | `rrel_entity` → concept_physics |
| 6 | Ника | "В области физики есть теория относительности и квантовая механика" | `answer` | — |
| 7 | Студент | "Кто сделал открытие пенициллина?" | `question_discovery` | `rrel_entity` → discovery_penicillin |
| 8 | Ника | "Пенициллин открыл Александр Флеминг" | `answer` | — |

## Классы сообщений (intents)

| Класс | Wit.ai ID | Описание |
|-------|-----------|----------|
| `concept_greeting_message` | `greeting` | Приветственное сообщение |
| `concept_message_about_entity` | `about_entity` | Вопрос "Что такое X?" |
| `concept_question_theories` | `question_theories` | Вопрос "Какие есть теории в области X?" |
| `concept_question_discovery` | `question_discovery` | Вопрос "Кто сделал открытие X?" |
| `concept_answer_message` | `answer` | Ответное сообщение |

## Сущности сообщений

| Класс | Wit.ai ID | Роль | Описание |
|-------|-----------|------|----------|
| `concept_entity` | `rrel_entity` | `rrel_entity` | Научная сущность (физика, химия, Ньютон и т.д.) |

## Формализация в базе знаний

### Классы сообщений

Каждый класс сообщений формализован в отдельном SCs-файле в каталоге `classification/messages/`.

Пример (`concept_message_about_entity.scs`):
```scs
concept_message_about_entity
<- sc_node_class;
<- concept_intent_possible_class;
=> nrel_main_idtf:
	[Сообщение о сущности] (* <- lang_ru;; *);
=> nrel_wit_ai_idtf:
	[about_entity];;
```

### Класс сущностей

Сущность формализована в `classification/entities/concept_entity.scs`:
```scs
concept_entity
<- sc_node_class;
<- concept_entity_possible_class;
=> nrel_main_idtf:
	[Сущность] (* <- lang_ru;; *);
=> nrel_wit_ai_idtf:
	[rrel_entity];
-> concept_science;
=> nrel_entity_possible_role:
    ..rrel_entity;;

..rrel_entity
<- sc_node_role_relation;
=> nrel_wit_ai_idtf:
	[rrel_entity];;
```

### Соответствие wit.ai и SCs

| Wit.ai | SCs-файл | nrel_wit_ai_idtf |
|--------|----------|-------------------|
| Intent `greeting` | `messages/concept_greeting_message.scs` | `[greeting]` |
| Intent `about_entity` | `messages/concept_message_about_entity.scs` | `[about_entity]` |
| Intent `question_theories` | `messages/concept_question_theories.scs` | `[question_theories]` |
| Intent `question_discovery` | `messages/concept_question_discovery.scs` | `[question_discovery]` |
| Entity `rrel_entity` | `entities/concept_entity.scs` | `[rrel_entity]` |
| Role `rrel_entity` | `entities/concept_entity.scs` | `[rrel_entity]` |

## Экспорт данных Wit.ai

Результат экспорта из Wit.ai в формате JSON:

```
classification/
├── app.json                      ← метаданные приложения
├── intents/
│   ├── about_entity.json         ← intent "Что такое X?"
│   ├── greeting.json             ← intent "Привет"
│   ├── question_discovery.json   ← intent "Кто сделал открытие X?"
│   └── question_theories.json    ← intent "Какие теории в области X?"
├── entities/
│   └── rrel_entity.json          ← entity с keywords (синонимы)
└── utterances/
    └── utterances-1.json         ← все обученные utterances
```

### Примеры utterances из экспорта

**Greeting:**
```json
{"text": "Привет", "intent": "greeting", "entities": [{"entity": "rrel_entity:rrel_entity", "body": "Привет"}]}
```

**About entity:**
```json
{"text": "Что такое физика", "intent": "about_entity", "entities": [{"entity": "rrel_entity:rrel_entity", "body": "физика"}]}
```

**Question theories:**
```json
{"text": "Какие теории есть в физике", "intent": "question_theories", "entities": [{"entity": "rrel_entity:rrel_entity", "body": "физике"}]}
```

**Question discovery:**
```json
{"text": "Кто открыл пенициллин", "intent": "question_discovery", "entities": [{"entity": "rrel_entity:rrel_entity", "body": "пенициллин"}]}
```

## Тестирование

### Тестовые сообщения

| Сообщение | Ожидаемый intent | Ожидаемая entity |
|-----------|------------------|------------------|
| "Привет" | `greeting` | — |
| "Здравствуйте" | `greeting` | — |
| "Что такое физика?" | `about_entity` | `rrel_entity` |
| "Что такое химия?" | `about_entity` | `rrel_entity` |
| "Какие теории есть в физике?" | `question_theories` | `rrel_entity` |
| "Кто открыл пенициллин?" | `question_discovery` | `rrel_entity` |

### Результаты тестирования

*(Заполнить после проверки в диалоговом окне NIKA)*

| Сообщение | Определён intent | Выделена entity | Результат |
|-----------|------------------|-----------------|-----------|
| "Привет" | ✓/✗ | — | ✓/✗ |
| "Здравствуйте" | ✓/✗ | — | ✓/✗ |
| "Что такое физика?" | ✓/✗ | ✓/✗ | ✓/✗ |
| "Что такое химия?" | ✓/✗ | ✓/✗ | ✓/✗ |
| "Какие теории есть в физике?" | ✓/✗ | ✓/✗ | ✓/✗ |
| "Кто открыл пенициллин?" | ✓/✗ | ✓/✗ | ✓/✗ |

## Структура файлов

```
classification/
├── WIT_AI_GUIDE.md
├── report.md
├── app.json                      ← метаданные приложения Wit.ai
├── intents/
│   ├── about_entity.json
│   ├── greeting.json
│   ├── question_discovery.json
│   └── question_theories.json
├── entities/
│   ├── concept_entity.scs        ← SCs: класс сущности
│   ├── rrel_entity.scs           ← SCs: роль сущности
│   └── rrel_entity.json          ← Wit.ai: entity с keywords
├── utterances/
│   └── utterances-1.json         ← обученные utterances
├── messages/
│   ├── concept_greeting_message.scs
│   ├── concept_message_about_entity.scs
│   ├── concept_question_theories.scs
│   ├── concept_question_discovery.scs
│   └── concept_answer_message.scs
├── phrases/
│   ├── concept_phrase_hello.scs
│   ├── concept_phrase_hello_2.scs
│   ├── concept_phrase_about_entity.scs
│   ├── concept_phrase_about_entity_2.scs
│   ├── concept_phrase_about_entity_template.scs
│   ├── concept_phrase_theories.scs
│   ├── concept_phrase_theories_template.scs
│   ├── concept_phrase_discovery.scs
│   └── concept_phrase_discovery_template.scs
└── rules/
    ├── lr_answer_greeting.scs
    ├── lr_answer_about_entity.scs
    ├── lr_answer_theories.scs
    ├── lr_answer_discovery.scs
    └── lr_classify_about.scs
```

## Выводы

1. Создано приложение классификации в Wit.ai для предметной области "Наука"
2. Обучены 4 класса сообщений (intent): greeting, about_entity, question_theories, question_discovery
3. Создана сущность rrel_entity с ролью rrel_entity для выделения научных понятий в сообщениях
4. Формализованы классы сообщений и сущность в базе знаний системы NIKA с помощью SCs-кода
5. Экспортированы данные из Wit.ai в формате JSON (intents, entities, utterances)
6. Все имена intent и entity в wit.ai точно совпадают со значениями nrel_wit_ai_idtf в SCs-файлах
