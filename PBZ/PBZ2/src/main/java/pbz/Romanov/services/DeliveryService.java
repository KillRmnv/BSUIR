package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.Delivery;
import pbz.Romanov.repository.DBInterface;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Singleton
public class DeliveryService {
    @Inject
    @Named("PostgreSQLRepository")
    private DBInterface dbInterface;

    public List<Delivery> getDeliveries(Delivery delivery) throws Exception {
        List<Object> params = setUpForDBOperation(delivery);
        List<Map<String, Object>> result = dbInterface.find(params, Delivery.class);
        List<Delivery> deliverys = new ArrayList<>();
        for (Map<String, Object> row : result) {
            deliverys.add(new Delivery((Integer) row.get("delivery_id"), (String) row.get("Тип"),
                     row.get("Дата").toString()));
        }
        return deliverys;
    }


    public void insertDelivery(Delivery delivery) throws Exception {
        List<Object> params = new ArrayList<>();
        params.add(delivery.getDate());
        params.add(delivery.getType());

        dbInterface.save(params, Delivery.class);
    }

    private List<Object> setUpForDBOperation(Delivery delivery) {
        List<Object> params = new ArrayList<>();
        params.add(delivery.getDate());
        params.add(delivery.getId());
        params.add(delivery.getType());

        return params;
    }

    public void updateDelivery(Delivery delivery) throws Exception {
        List<Object> params = setUpForDBOperation(delivery);
        dbInterface.update(params, Delivery.class);
    }

    public int deleteDelivery(Delivery delivery) throws Exception {
        List<Object> params = setUpForDBOperation(delivery);
        return dbInterface.delete(params, Delivery.class);
    }
}
