package app;

import java.util.Arrays;

/**
 * Запись пользователя. Разделение по типам данных:
 *  - неконфиденциальные: username, note (открытый текст допустим);
 *  - конфиденциальные: пароль — ТОЛЬКО соль+хеш; номер карты — ТОЛЬКО IV+шифротекст.
 * Plaintext секретов в полях объекта никогда не хранится.
 */
public final class UserRecord {
    private final long id;
    private volatile String username;
    private volatile String note;
    private volatile byte[] passwordSalt;
    private volatile byte[] passwordHash;
    private volatile byte[] cardIv;
    private volatile byte[] cardCipher;

    public UserRecord(long id, String username, String note,
                      byte[] passwordSalt, byte[] passwordHash,
                      byte[] cardIv, byte[] cardCipher) {
        this.id = id;
        this.username = username;
        this.note = note;
        this.passwordSalt = passwordSalt;
        this.passwordHash = passwordHash;
        this.cardIv = cardIv;
        this.cardCipher = cardCipher;
    }

    public long id() { return id; }
    public String username() { return username; }
    public String note() { return note; }
    public byte[] passwordSalt() { return passwordSalt; }
    public byte[] passwordHash() { return passwordHash; }
    public byte[] cardIv() { return cardIv; }
    public byte[] cardCipher() { return cardCipher; }

    public void setUsername(String v) { this.username = v; }
    public void setNote(String v) { this.note = v; }
    public void setPassword(byte[] salt, byte[] hash) {
        wipe(passwordSalt);
        wipe(passwordHash);
        this.passwordSalt = salt;
        this.passwordHash = hash;
    }
    public void setCard(byte[] iv, byte[] cipher) {
        wipe(cardIv);
        wipe(cardCipher);
        this.cardIv = iv;
        this.cardCipher = cipher;
    }

    /** Безвозвратное затирание секретов перед удалением из хранилища. */
    public void destroySecrets() {
        wipe(passwordSalt);
        wipe(passwordHash);
        wipe(cardIv);
        wipe(cardCipher);
        passwordSalt = null;
        passwordHash = null;
        cardIv = null;
        cardCipher = null;
    }

    private static void wipe(byte[] a) {
        if (a != null) {
            Arrays.fill(a, (byte) 0);
        }
    }

    /** Безопасное строковое представление: секреты не печатаются. */
    @Override
    public String toString() {
        return "UserRecord{id=" + id
                + ", username='" + username + '\''
                + ", note='" + note + '\''
                + ", passwordHash=" + (passwordHash == null ? "null" : "present(" + passwordHash.length + "B)")
                + ", cardCipher=" + (cardCipher == null ? "null" : "present(" + cardCipher.length + "B)")
                + '}';
    }
}
