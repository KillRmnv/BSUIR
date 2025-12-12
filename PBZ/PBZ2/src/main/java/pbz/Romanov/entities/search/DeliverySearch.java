package pbz.Romanov.entities.search;

import lombok.Getter;
import lombok.Setter;
import pbz.Romanov.entities.Delivery;

@Getter
@Setter
public class DeliverySearch extends Delivery {

    public DeliverySearch() {
        // Пустой конструктор
    }

    public DeliverySearch(Integer deliveryId) {
        this.id = deliveryId;
    }

    @Override
    public void setId(Integer id) {
        // Для поиска разрешаем любые значения, включая -1
        this.id = id;
    }

    @Override
    public void setType(Integer type) {
        // Для поиска разрешаем любые значения
        this.type = type;
    }

    @Override
    public void setAddress(String address) {
        // Для поиска разрешаем пустые значения
        this.address = (address != null) ? address.trim() : null;
    }

    @Override
    public void setState(Integer state) {
        // Для поиска разрешаем любые значения
        this.histId = state;
    }

    @Override
    public void setExpectedDate(String expectedDate) {
        // Для поиска разрешаем пустые значения
        this.expectedDate = (expectedDate != null) ? expectedDate.trim() : null;
    }
}
