package app;

import java.io.Console;
import java.io.File;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

/**
 * Лаб. №3.1: консольное приложение «учётные записи» (RAM, хеш+шифр).
 *
 * Режимы запуска:
 *   java -cp out app.Main --demo     — автомат: создаёт → обновляет → удаляет, снимает 3 дампа в dumps/
 *   java -cp out app.Main --stress N — создаёт N записей для раздела «нагрузки»
 *   java -cp out app.Main            — интерактивное меню (ручной ввод)
 */
public final class Main {
    private final SecureStore store;
    private final Scanner scanner = new Scanner(System.in);

    public Main(SecureStore store) {
        this.store = store;
    }

    public static void main(String[] args) {
        CryptoService crypto = new CryptoService();
        SecureStore store = new SecureStore(crypto);
        Main app = new Main(store);

        if (args.length > 0 && args[0].equals("--demo")) {
            runDemo(store);
            return;
        }
        if (args.length > 0 && args[0].equals("--stress")) {
            int n = args.length > 1 ? Integer.parseInt(args[1]) : 10_000;
            runStress(store, n);
            return;
        }

        System.out.println("=== Лаб. №3.1: учётные записи (RAM, хеш+шифр) ===");
        System.out.println("PID процесса: " + ProcessHandle.current().pid()
                + " — используйте его для jcmd/jmap.");
        app.menuLoop();
    }

    /** Демо-режим: автоматически создаёт/обновляет/удаляет записи + снимает 3 дампа. */
    private static void runDemo(SecureStore store) {
        File dumpsDir = new File("dumps");
        if (!dumpsDir.exists() && !dumpsDir.mkdirs()) {
            System.err.println("Не удалось создать папку dumps/");
            return;
        }

        long pid = ProcessHandle.current().pid();
        System.out.println("=== DEMO MODE (pid=" + pid + ") ===");

        System.out.println("\n--- Шаг 1: создание записей ---");
        try {
            store.create("alice", "открытая заметка 1",
                    "S3cret-alice!".toCharArray(), "4111-1111-1111-1111".toCharArray());
            store.create("bob", "открытая заметка 2",
                    "S3cret-bob!!".toCharArray(), "5500-0000-0000-0004".toCharArray());
            store.create("carol", "открытая заметка 3",
                    "S3cret-carol!".toCharArray(), "3400-0000-0000-009".toCharArray());
            System.out.println("Создано 3 записи: alice, bob, carol");
        } catch (ValidationException e) {
            System.err.println("Demo setup failed: " + e.getMessage());
            return;
        }

        sleep(500);
        takeDump(pid, "dumps/after_create.hprof");

        System.out.println("\n--- Шаг 2: обновление alice ---");
        try {
            String newPwd = new String(new char[]{
                    'A','L','I','C','E','-','N','E','W','-',
                    'S','E','C','R','E','T','-','1','1','!'});
            String newCard = new String(new char[]{
                    '3','4','0','0','-','0','0','0','0','-',
                    '0','0','0','0','-','0','0','9'});
            store.update(1L, "S3cret-alice!".toCharArray(),
                    null, null,
                    newPwd.toCharArray(),
                    newCard.toCharArray());
            System.out.println("alice: пароль → " + newPwd + ", карта → " + newCard);
        } catch (ValidationException e) {
            System.err.println("Update failed: " + e.getMessage());
        }

        sleep(500);
        takeDump(pid, "dumps/after_update.hprof");

        System.out.println("\n--- Шаг 3: удаление bob ---");
        try {
            store.delete(2L, "S3cret-bob!!".toCharArray());
            System.out.println("bob удалён, секреты затёрты");
        } catch (ValidationException e) {
            System.err.println("Delete failed: " + e.getMessage());
        }

        sleep(500);
        takeDump(pid, "dumps/after_delete.hprof");

        System.out.println("\n=== DEMO DONE ===");
        System.out.println("Дампы в папке dumps/:");
        System.out.println("  after_create.hprof  — после создания 3 записей");
        System.out.println("  after_update.hprof  — после обновления alice");
        System.out.println("  after_delete.hprof  — после удаления bob");
        System.out.println("\nАнализ:");
        System.out.println("  grep -a 'S3cret-alice' dumps/*.hprof   — старый пароль alice (должен быть ТОЛЬКО в after_create)");
        System.out.println("  grep -a 'ALICE-NEW-SECRET' dumps/*.hprof — новый пароль alice (должен быть в after_update и after_delete)");
        System.out.println("  grep -a 'S3cret-bob' dumps/*.hprof     — пароль bob (должен быть во всех — буфер ввода)");
        System.out.println("  grep -a '4111-1111' dumps/*.hprof      — старая карта alice");
        System.out.println("  grep -a '5500-0000' dumps/*.hprof      — карта bob");
    }

