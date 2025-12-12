package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.Delivery;
import pbz.Romanov.entities.search.DeliverySearch;
import pbz.Romanov.repository.DBInterface;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Singleton
public class DeliveryService {
    @Inject
    @Named("PostgreSQLRepository")
    private DBInterface dbInterface;

    public List<Delivery> getDeliveries(DeliverySearch delivery) throws Exception {
        List<Object> params = setUpForDBOperation(delivery);
        List<Map<String, Object>> result = dbInterface.find(params, Delivery.class);
        List<Delivery> deliveries = new ArrayList<>();
        for (Map<String, Object> row : result) {
            deliveries.add(new Delivery((Integer) row.get("delivery_id"), (int) row.get("type_id"),
                    row.get("address").toString(), (int) row.get("hist_id"),  row.get("expected_date").toString()));
        }
        return deliveries;
    }


    public void insertDelivery(Delivery delivery) throws Exception {
        List<Object> params = new ArrayList<>();
        params.add(delivery.getType());
        params.add(delivery.getAddress());
        params.add(delivery.getHistId());
        params.add(delivery.getExpectedDate());

        dbInterface.save(params, Delivery.class);
    }

    private List<Object> setUpForDBOperation(DeliverySearch delivery) {

        return form(delivery.getId(), delivery.getType(), delivery.getAddress(), delivery.getHistId(), delivery.getExpectedDate());
    }

    private List<Object> form(int id, int type, String address, int hist, String date) {
        List<Object> params = new ArrayList<>();
        params.add(id);
        params.add(type);
        params.add(address);
        params.add(hist);
        params.add(date);
        return params;
    }

    public void updateDelivery(Delivery delivery) throws Exception {

        dbInterface.update(form(delivery.getId(), delivery.getType(), delivery.getAddress(), delivery.getHistId(), delivery.getExpectedDate()),
        Delivery.class);
    }

    public int deleteDelivery(DeliverySearch delivery) throws Exception {
        List<Object> params = setUpForDBOperation(delivery);
         dbInterface.delete(params, Delivery.class);
         return 0;
    }
}
