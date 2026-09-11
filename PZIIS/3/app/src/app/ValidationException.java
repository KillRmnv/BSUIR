package app;

/** Исключение валидации с безопасным сообщением для пользователя. */
public final class ValidationException extends Exception {
    public ValidationException(String message) {
        super(message);
    }
}
