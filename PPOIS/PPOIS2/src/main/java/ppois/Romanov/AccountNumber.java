package ppois.Romanov;

public class AccountNumber {
    private int accountNumber;

    public AccountNumber(int accountNumber) throws IllegalArgumentException {
        if (isValidAccountNumber(accountNumber)) {
            setAccountNumber(accountNumber);
        }
        else {
            throw new IllegalArgumentException("Номер счета должен быть положительным и состоять из 8 цифр.");
        }
    }

    public void setAccountNumber(int accountNumber) throws IllegalArgumentException {
        if (isValidAccountNumber(accountNumber)) {
            this.accountNumber = accountNumber;
        } else {
            throw new IllegalArgumentException("Номер счета должен быть положительным и состоять из 8 цифр.");
        }
    }

    public int getAccountNumber() {
        return accountNumber;
    }

    private boolean isValidAccountNumber(int number) {
        return number >= 0 && String.valueOf(number).length() == 8;
    }
}
