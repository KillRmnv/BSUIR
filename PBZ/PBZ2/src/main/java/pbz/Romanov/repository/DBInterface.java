package pbz.Romanov.repository;

import java.util.List;
import java.util.Map;

public interface DBInterface {

    boolean save(List<Object> entity, Class clazz) throws Exception;

    List<Map<String, Object>> find(List<Object> template_entity, Class clazz) throws Exception;

    int delete(List<Object> entity, Class clazz) throws Exception;

    int update(List<Object> entity, Class clazz) throws Exception;


}
