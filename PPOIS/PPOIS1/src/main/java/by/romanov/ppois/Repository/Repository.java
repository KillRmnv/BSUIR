package by.romanov.ppois.Repository;

import java.io.IOException;

public interface Repository<Source,Record,Key> {
    void saveAll(Source source) throws IOException;
    Source loadAll() throws IOException;
    boolean delete(Record record) throws IOException;
    void add(Record data) throws IOException;
    Record load(Key key) throws IOException;
}