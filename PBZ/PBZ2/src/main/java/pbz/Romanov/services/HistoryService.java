package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.HistoryRecord;
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

    public List<HistoryRecord> getHistoryRecords(HistoryRecord record) throws Exception {
        List<Object> params = setUpForDBOperation(record);
        List<Map<String, Object>> result = dbInterface.find(params, HistoryRecord.class);
        List<HistoryRecord> records = new ArrayList<>();
        for (Map<String, Object> row : result) {
            records.add(new HistoryRecord( row.get("Дата").toString(),
                    (Integer) row.get("employee_id"),
                    (Integer) row.get("Издание"),
                    (Integer) row.get("Номер издания"),
                    (Integer) row.get("Выписан"),
                    (Integer) row.get("Получен")));
        }
        return records;
    }


    public void insertHistoryRecord(HistoryRecord record) throws Exception {
        List<Object> params = setUpForDBOperation(record);
        dbInterface.save(params, HistoryRecord.class);

    }

    private List<Object> setUpForDBOperation(HistoryRecord record) {
        List<Object> params = new ArrayList<>();
        params.add(record.getDate());
        params.add(record.getEmployee().getId());
        params.add(record.getPrinting());
        params.add(record.getNumOfPublication());
        params.add(record.getWriteOut());
        params.add(record.getReceived());
        return params;
    }

    public void updateHistoryRecord(HistoryRecord record) throws Exception {
        List<Object> params = setUpForDBOperation(record);
        dbInterface.update(params, HistoryRecord.class);
    }

    public int deleteHistoryRecord(HistoryRecord record) throws Exception {
        List<Object> params = setUpForDBOperation(record);
        return dbInterface.delete(params, HistoryRecord.class);
    }

}
