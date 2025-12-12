package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class Organization {
    protected Integer id;
    protected String name;
    protected String baseAddressForDelivery;
    protected Integer typeOfDelivery;

    public void setId(int id) {
        if (id < 1)
            throw new IllegalArgumentException("Organization ID must be > 0");
        this.id = id;
    }

    public void setName(String name) {
        if (name == null || name.isBlank())
            throw new IllegalArgumentException("Organization name cannot be empty");
        this.name = name.trim();
    }

    public void setBaseAddressForDelivery(String address) {
        if (address == null || address.isBlank())
            throw new IllegalArgumentException("Base address cannot be empty");
        this.baseAddressForDelivery = address.trim();
    }
}
