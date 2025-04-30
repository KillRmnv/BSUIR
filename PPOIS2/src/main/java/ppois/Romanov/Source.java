package ppois.Romanov;

import java.util.List;
import java.util.function.Predicate;

public interface Source {
    List<Customer> load(Predicate<Customer> conditions) throws Exception;
    void save(List<Customer> records) throws Exception;
    void add(Customer record) throws Exception;
    void delete(Predicate<Customer> condition) throws Exception;

}

