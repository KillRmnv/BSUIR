package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.HistoryRecord;
import pbz.Romanov.entities.search.HistoryRecordSearch;
import pbz.Romanov.repository.DBInterface;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Singleton
public class HistoryService {
    @Inject
    @Named("PostgreSQLRepository")
    private DBInterface dbInterface;

    public HistoryService(DBInterface dbInterface) {
        this.dbInterface = dbInterface;
    }

    public List<HistoryRecord> getHistoryRecords(HistoryRecordSearch record) throws Exception {
        List<Object> params = setUpForDBOperation(record);
        params.addFirst(record.getId());
        List<Map<String, Object>> result = dbInterface.find(params, HistoryRecord.class);
        List<HistoryRecord> records = new ArrayList<>();
        for (Map<String, Object> row : result) {
            records.add(new HistoryRecord(  (Integer) row.get("id"),
                    row.get("date_hist").toString(),
                    (Integer) row.get("num_pub"),
                    (Integer) row.get("state_id"),
                    (Integer) row.get("subscription_id"))
            );
        }
        return records;
    }


    public void insertHistoryRecord(HistoryRecord record) throws Exception {
        List<Object> params = new ArrayList<>();
        params.add(record.getDate());
        params.add(record.getSub());
        params.add(record.getNumOfPublication());
        params.add(record.getState());
        dbInterface.save(params, HistoryRecord.class);

    }

    private List<Object> setUpForDBOperation(HistoryRecordSearch record) {
        List<Object> params = new ArrayList<>();
        params.add(record.getDate());
        params.add(record.getSub());
        params.add(record.getNumOfPublication());
        params.add(record.getState());
        return params;
    }

    public void updateHistoryRecord(HistoryRecord record) throws Exception {
        List<Object> params = new ArrayList<>();
        params.add(record.getDate());
        params.add(record.getSub());
        params.add(record.getNumOfPublication());
        params.add(record.getState());
        params.addFirst(record.getId());
        dbInterface.update(params, HistoryRecord.class);
    }

    public int deleteHistoryRecord(HistoryRecordSearch record) throws Exception {
        List<Object> params = setUpForDBOperation(record);
         dbInterface.delete(params, HistoryRecord.class);
         return 0;
    }

}
