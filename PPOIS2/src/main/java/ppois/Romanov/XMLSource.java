package ppois.Romanov;

import java.io.File;
import java.util.List;
import java.util.function.Predicate;

public class XMLSource implements Source {
    private File file;
    public XMLSource(File file) {
        this.file = file;
    }

    @Override
    public List<Customer> load(Predicate<Customer> conditions) { /* парсим XML с помощью SAX */
        return null;
    }

    @Override
    public void save(List<Customer> records) { /* пишем XML с помощью DOM */ }

    @Override
    public void add(Customer record) { /* добавляем в XML */ }

    @Override
    public void delete(Predicate<Customer> condition) { /* удаляем из XML */ }
}

