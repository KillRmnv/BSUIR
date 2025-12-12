package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.Subscription;
import pbz.Romanov.entities.search.SubscriptionSearch;
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

    public List<Subscription> getSubscriptions(SubscriptionSearch subscription) throws Exception {
        List<Object> params = setUpForDBOperation(subscription);
        params.addFirst(Integer.valueOf(-1));
        List<Map<String, Object>> result = dbInterface.find(params, Subscription.class);

        List<Subscription> subscriptions = new ArrayList<>();
        for (Map<String, Object> row : result) {
            subscriptions.add(new Subscription((Integer) row.get("id"), (Integer) row.get("index_printing"),
                    (Integer) row.get("employee_id"), row.get("date_beg").toString(),
                    row.get("date_end").toString(), (Integer) row.get("period"), (Integer) row.get("cost")));
        }
        return subscriptions;
    }

    public void insertSubscription(Subscription subscription) throws Exception {

        List<Object> params = new ArrayList<>();
        params.add(subscription.getPrinting().getIndex());
        params.add(subscription.getEmployeeId());
        params.add(subscription.getStartingDate());
        params.add(subscription.getPeriod());
        params.add(subscription.getCost());
        dbInterface.save(params , Subscription.class);
    }

    private List<Object> setUpForDBOperation(SubscriptionSearch subscription) {
        return form(subscription.getPrinting().getIndex(), subscription.getEmployeeId(),
                subscription.getStartingDate(), subscription.getEndingDate(), subscription.getPeriod(),
                subscription.getCost());
    }

    public void updateSubscription(Subscription subscription) throws Exception {
        List<Object> params = form(subscription.getPrinting().getIndex(), subscription.getEmployeeId(),
                subscription.getStartingDate(), subscription.getEndingDate(), subscription.getPeriod(), subscription.getCost());
        params.addFirst(subscription.getId());
        params.remove(3);
        dbInterface.update(params, Subscription.class);
    }

    private List<Object> form(Integer index, Integer employeeId, String startingDate, String endingDate, Integer period, Integer cost) {
        List<Object> params = new ArrayList<>();
        params.add(index);
        params.add(employeeId);
        params.add(startingDate);
        params.add(endingDate);
        params.add(period);
        params.add(cost);
        return params;
    }

    public int deleteSubscription(SubscriptionSearch subscription) throws Exception {
        List<Object> params = setUpForDBOperation(subscription);
         dbInterface.delete(params, Subscription.class);
         return 0;
    }


}
