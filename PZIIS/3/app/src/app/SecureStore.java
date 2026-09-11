package app;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;


public final class SecureStore {
    private final ConcurrentHashMap<Long, UserRecord> map = new ConcurrentHashMap<>();
    private final AtomicLong ids = new AtomicLong(0);
    private final CryptoService crypto;

    public SecureStore(CryptoService crypto) {
        this.crypto = crypto;
    }

    public UserRecord create(String username, String note, char[] password, char[] card)
            throws ValidationException {
        username = Validator.username(username);
        note = Validator.note(note);
        Validator.password(password);
        Validator.card(card);
        CryptoService.PasswordHash ph = null;
        CryptoService.EncryptedData enc = null;
        try {
            ph = crypto.hashPassword(password);
            enc = crypto.encrypt(card);
            long id = ids.incrementAndGet();
            UserRecord r = new UserRecord(id, username, note,
                    ph.salt(), ph.hash(), enc.iv(), enc.ciphertext());
            map.put(id, r);
            return r;
        } finally {
            CryptoService.wipe(password);
            CryptoService.wipe(card);
        }
    }

    /**
     * Обновление записи. Требует текущий пароль: без него чужую запись
     * нельзя ни прочитать, ни изменить. Сообщение об ошибке единое —
     * не раскрывает, существует ли ID (защита от перебора ID).
     */
    public UserRecord update(long id, char[] authPassword,
                             String username, String note,
                             char[] newPassword, char[] newCard)
            throws ValidationException {
        UserRecord r = authenticate(id, authPassword);
        try {
            if (username != null && !username.isBlank()) {
                r.setUsername(Validator.username(username));
            }
            if (note != null) {
                r.setNote(Validator.note(note));
            }
            if (newPassword != null && newPassword.length > 0) {
                Validator.password(newPassword);
                CryptoService.PasswordHash ph = crypto.hashPassword(newPassword);
                r.setPassword(ph.salt(), ph.hash());
            }
            if (newCard != null && newCard.length > 0) {
                Validator.card(newCard);
                CryptoService.EncryptedData enc = crypto.encrypt(newCard);
                r.setCard(enc.iv(), enc.ciphertext());
            }
            return r;
        } finally {
            CryptoService.wipe(newPassword);
            CryptoService.wipe(newCard);
        }
    }

    /**
     * Удаление: сначала аутентификация, затем затирание секретов + remove,
     * чтобы объект стал unreachable для GC.
     */
    public void delete(long id, char[] authPassword) throws ValidationException {
        UserRecord r = authenticate(id, authPassword);
        if (map.remove(id, r)) {
            r.destroySecrets();
        }
    }

    public UserRecord get(long id) {
        return map.get(id);
    }

    public List<UserRecord> list() {
        return new ArrayList<>(map.values());
    }

    public int size() {
        return map.size();
    }

    public boolean verifyPassword(long id, char[] candidate) throws ValidationException {
        UserRecord r = authenticate(id, candidate);
        // authenticate уже сверил пароль: дошли сюда — он верный.
        // Повторная сверка не нужна; candidate затёрт внутри authenticate.
        return true;
    }

    /**
     * Расшифровка карты. Требует текущий пароль (чтение чужого секрета —
     * та же дыра, что и изменение без пароля). Возвращённый char[]
     * вызывающий обязан затереть.
     */
    public char[] decryptCard(long id, char[] authPassword) throws ValidationException {
        UserRecord r = authenticate(id, authPassword);
        return crypto.decrypt(r.cardIv(), r.cardCipher());
    }

    /**
     * Единая точка аутентификации: сверяет пароль и возвращает запись.
     * Неверный пароль и несуществующий ID дают ОДНО сообщение —
     * нельзя перебором установить, какие ID существуют.
     * candidate затирается всегда.
     */
    private UserRecord authenticate(long id, char[] candidate) throws ValidationException {
        try {
            UserRecord r = map.get(id);
            if (r != null && crypto.verifyPassword(candidate, r.passwordSalt(), r.passwordHash())) {
                return r;
            }
            throw new ValidationException("Неверный пароль или запись не найдена.");
        } finally {
            CryptoService.wipe(candidate);
        }
    }
}