    private static void takeDump(long pid, String path) {
        System.out.print("Снимаю дамп " + path + "... ");
        try {
            ProcessBuilder pb = new ProcessBuilder(
                    "jcmd", String.valueOf(pid), "GC.heap_dump", path);
            pb.redirectErrorStream(true);
            Process proc = pb.start();
            String output = new String(proc.getInputStream().readAllBytes()).trim();
            int exit = proc.waitFor();
            if (exit == 0) {
                long size = new File(path).length();
                System.out.println("OK (" + (size / 1024) + " KB)");
            } else {
                System.out.println("ОШИБКА: " + output);
            }
        } catch (Exception e) {
            System.out.println("ОШИБКА: " + e.getMessage());
            System.out.println("Убедитесь, что jcmd доступен в PATH (JDK tool)");
        }
    }

    private static void sleep(int ms) {
        try { Thread.sleep(ms); } catch (InterruptedException ignored) { }
    }

    /** Нагрузочный прогон для раздела отчёта "поведение при больших нагрузках". */
    private static void runStress(SecureStore store, int n) {
        System.out.println("STRESS: создание " + n + " записей...");
        long t0 = System.nanoTime();
        int ok = 0;
        for (int i = 0; i < n; i++) {
            try {
                store.create("user" + i, "note " + i,
                        ("Pwd-" + i + "-xx!").toCharArray(), "4111111111111111".toCharArray());
                ok++;
            } catch (ValidationException e) {
                System.err.println("skip " + i + ": " + e.getMessage());
            }
        }
        long ms = (System.nanoTime() - t0) / 1_000_000;
        printMem("после stress (" + ok + " записей за " + ms + " мс)");
        System.out.println("STRESS DONE pid=" + ProcessHandle.current().pid()
                + " — снимайте дамп/метрики, затем Ctrl+C.");
        try {
            Thread.sleep(600_000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private void menuLoop() {
        while (true) {
            System.out.println();
            System.out.println("1. Создать запись");
            System.out.println("2. Показать список (без секретов)");
            System.out.println("3. Обновить запись (нужен пароль)");
            System.out.println("4. Удалить запись (нужен пароль)");
            System.out.println("5. Проверить пароль");
            System.out.println("6. Расшифровать карту (нужен пароль)");
            System.out.println("7. Память (Runtime/MXBean)");
            System.out.println("0. Выход");
            System.out.print("> ");
            String line;
            try {
                line = scanner.nextLine();
            } catch (Exception e) {
                System.out.println("Ошибка ввода. Завершение.");
                return;
            }
            int choice;
            try {
                choice = Validator.menuChoice(line, 0, 7);
            } catch (ValidationException e) {
                System.out.println("Ошибка: " + e.getMessage());
                continue;
            }
            try {
                switch (choice) {
                    case 1 -> doCreate();
                    case 2 -> doList();
                    case 3 -> doUpdate();
                    case 4 -> doDelete();
                    case 5 -> doVerify();
                    case 6 -> doDecrypt();
                    case 7 -> printMem("по запросу");
                    case 0 -> {
                        System.out.println("Выход.");
                        return;
                    }
                }
            } catch (ValidationException e) {
                System.out.println("Ошибка: " + e.getMessage());
            } catch (OutOfMemoryError e) {
                System.out.println("Ошибка: недостаточно памяти. Часть данных могла быть потеряна.");
            } catch (Exception e) {
                System.out.println("Внутренняя ошибка. Попробуйте ещё раз.");
            }
        }
    }

    private void doCreate() throws ValidationException {
        System.out.print("Имя (3-32): ");
        String username = scanner.nextLine();
        System.out.print("Заметка (до 256, открытая): ");
        String note = scanner.nextLine();
        char[] pwd = readSecret("Пароль (6-64): ");
        char[] card = readSecret("Номер карты (8-32, цифры/пробел/-): ");
        UserRecord r = store.create(username, note, pwd, card);
        // store уже затёр pwd/card в finally
        System.out.println("Создано: " + r);
    }

    private void doList() {
        List<UserRecord> all = store.list();
        if (all.isEmpty()) {
            System.out.println("(пусто)");
            return;
        }
        all.forEach(System.out::println);
    }

    private void doUpdate() throws ValidationException {
        System.out.print("ID записи: ");
        long id = Validator.id(scanner.nextLine());
        char[] auth = readSecret("Текущий пароль записи: ");
        System.out.print("Новое имя (Enter — пропустить): ");
        String username = scanner.nextLine();
        System.out.print("Новая заметка (Enter — пропустить): ");
        String note = scanner.nextLine();
        char[] pwd = readSecretOptional("Новый пароль (Enter — пропустить): ");
        char[] card = readSecretOptional("Новый номер карты (Enter — пропустить): ");
        UserRecord r = store.update(id, auth,
                username.isBlank() ? null : username,
                note.isEmpty() ? null : note, pwd, card);
        System.out.println("Обновлено: " + r);
    }

    private void doDelete() throws ValidationException {
        System.out.print("ID записи: ");
        long id = Validator.id(scanner.nextLine());
        char[] auth = readSecret("Текущий пароль записи: ");
        store.delete(id, auth);
        System.out.println("Удалено (секреты затёрты).");
    }

    private void doVerify() throws ValidationException {
        System.out.print("ID записи: ");
        long id = Validator.id(scanner.nextLine());
        char[] cand = readSecret("Пароль для проверки: ");
        boolean ok = store.verifyPassword(id, cand);
        System.out.println(ok ? "Пароль верный." : "Пароль НЕверный.");
    }

    private void doDecrypt() throws ValidationException {
        System.out.print("ID записи: ");
        long id = Validator.id(scanner.nextLine());
        char[] auth = readSecret("Текущий пароль записи: ");
        char[] plain = store.decryptCard(id, auth);
        try {
            System.out.println("Расшифрованная карта: " + new String(plain));
        } finally {
            CryptoService.wipe(plain);
        }
    }

    private static void printMem(String ctx) {
        Runtime rt = Runtime.getRuntime();
        MemoryMXBean mx = ManagementFactory.getMemoryMXBean();
        System.out.printf("Память [%s]: heap used=%d MB / max=%d MB; nonHeap=%d MB%n",
                ctx,
                mx.getHeapMemoryUsage().getUsed() / 1024 / 1024,
                rt.maxMemory() / 1024 / 1024,
                mx.getNonHeapMemoryUsage().getUsed() / 1024 / 1024);
    }

    /** Чтение секрета без эха, если есть консоль; иначе — обычный ввод. */
    private char[] readSecret(String prompt) {
        Console console = System.console();
        if (console != null) {
            char[] v = console.readPassword("%s", prompt);
            return v == null ? new char[0] : v;
        }
        System.out.print(prompt);
        return scanner.nextLine().toCharArray();
    }

    private char[] readSecretOptional(String prompt) {
        char[] v = readSecret(prompt);
        // Пустой ввод = "пропустить поле" (update); store трактует пустой массив как пропуск.
        if (v.length == 1 && v[0] == '\n') {
            Arrays.fill(v, '\0');
            return new char[0];
        }
        return v;
    }
}
