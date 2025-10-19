package pbz.Romanov.entities;

import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@Data
public class Printing {
    private String type;
    private int index = -1;
    private int period = -1;
    private String name;

    public void setPeriod(int period) {
        if (period > 0) {
            this.period = period;
        } else throw new IllegalArgumentException("Period must be greater than 0");
    }

    public void setIndex(int index) {
        if (index > 0) {
            this.index = index;
        } else throw new IllegalArgumentException("Index must be greater than 0");
    }
    public Printing(int id) {
        this.index = id;
    }
    public Printing(String type, int index, int period, String name) {
        this.type = type;
        this.index = index;
        this.period = period;
        this.name = name;
    }

}
