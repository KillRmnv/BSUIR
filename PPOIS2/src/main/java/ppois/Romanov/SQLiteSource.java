package ppois.Romanov;

import java.sql.*;
import java.util.List;
import java.util.function.Predicate;

public class SQLiteSource implements Source {
    private Connection connection;
    private Statement statement;

    public SQLiteSource(String dbPath) throws ClassNotFoundException, SQLException {
        Class.forName("org.sqlite.JDBC");
        connection = DriverManager.getConnection("jdbc:sqlite:" + dbPath);
        System.out.println("Opened database successfully");
        statement = connection.createStatement();
        String tableCustomers= """
                CREATE TABLE IF NOT EXISTS Customers(
                FIO TEXT PRIMARY KEY NOT NULL,
                ACCOUNT_NUMBER INTEGER NOT NULL,
                ADDRESS TEXT,
                PHONES TABLE
                );
                """;
        String tablePhones= """
                CREATE TABLE IF NOT EXISTS Phones(
                FIO TEXT PRIMARY KEY NOT NULL,
                MOBILE_PHONE TEXT PRIMARY KEY,
                TOWN_PHONE TEXT
                );
                """;
        statement.executeUpdate(tablePhones);
        statement.executeUpdate(tableCustomers);
        statement.close();
    }

    @Override
    public List<Customer> load(Predicate<Customer> conditions) {
        return null;
    }

    @Override
    public void save(List<Customer> records) throws Exception {

    }

    @Override
    public void add(Customer record) {

    }

    @Override
    public void delete(Predicate<Customer> condition) throws Exception {

    }

}

