package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.Circulation;
import pbz.Romanov.entities.search.CirculationSearch;
import pbz.Romanov.repository.DBInterface;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Singleton
public class CirculationService {

    @Inject
    @Named("PostgreSQLRepository")
    private DBInterface dbInterface;

    public CirculationService(DBInterface dbInterface) {
        this.dbInterface = dbInterface;
    }

    public List<Circulation> getCirculations(CirculationSearch filter) throws Exception {
        List<Object> params = setUpForDBOperation(filter);
        List<Map<String, Object>> result = dbInterface.find(params, Circulation.class);
        List<Circulation> circulations = new ArrayList<>();
        for (Map<String, Object> row : result) {
            circulations.add(new Circulation(
                    (int) row.get("pub_id"),
                    (int) row.get("amount"),
                    (int) row.getOrDefault("allocated_amount", 0),
                    (int) row.get("num_of_pub")
            ));
        }
        return circulations;
    }

    public void insertCirculation(Circulation circulation) throws Exception {
        List<Object> params = new ArrayList<>();
        params.add(circulation.getPubId());
        params.add(circulation.getAmount());
        params.add(circulation.getNumOfPub());
        dbInterface.save(params, Circulation.class);
    }

    public void updateCirculation(Circulation circulation) throws Exception {
        dbInterface.update(form(circulation.getPubId(), circulation.getAmount(),
                circulation.getNumOfPub(), circulation.getAllocatedAmount()), Circulation.class);
    }

    public int deleteCirculation(CirculationSearch filter) throws Exception {
        List<Object> params = setUpForDBOperation(filter);
         dbInterface.delete(params, Circulation.class);
         return 0;
    }

    private List<Object> setUpForDBOperation(CirculationSearch circulation) {
        return form(circulation.getPubId(), circulation.getAmount(),
                circulation.getNumOfPub(), circulation.getAllocatedAmount());
    }

    private List<Object> form(Integer pubId, Integer amount, Integer numOfPub, Integer allocatedAmount) {
        List<Object> params = new ArrayList<>();
        params.add(pubId);
        params.add(amount);
        params.add(numOfPub);
        if(allocatedAmount != null)
        params.add(allocatedAmount);
        else
            params.add(0);
        return params;
    }
}
