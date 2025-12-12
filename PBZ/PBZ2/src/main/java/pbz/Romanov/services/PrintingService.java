package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.Printing;
import pbz.Romanov.entities.search.PrintingSearch;
import pbz.Romanov.repository.DBInterface;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Singleton
public class PrintingService {

    @Inject
    @Named("PostgreSQLRepository")
    private DBInterface dbInterface;

    public PrintingService(DBInterface dbInterface) {
        this.dbInterface = dbInterface;
    }

    public List<Printing> getPrintings(PrintingSearch filter) throws Exception {
        List<Object> params = setUpForDBOperation(filter);
        List<Map<String, Object>> result = dbInterface.find(params, Printing.class);
        List<Printing> printings = new ArrayList<>();
        for (Map<String, Object> row : result) {
            printings.add(new Printing(
                    (int) row.get("type_id"),
                    (int) row.get("index"),
                    (int) row.getOrDefault("freq_id", 0),
                    (String) row.get("name")
            ));
        }
        return printings;
    }

    public void insertPrinting(Printing printing) throws Exception {
        dbInterface.save(form(printing.getType(), printing.getIndex(), printing.getPeriod(), printing.getName()), Printing.class);
    }

    public void updatePrinting(Printing printing) throws Exception {
        dbInterface.update(form(printing.getType(), printing.getIndex(), printing.getPeriod(), printing.getName()), Printing.class);
    }

    public Integer deletePrinting(PrintingSearch filter) throws Exception {
        List<Object> params = setUpForDBOperation(filter);
         dbInterface.delete(params, Printing.class);
         return 0;
    }

    private List<Object> setUpForDBOperation(PrintingSearch printing) {
        return form(printing.getType(), printing.getIndex(), printing.getPeriod(), printing.getName());
    }

    private List<Object> form(Integer type, Integer index, Integer period, String name) {
        List<Object> params = new ArrayList<>();
        params.add(index);

        params.add(name);

        params.add(period);
        params.add(type);
        return params;
    }
}
