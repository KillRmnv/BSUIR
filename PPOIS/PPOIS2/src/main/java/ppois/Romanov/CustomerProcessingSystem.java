package ppois.Romanov;

import java.io.File;
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
        Source anthrSource;
        if(source.getClass().equals(ppois.Romanov.SQLiteSource.class)) {
            anthrSource=new XMLSource(new File("src/main/resources/xml/customers.xml"));

        }else{
            anthrSource=new SQLiteSource("src/main/resources/db/customers.db");
        }
        anthrSource.load(null);
        if(!anthrSource.add(customer)) {
            System.out.println("Customer not added into anthr source");
            return false;
        }
        if( !source.add(customer)){
            System.out.println("Customer not added into  source");
            anthrSource.delete(new CustomerSearchCriteria(customer));
            return false;
        }
        return true;
    }

    public int removeCustomer(CustomerSearchCriteria customer) throws Exception {
        Source anthrSource;
        if(source.getClass().equals(ppois.Romanov.XMLSource.class)) {
            anthrSource=new SQLiteSource("src/main/resources/db/customers.db");
        }else{
            anthrSource=new XMLSource(new File("src/main/resources/xml/customers.xml"));
        }
        anthrSource.delete(customer);

        return source.delete(customer);
    }
    public void migrate() throws Exception {
        Source anthrSource;
        if(source.getClass().equals(ppois.Romanov.XMLSource.class)) {
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
}