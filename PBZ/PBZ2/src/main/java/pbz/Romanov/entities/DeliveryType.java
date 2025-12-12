package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class DeliveryType {
    protected Integer id;
    protected String typeD;

    public void setTypeD(String type) {
        if (type == null || type.isBlank())
            throw new IllegalArgumentException("Delivery type cannot be empty");
        this.typeD = type.trim();
    }
}
