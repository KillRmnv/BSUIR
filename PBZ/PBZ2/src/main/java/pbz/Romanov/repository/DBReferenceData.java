package pbz.Romanov.repository;

import java.util.List;
import java.util.Map;


public interface DBReferenceData {

    List<Map<String, Object>> findAll(String tableName) throws Exception;

}
