package ppois.romanov.entities;

public class PhoneNumber {
    private String number;

    public PhoneNumber(String number) throws IllegalArgumentException {
        setNumber(number);
    }

    public void setNumber(String number) throws  IllegalArgumentException {
        if (isValidPhoneNumber(number)) {
            this.number = number;
        } else {
            throw new IllegalArgumentException("Неверный формат номера. Номер должен начинаться с '+' и иметь длину 10 символов (включая '+').");
        }
    }

    public String getNumber() {
        return number;
    }

    private boolean isValidPhoneNumber(String number) {
        return number != null && number.length() == 10 && number.startsWith("+") && number.substring(1).matches("\\d{9}");
    }
}
