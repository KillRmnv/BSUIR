package app;

/**
 * Валидация всего пользовательского ввода с понятными сообщениями.
 * Требование методички: поведение при невалидных данных (длинные строки,
 * некорректные типы) должно быть определено и безопасно.
 */
public final class Validator {
    private Validator() {}

    public static final int USERNAME_MIN = 3;
    public static final int USERNAME_MAX = 32;
    public static final int NOTE_MAX = 256;
    public static final int PASSWORD_MIN = 6;
    public static final int PASSWORD_MAX = 64;
    public static final int CARD_MIN = 8;
    public static final int CARD_MAX = 32;

    public static String username(String s) throws ValidationException {
        if (s == null || s.isBlank()) {
            throw new ValidationException("Имя пользователя не должно быть пустым.");
        }
        s = s.trim();
        if (s.length() < USERNAME_MIN || s.length() > USERNAME_MAX) {
            throw new ValidationException(
                    "Имя пользователя: длина " + USERNAME_MIN + "-" + USERNAME_MAX + " символов.");
        }
        if (!s.matches("[A-Za-z0-9_\\-.А-Яа-яЁё]+")) {
            throw new ValidationException("Имя пользователя: допустимы буквы, цифры, '_', '-', '.'.");
        }
        return s;
    }

    public static String note(String s) throws ValidationException {
        if (s == null) {
            return "";
        }
        s = s.trim();
        if (s.length() > NOTE_MAX) {
            throw new ValidationException("Заметка: максимум " + NOTE_MAX + " символов.");
        }
        return s;
    }

    public static void password(char[] p) throws ValidationException {
        if (p == null || p.length == 0) {
            throw new ValidationException("Пароль не должен быть пустым.");
        }
        if (p.length < PASSWORD_MIN || p.length > PASSWORD_MAX) {
            throw new ValidationException(
                    "Пароль: длина " + PASSWORD_MIN + "-" + PASSWORD_MAX + " символов.");
        }
    }

    public static void card(char[] c) throws ValidationException {
        if (c == null || c.length == 0) {
            throw new ValidationException("Номер карты не должен быть пустым.");
        }
        if (c.length < CARD_MIN || c.length > CARD_MAX) {
            throw new ValidationException(
                    "Номер карты: длина " + CARD_MIN + "-" + CARD_MAX + " символов.");
        }
        for (char ch : c) {
            if (!(Character.isDigit(ch) || ch == ' ' || ch == '-')) {
                throw new ValidationException("Номер карты: допустимы только цифры, пробелы и '-'.");
            }
        }
    }

    public static long id(String s) throws ValidationException {
        try {
            long v = Long.parseLong(s.trim());
            if (v <= 0) {
                throw new ValidationException("ID должен быть положительным числом.");
            }
            return v;
        } catch (NumberFormatException e) {
            throw new ValidationException("ID должен быть числом (некорректный тип ввода).");
        }
    }

    public static int menuChoice(String s, int min, int max) throws ValidationException {
        try {
            int v = Integer.parseInt(s.trim());
            if (v < min || v > max) {
                throw new ValidationException("Выберите пункт " + min + "-" + max + ".");
            }
            return v;
        } catch (NumberFormatException e) {
            throw new ValidationException("Введите число — номер пункта меню.");
        }
    }
}
