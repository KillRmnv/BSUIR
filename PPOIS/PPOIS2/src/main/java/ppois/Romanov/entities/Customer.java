package ppois.Romanov.entities;

import lombok.Data;

@Data
public class Customer {
    private FullName name;
    private AccountNumber accountNumber;
    private String address;
    private PhoneNumber mobilePhone;
    private PhoneNumber townPhone;

    public Customer() {
        accountNumber = null;
        mobilePhone = null;
        townPhone = null;
        name = null;
        address = null;
    }

    public Customer(FullName name, int accountNumber, String mobilePhone, String townPhone) {
        this.name = name;
        this.accountNumber = new AccountNumber(accountNumber);
        this.mobilePhone = new PhoneNumber(mobilePhone);
        this.townPhone = new PhoneNumber(townPhone);

    }

    public String getName() {
        if (name != null) {
            return name.getFullName();
        }
        return "";
    }

    public String getAccountNumber() {
        if (accountNumber == null) return "";
        return String.valueOf(accountNumber.getAccountNumber());
    }

    public void setAccountNumber(int accountNumber) {
        this.accountNumber = new AccountNumber(accountNumber);
    }

    public String getMobilePhone() {
        if (mobilePhone == null) return "";
        return mobilePhone.getNumber();
    }

    public String getTownPhone() {
        if (townPhone == null) return "";
        return townPhone.getNumber();
    }

    public void setMobilePhone(String mobilePhone) {
        this.mobilePhone = new PhoneNumber(mobilePhone);
    }

    public void setTownPhone(String townPhone) {
        this.townPhone = new PhoneNumber(townPhone);
    }

    public void setName(String name) {
        if (this.name == null)
            this.name = new FullName(name);
        else
            this.name.setFullName(name);
    }
    public String getAddress() {
        if (address == null) return "";
        return address;
    }

}
