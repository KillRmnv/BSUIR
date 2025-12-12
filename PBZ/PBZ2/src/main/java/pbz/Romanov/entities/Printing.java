package pbz.Romanov.entities;

import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.*;

@NoArgsConstructor
@Data
public class Printing {
    protected Integer type;
    protected Integer index ;
    protected Integer period ;
    protected String name;

    public void setPeriod(Integer period) {
        if (period > 0) {
            this.period = period;
        } else throw new IllegalArgumentException("Period must be greater than 0");
    }

    public void setIndex(Integer index) {
        if (index > 0) {
            this.index = index;
        } else throw new IllegalArgumentException("Index must be greater than 0");
    }
    public Printing(Integer id) {
        this.index = id;
    }
    public Printing(Integer type, Integer index, Integer period, String name) {
        this.type = type;
        this.index = index;
        this.period = period;
        this.name = name;
    }
    public void  setType(Integer type) {
        Set<String> allowedTypes = new HashSet<String>(Set.of("Выписано", "Получено", "Отсутствует"));
        if(allowedTypes.contains(type)) {
            this.type = type;
        }else{
            throw new IllegalArgumentException("not allowed type");
        }
    }
}
