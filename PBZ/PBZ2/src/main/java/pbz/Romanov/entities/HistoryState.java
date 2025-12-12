package pbz.Romanov.entities;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
public class HistoryState {
    protected Integer stateId;
    protected String stateName;

    public void setStateName(String name) {
        if (name == null || name.isBlank())
            throw new IllegalArgumentException("History state name cannot be empty");
        this.stateName = name.trim();
    }
}
