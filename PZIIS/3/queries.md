SELECT arr FROM char[] arr WHERE (toString(arr) LIKE ".*SECRET.*")

SELECT * FROM char[] arr WHERE arr.@length > 5


```bash
# Вариант 1: ps + grep
ps aux | grep "app.Main"

# Вариант 2: jcmd (покажет все Java-процессы)
jcmd -l

# Вариант 3:pidof (если нет других java)
pidof java


jcmd <PID> GC.heap_dump dumps/interactive.hprof

```