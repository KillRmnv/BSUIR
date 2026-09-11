# Лаб. №3.1 — учётные записи в RAM (хеш + шифр)

Консольное приложение на чистом JDK (без зависимостей).
`username`/`note` — открытые; `password` — только соль+хеш (PBKDF2WithHmacSHA256);
номер карты — только шифротекст (AES/GCM). Plaintext секретов не хранится,
`char[]` затираются через `Arrays.fill` в `finally`.

## Сборка и запуск (Arch и Void одинаково)

Требуется только JDK 17+ (проверено на 21):

```bash
chmod +x run.sh
./run.sh              # интерактивное меню
./run.sh --build-only # только компиляция
./run.sh --demo       # 3 демо-записи + ожидание (для снятия дампов)
./run.sh --stress 10000  # нагрузка для раздела отчёта
```

Void Linux (QEMU VM):

```bash
sudo xbps-install -Su
sudo xbps-install openjdk21
./run.sh
```

## Три дампа для отчёта (п.4 задания)

Терминал 1 — приложение:

```bash
./run.sh --demo
# запомнить pid из строки DEMO READY
```

Терминал 2 — дампы:

```bash
jcmd <pid> GC.heap_dump dumps/after_create.hprof
# (в меню/новых запусках: обновить запись → дамп update, удалить → дамп delete)
jcmd <pid> GC.heap_dump dumps/after_update.hprof
jcmd <pid> GC.heap_dump dumps/after_delete.hprof
jmap -histo <pid> | head -30   # гистограмма классов для отчёта
jstat -gc <pid> 1000           # GC-метрики
```

Анализ (на хосте, не в headless-VM): Eclipse MAT / VisualVM —
искать `app.UserRecord`, проверять отсутствие plaintext паролей/карт
(поиск строк `S3cret`, `4111`), наличие только хешей/шифротекста.

Готовые дампы сценария create/update/delete лежат в `dumps/`
(`after_create.hprof`, `after_update.hprof`, `after_delete.hprof`).
Полный отчёт с измеренными цифрами — в [REPORT.md](REPORT.md).

## Что писать в отчёте

1. Постановка задачи. 2. Описание приложения (модель, меню).
3. Анализ защищённости кода: `char[]`+wipe, PBKDF2 с солью 210k итераций,
AES/GCM (не ECB), ключ через `KeyGenerator`+`SecureRandom`, валидация ввода,
constant-time сравнение, затирание при update/delete, отсутствие секретов
в логах/`toString`/исключениях. 4. Память/CPU (`jstat`, `MemoryMXBean`, stress).
5. Анализ трёх дампов (таблица: что искали → что нашли).
