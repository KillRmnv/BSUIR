package pbz.Romanov.entities.search;

import lombok.Getter;
import lombok.Setter;
import pbz.Romanov.entities.Subscription;
import pbz.Romanov.entities.Printing;

@Getter
@Setter
public class SubscriptionSearch extends Subscription {

    @Override
    public void setId(Integer id) {
        this.id = id;
    }

    @Override
    public void setStartingDate(String startingDate) {
        this.startingDate = (startingDate != null) ? startingDate.trim() : null;
    }

    @Override
    public void setEndingDate(String endingDate) {
        this.endingDate = (endingDate != null) ? endingDate.trim() : null;
    }

    @Override
    public void setPeriod(Integer period) {
        this.period = period;
    }

    @Override
    public void setPrinting(Printing printing) {
        this.printing = printing;
    }

    @Override
    public void setEmployeeId(Integer employeeId) {
        this.employeeId = employeeId;
    }

    @Override
    public void setCost(Integer cost) {
        this.cost = cost;
    }
}
