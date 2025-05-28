package ppois.Romanov.data;

import org.sqlite.Function;
import ppois.Romanov.entities.Customer;
import ppois.Romanov.CustomerSearchCriteria;

import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SQLiteSource implements Source {
    private Connection connection;
    private Statement statement;

    private void registerRegexpFunction(Connection conn) throws SQLException {
        Function.create(conn, "REGEXP", new Function() {
            @Override
            protected void xFunc() throws SQLException {
                if (args() != 2) throw new SQLException("REGEXP requires 2 arguments.");
                String pattern = value_text(0);
                String value = value_text(1);
                if (value == null) {
                    result(0);
                    return;
                }
                result(value.matches(pattern) ? 1 : 0);
            }
        });
    }

    public SQLiteSource(String dbPath) throws ClassNotFoundException, SQLException {
        Class.forName("org.sqlite.JDBC");
        connection = DriverManager.getConnection("jdbc:sqlite:" + dbPath);
        System.out.println("Opened database successfully");
        statement = connection.createStatement();
        String tableCustomers = """
                CREATE TABLE IF NOT EXISTS Customers(
                FIO STRING  NOT NULL,
                ACCOUNT_NUMBER  STRING PRIMARY KEY NOT NULL,
                ADDRESS STRING
                );
                """;
        String tablePhones = """
                CREATE TABLE IF NOT EXISTS Phones(
                ACCOUNT_NUMBER  INTEGER PRIMARY KEY NOT NULL,
                MOBILE_PHONE TEXT,
                TOWN_PHONE TEXT
                );
                """;
        registerRegexpFunction(connection);
        statement.executeUpdate(tablePhones);
        statement.executeUpdate(tableCustomers);
        statement.close();
    }

    @Override
    public List<Customer> load(int start, int limit) throws SQLException {
        limit = limit - start;
        String sql = """
                    SELECT c.FIO, c.ACCOUNT_NUMBER, c.ADDRESS,
                           p.MOBILE_PHONE, p.TOWN_PHONE
                    FROM Customers c
                    JOIN Phones p ON c.ACCOUNT_NUMBER = p.ACCOUNT_NUMBER
                    ORDER BY c.ACCOUNT_NUMBER
                    LIMIT ? OFFSET ?;
                """;
        PreparedStatement stmt = connection.prepareStatement(sql);
        stmt.setInt(1, limit);
        if (start % 10 == 1)
            stmt.setInt(2, start - 1);
        else stmt.setInt(2, start);
        ResultSet rs = stmt.executeQuery();
        List<Customer> customers = new ArrayList<>();
        while (rs.next()) {
            Customer customer = new Customer();
            customer.setName(rs.getString("FIO"));
            customer.setAccountNumber(Integer.parseInt(rs.getString("ACCOUNT_NUMBER")));
            customer.setMobilePhone(rs.getString("MOBILE_PHONE"));
            customer.setTownPhone(rs.getString("TOWN_PHONE"));
            customer.setAddress(rs.getString("ADDRESS"));
            customers.add(customer);
        }
        return customers;
    }

    @Override
    public List<Customer> load(CustomerSearchCriteria condition) throws SQLException {
        StringBuilder sql = new StringBuilder("SELECT * FROM Customers WHERE ");
        var customers = findRecordsByNameAccountAddress(condition, sql);
        for (int record=0;record< customers.size();record++) {
            sql = new StringBuilder("SELECT * FROM Phones WHERE ACCOUNT_NUMBER REGEXP '.*").append(customers.get(record).getAccountNumber()).append(".*' AND ");
            if (condition == null) {
                sql.replace(sql.length() - 5, sql.length() - 1, "");
            } else
                formPhonesConditions(sql, condition);
            ResultSet records = connection.createStatement().executeQuery(sql.toString());
            if (records.next()) {
                customers.get(record).setMobilePhone(records.getString("MOBILE_PHONE"));
                customers.get(record).setTownPhone(records.getString("TOWN_PHONE"));
            }else{
                customers.remove(record);
                record --;
            }
        }
        return customers;
    }

    @Override
    public void save(List<Customer> records) throws Exception {
        for (var record : records) {
            add(record);
        }
    }

    @Override
    public boolean add(Customer record) throws SQLException {
        StringBuilder sql = new StringBuilder("INSERT INTO Customers(FIO,ACCOUNT_NUMBER,ADDRESS) VALUES ");
        sql.append("('").append(record.getName()).append("','").append(record.getAccountNumber()).append("','");
        sql.append(record.getAddress()).append("');");
        try {
            connection.createStatement().executeUpdate(sql.toString());
        } catch (Exception e) {
            return false;
        }

        sql = new StringBuilder("INSERT INTO Phones(ACCOUNT_NUMBER,MOBILE_PHONE,TOWN_PHONE) VALUES ");
        sql.append("('").append(record.getAccountNumber()).append("','").append(record.getMobilePhone()).append("','");
        sql.append(record.getTownPhone()).append("');");
        connection.createStatement().executeUpdate(sql.toString());
        return true;
    }

    @Override
    public int delete(CustomerSearchCriteria condition) throws Exception {
        List<Customer> customers = load(condition);

        if (customers.isEmpty()) {
            return 0;
        }

        int deletedCount = 0;
        for (Customer record : customers) {
            String sqlDeletePhones = "DELETE FROM Phones WHERE ACCOUNT_NUMBER = " + record.getAccountNumber();
            connection.createStatement().executeUpdate(sqlDeletePhones);

            String sqlDeleteCustomer = "DELETE FROM Customers WHERE ACCOUNT_NUMBER = " + record.getAccountNumber();
            deletedCount += connection.createStatement().executeUpdate(sqlDeleteCustomer);
        }

        return deletedCount;
    }

    @Override
    public int size() throws SQLException {
        String sql = "SELECT COUNT(*) FROM Customers;";
        Statement stmt = connection.createStatement();
        ResultSet rs = stmt.executeQuery(sql);
        int count = 0;
        if (rs.next()) {
            count = rs.getInt(1);
        }
        rs.close();
        stmt.close();
        return count;
    }


    private void formPhonesConditions(StringBuilder sqlPhones, CustomerSearchCriteria condition) {
        boolean mobPhone = false;
        if (condition.getMobilePhone() != null && !condition.getMobilePhone().isEmpty()) {
            sqlPhones.append("(MOBILE_PHONE REGEXP '.*");
            sqlPhones.append(condition.getMobilePhone()).append(".*'").append(" OR ");
            mobPhone = true;
        }
        if (condition.getTownPhone() != null && !condition.getTownPhone().isEmpty()) {
            sqlPhones.append("TOWN_PHONE REGEXP '.*");

                sqlPhones.append(condition.getTownPhone()).append(".*'");
            if (mobPhone)
                sqlPhones.append(" )");

        } else {
            sqlPhones.replace(sqlPhones.length() - 4, sqlPhones.length() - 1, "");
        }
    }

    private List<Customer> findRecordsByNameAccountAddress(CustomerSearchCriteria condition, StringBuilder sql) throws SQLException {

        if (condition != null) {
            if (!condition.getAccountNumber().isEmpty()) {
                sql.append("ACCOUNT_NUMBER REGEXP '.*").append(condition.getAccountNumber()).append(".*' AND ");
            }
            if (condition.getName() != null && !condition.getName().isEmpty()) {
                sql.append("FIO REGEXP '.*");
                sql.append(condition.getName()).append(".*' AND ");
            }
            if (condition.getAddress() != null && !condition.getAddress().isEmpty()) {
                sql.append("ADDRESS REGEXP '.*");
                sql.append(condition.getAddress()).append(".*'");
            } else {
                sql.replace(sql.length() - 5, sql.length() - 1, "");
            }
        } else {
            sql.replace(sql.length() - 7, sql.length() - 1, "");
        }
        ResultSet records = connection.createStatement().executeQuery(sql.toString());
        List<Customer> customers = new ArrayList<>();
        Map<Integer, Integer> indexByName = new HashMap<>();
        while (records.next()) {
            Customer record = new Customer();
            record.setAccountNumber(Integer.parseInt(records.getString("ACCOUNT_NUMBER")));
            record.setName(records.getString("FIO"));
            record.setAddress(records.getString("ADDRESS"));
            indexByName.put(Integer.parseInt(record.getAccountNumber()), customers.size());
            customers.add(record);
        }
        return customers;
    }

    @Override
    public void close() throws SQLException {
        connection.close();
    }
}