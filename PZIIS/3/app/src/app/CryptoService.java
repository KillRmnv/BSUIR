package app;

import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Arrays;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.PBEKeySpec;

/**
 * Криптографический сервис: хеширование паролей (PBKDF2) и
 * шифрование обратимых конфиденциальных данных (AES/GCM).
 *
 * Только JDK (JCA), без внешних зависимостей — для переносимости Arch → Void.
 */
public final class CryptoService {

    private static final String PBKDF2_ALG = "PBKDF2WithHmacSHA256";
    private static final int PBKDF2_ITERATIONS = 210_000;
    private static final int PBKDF2_KEY_BITS = 256;
    private static final int SALT_BYTES = 16;

    private static final String AES_TRANSFORMATION = "AES/GCM/NoPadding";
    private static final int GCM_IV_BYTES = 12;
    private static final int GCM_TAG_BITS = 128;

    private final SecureRandom random = new SecureRandom();
    private final SecretKey aesKey;
    private final SecretKeyFactory pbkdf2;

    public CryptoService() {
        try {
            KeyGenerator kg = KeyGenerator.getInstance("AES");
            kg.init(256, random);
            this.aesKey = kg.generateKey();
            this.pbkdf2 = SecretKeyFactory.getInstance(PBKDF2_ALG);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException("JCA-алгоритм недоступен в данном JDK", e);
        }
    }

    // --- Пароли: только соль + хеш, plaintext нигде не хранится ---

    public record PasswordHash(byte[] salt, byte[] hash) {}

    public PasswordHash hashPassword(char[] password) {
        byte[] salt = new byte[SALT_BYTES];
        random.nextBytes(salt);
        byte[] pwdBytes = charsToBytes(password);
        try {
            PBEKeySpec spec = new PBEKeySpec(toChars(pwdBytes), salt, PBKDF2_ITERATIONS, PBKDF2_KEY_BITS);
            byte[] hash = pbkdf2.generateSecret(spec).getEncoded();
            spec.clearPassword();
            return new PasswordHash(salt.clone(), hash);
        } catch (Exception e) {
            throw new IllegalStateException("Не удалось захешировать пароль", e);
        } finally {
            wipe(pwdBytes);
        }
    }

    /** Сравнение в constant-time через MessageDigest.isEqual. */
    public boolean verifyPassword(char[] candidate, byte[] salt, byte[] expectedHash) {
        byte[] candBytes = charsToBytes(candidate);
        try {
            PBEKeySpec spec = new PBEKeySpec(toChars(candBytes), salt, PBKDF2_ITERATIONS, PBKDF2_KEY_BITS);
            byte[] candHash = pbkdf2.generateSecret(spec).getEncoded();
            spec.clearPassword();
            boolean ok = java.security.MessageDigest.isEqual(candHash, expectedHash);
            wipe(candHash);
            return ok;
        } catch (Exception e) {
            return false;
        } finally {
            wipe(candBytes);
        }
    }

    // --- Обратимые данные (номер карты): AES/GCM ---

    public record EncryptedData(byte[] iv, byte[] ciphertext) {}

    public EncryptedData encrypt(char[] plaintext) {
        byte[] plainBytes = charsToBytes(plaintext);
        try {
            byte[] iv = new byte[GCM_IV_BYTES];
            random.nextBytes(iv);
            Cipher cipher = Cipher.getInstance(AES_TRANSFORMATION);
            cipher.init(Cipher.ENCRYPT_MODE, aesKey, new GCMParameterSpec(GCM_TAG_BITS, iv));
            byte[] ct = cipher.doFinal(plainBytes);
            return new EncryptedData(iv, ct);
        } catch (Exception e) {
            throw new IllegalStateException("Не удалось зашифровать данные", e);
        } finally {
            wipe(plainBytes);
        }
    }

    /** Возвращает расшифровку как char[] — вызывающий обязан затереть результат. */
    public char[] decrypt(byte[] iv, byte[] ciphertext) {
        try {
            Cipher cipher = Cipher.getInstance(AES_TRANSFORMATION);
            cipher.init(Cipher.DECRYPT_MODE, aesKey, new GCMParameterSpec(GCM_TAG_BITS, iv));
            byte[] plainBytes = cipher.doFinal(ciphertext);
            char[] chars = bytesToChars(plainBytes);
            wipe(plainBytes);
            return chars;
        } catch (Exception e) {
            throw new IllegalStateException("Не удалось расшифровать данные", e);
        }
    }

    // --- Утилиты безопасной работы с памятью ---

    /** Затирание секретов. Вызывать в finally после использования. */
    public static void wipe(byte[] a) {
        if (a != null) {
            Arrays.fill(a, (byte) 0);
        }
    }

    public static void wipe(char[] a) {
        if (a != null) {
            Arrays.fill(a, '\0');
        }
    }

    private static byte[] charsToBytes(char[] chars) {
        ByteBuffer bb = StandardCharsets.UTF_8.encode(CharBuffer.wrap(chars));
        byte[] out = new byte[bb.remaining()];
        bb.get(out);
        wipeBuffer(bb);
        return out;
    }

    private static char[] bytesToChars(byte[] bytes) {
        CharBuffer cb = StandardCharsets.UTF_8.decode(ByteBuffer.wrap(bytes));
        char[] out = new char[cb.remaining()];
        cb.get(out);
        wipeBuffer(cb);
        return out;
    }

    private static char[] toChars(byte[] bytes) {
        char[] c = new char[bytes.length];
        for (int i = 0; i < bytes.length; i++) {
            c[i] = (char) (bytes[i] & 0xFF);
        }
        return c;
    }

    private static void wipeBuffer(ByteBuffer bb) {
        if (bb.hasArray()) {
            wipe(bb.array());
        }
    }

    private static void wipeBuffer(CharBuffer cb) {
        if (cb.hasArray()) {
            wipe(cb.array());
        }
    }
}
