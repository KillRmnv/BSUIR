package pbz.Romanov.entities.search;

import lombok.Getter;
import lombok.Setter;
import pbz.Romanov.entities.Printing;

@Getter
@Setter
public class PrintingSearch extends Printing {

    @Override
    public void setType(Integer type) {
        this.type = type;
    }

    @Override
    public void setIndex(Integer index) {
       this.index = index;
    }

    @Override
    public void setPeriod(Integer period) {
        this.period = period;
    }

    @Override
    public void setName(String name) {
        this.name = (name != null) ? name.trim() : null;
    }
}
