package pbz.Romanov.entities.search;

import lombok.Getter;
import lombok.Setter;
import pbz.Romanov.entities.Circulation;

@Getter
@Setter
public class CirculationSearch extends Circulation {

    @Override
    public void setAmount(Integer amount) {
        // Для поиска разрешаем любые значения, включая 0 или -1
        this.amount = amount;
    }

    @Override
    public void setAllocatedAmount(Integer allocated) {
        // Для поиска разрешаем любые значения, включая отрицательные
        this.allocatedAmount = allocated;
    }

    @Override
    public void setNumOfPub(Integer num) {
        // Для поиска разрешаем любые значения, включая 0 или -1
        this.numOfPub = num;
    }
}
