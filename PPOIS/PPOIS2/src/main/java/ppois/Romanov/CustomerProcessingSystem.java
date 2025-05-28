package ppois.Romanov;

import ppois.Romanov.data.SQLiteSource;
import ppois.Romanov.data.Source;
import ppois.Romanov.data.XMLSource;
import ppois.Romanov.entities.Customer;

import java.io.File;
import java.sql.SQLException;
import java.util.List;

public class CustomerProcessingSystem {
    private Source source;

    public CustomerProcessingSystem(Source source) {
        this.source = source;
    }

    public List<Customer> loadCustomers(CustomerSearchCriteria templateCustomer) throws Exception {
        return source.load(templateCustomer);
    }

    public List<Customer> loadCustomers(int start, int end) throws Exception {
        return source.load(start, end);
    }

    public boolean addCustomer(Customer customer) throws Exception {
        return source.add(customer);
    }

    public int removeCustomer(CustomerSearchCriteria customer) throws Exception {
        return source.delete(customer);
    }
    public void migrate() throws Exception {
        Source anthrSource;
        if(source.getClass().equals(XMLSource.class)) {
            anthrSource=new SQLiteSource("src/main/resources/db/customers.db");
        }else{
            anthrSource=new XMLSource(new File("src/main/resources/xml/customers.xml"));
        }
        List<Customer> customers=source.load(null);
        anthrSource.save(customers);
    }
    public void close() throws Exception {
        source.close();
    }
    public int getSize() throws SQLException {
       return source.size();
    }
}