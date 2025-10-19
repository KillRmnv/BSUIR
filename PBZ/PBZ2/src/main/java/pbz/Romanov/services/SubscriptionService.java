package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.Subscription;
import pbz.Romanov.repository.DBInterface;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Singleton
public class SubscriptionService {
    @Inject
    @Named("PostgreSQLRepository")
    private DBInterface dbInterface;

    public SubscriptionService(DBInterface dbInterface) {
        this.dbInterface = dbInterface;
    }

    public List<Subscription> getSubscriptions(Subscription subscription) throws Exception {
        List<Object> params = setUpForDBOperation(subscription);
        List<Map<String, Object>> result = dbInterface.find(params, Subscription.class);
        List<Subscription> subscriptions = new ArrayList<>();
        for (Map<String, Object> row : result) {
            subscriptions.add(new Subscription(
                    (Integer) row.get("Индекс издания"),
                    (Integer) row.get("employee_id"),
                     row.get("Дата начала").toString(),
                     row.get("Дата окончания").toString(),
                    (Integer) row.get("Доставка"),
                    (Integer) row.get("Период"),
                    (Integer) row.get("Стоимость")));
        }
        return subscriptions;
    }


    public void insertSubscription(Subscription subscription) throws Exception {
        List<Object> params = setUpForDBOperation(subscription);
        dbInterface.save(params, Subscription.class);
    }

    private List<Object> setUpForDBOperation(Subscription subscription) {
        List<Object> params = new ArrayList<>();
        params.add(subscription.getPrinting().getIndex());
        params.add(subscription.getEmployeeId());
        params.add(subscription.getStartingDate());
        params.add(subscription.getEndingDate());
        params.add(subscription.getDelivery().getId());
        params.add(subscription.getAmountOfMonths());
        params.add(subscription.getCost());
        return params;
    }

    public void updateSubscription(Subscription subscription) throws Exception {
        List<Object> params = setUpForDBOperation(subscription);
        dbInterface.update(params, Subscription.class);
    }

    public int deleteSubscription(Subscription subscription) throws Exception {
        List<Object> params = setUpForDBOperation(subscription);
        return dbInterface.delete(params, Subscription.class);
    }


}
