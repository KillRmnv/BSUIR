package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Singleton;
import pbz.Romanov.repository.DBReferenceData;

import java.util.List;
import java.util.Map;

@Singleton
public class ReferenceDataService {

    @Inject
    private DBReferenceData dbReferenceData;

    public ReferenceDataService(DBReferenceData dbReferenceData) {
        this.dbReferenceData = dbReferenceData;
    }

    /**
     * Получение всех записей из справочной таблицы по имени таблицы
     * @param tableName имя таблицы в БД
     * @return список записей (Map<String, Object>)
     * @throws Exception
     */
    public List<Map<String, Object>> getReferenceTable(String tableName) throws Exception {
        return dbReferenceData.findAll(tableName);
    }

    /**
     * Получение всех справочников с отображаемым именем и классом
     * @return список справочников
     * @throws Exception
     */
    public List<Map<String, Object>> getAllReferenceTables() throws Exception {
        return dbReferenceData.findAll("reference_tables");
    }

}