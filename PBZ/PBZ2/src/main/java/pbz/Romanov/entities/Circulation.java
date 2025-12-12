package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class Circulation {
    protected Integer pubId;
    protected Integer amount;
    protected Integer allocatedAmount;
    protected Integer numOfPub;

    public void setAmount(Integer amount) {
        if (amount <= 0)
            throw new IllegalArgumentException("Amount must be > 0");
        this.amount = amount;
    }

    public void setAllocatedAmount(Integer allocated) {
        if (allocated < 0)
            throw new IllegalArgumentException("Allocated amount cannot be negative");
        this.allocatedAmount = allocated;
    }

    public void setNumOfPub(Integer num) {
        if (num <= 0)
            throw new IllegalArgumentException("Publication number must be > 0");
        this.numOfPub = num;
    }
}
