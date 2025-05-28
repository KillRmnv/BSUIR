package ppois.Romanov;

import lombok.Data;
import ppois.Romanov.entities.Customer;

@Data
public class CustomerSearchCriteria {
    private String name;
    private String accountNumber;
    private String address;
    private String mobilePhone;
    private String townPhone;
    public CustomerSearchCriteria() {

    }
    public CustomerSearchCriteria(Customer customer) {
        this.name = customer.getName();
        this.accountNumber = String.valueOf(customer.getAccountNumber());
        this.address = customer.getAddress();
        this.mobilePhone = customer.getMobilePhone();
        this.townPhone = customer.getTownPhone();
    }
}
