package ppois.Romanov;

import java.sql.SQLException;
import java.util.List;

public interface Source {
    List<Customer> load(CustomerSearchCriteria condition) throws Exception;

    void save(List<Customer> records) throws Exception;

    boolean add(Customer record) throws Exception;

    int delete(CustomerSearchCriteria condition) throws Exception;

    default List<Customer> load(int start, int limit) throws Exception {
        return null;
    }

    default void close() throws Exception {

    }
}