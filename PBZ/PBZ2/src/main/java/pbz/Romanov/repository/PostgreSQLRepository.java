package pbz.Romanov.repository;

import jakarta.inject.Singleton;

import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Singleton
public class PostgreSQLRepository implements DBInterface, DBMainMenuInterface,DBReferenceData {
    private final DataSource dataSource;

    public PostgreSQLRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    private String get_function_name(String className, String one_symbol_operation) throws Exception {
        String get_function_name = "SELECT * FROM get_function_name(?,?)";
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(get_function_name);
            stmt.setString(1, className);
            stmt.setString(2, one_symbol_operation);
            var rs=stmt.executeQuery();
            if (rs.next()) {
                return rs.getString(1);
            }

        }catch (SQLException e) {
            throw new Exception(e.getMessage());
        }
        return "";
    }

    @Override
    public boolean save(List<Object> entity, Class clazz) throws Exception {
        StringBuilder sql = new StringBuilder();
        sql.append("CALL ").append(get_function_name(clazz.getSimpleName(), "c"));
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(sql.toString());
            for (int i = 0; i < entity.size(); i++) {
                stmt.setObject(i + 1, entity.get(i));
            }

            stmt.executeUpdate();

            return true;
        }catch (SQLException e) {
            throw new Exception(e.getMessage());
        }

    }

    @Override
    public List<Map<String, Object>> find(List<Object> template_entity, Class clazz) throws Exception {
        StringBuilder sql = new StringBuilder();
        sql.append("SELECT * FROM ").append(get_function_name(clazz.getSimpleName(), "r"));
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(sql.toString());
            for (int i = 0; i < template_entity.size(); i++) {
                stmt.setObject(i + 1, template_entity.get(i));
            }
            return getMaps(stmt);
        }catch (SQLException e) {
            throw new Exception(e.getMessage());
        }

    }

    @Override
    public void delete(List<Object> entity, Class clazz) throws Exception {
        StringBuilder sql = new StringBuilder();
        sql.append("CALL ").append(get_function_name(clazz.getSimpleName(), "d"));
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(sql.toString());
            for (int i = 0; i < entity.size(); i++) {
                stmt.setObject(i + 1, entity.get(i));
            }
            stmt.executeUpdate();
        }catch (SQLException e) {
            throw new Exception(e.getMessage());
        }

    }

    @Override
    public int update(List<Object> entity, Class clazz) throws Exception {
        StringBuilder sql = new StringBuilder();
        sql.append("CALL ").append(get_function_name(clazz.getSimpleName(), "u"));
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(sql.toString());
            for (int i = 0; i < entity.size(); i++) {
                stmt.setObject(i + 1, entity.get(i));
            }
            stmt.executeUpdate();

        }catch (SQLException e) {
                throw new Exception(e.getMessage());
            }
        return 0;
    }

    @Override
    public List<Map<String, Object>> findPrintingsByStateAndType(String state_var, String type_var) throws Exception {

        String sql = "SELECT * FROM find_printings_by_state_and_type(?,?)";
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(sql);

            stmt.setString(1, state_var);

            stmt.setString(2, type_var);
            return getMaps(stmt);
        }catch (SQLException e) {
                throw new Exception(e.getMessage());
            }

    }

    @Override
    public List<Map<String, Object>> printingsForYear(int year) throws Exception {
        String sql = "SELECT * FROM printings_for_year(?)";
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(sql);

            stmt.setInt(1, year);


            return getMaps(stmt);
        } catch (SQLException e) {
            throw new Exception(e.getMessage());
        }

    }

    private List<Map<String, Object>> getMaps(String sql) throws SQLException {
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(sql);
            return getMaps(stmt);
        }
    }

    @Override
    public List<Map<String, Object>> unrecievedPrintingsForTwoMonths() throws Exception {
        String sql = "SELECT * FROM amount_of_unrecieved_printings_for_two_months()";
        return getMaps(sql);
    }

    @Override
    public List<Map<String, Object>> employeesByMonthAndDepartment(int department, String Date, int name) throws Exception {
        String sql = "SELECT * FROM employees_by_month_and_department(?,?::date,?)";
        try (Connection conn = dataSource.getConnection()) {
            PreparedStatement stmt = conn.prepareStatement(sql);

            stmt.setInt(1, department);

            stmt.setString(2, Date);
            stmt.setInt(3, name);
            return getMaps(stmt);
        } catch (SQLException e) {
                throw new Exception(e.getMessage());
            }

    }

    private List<Map<String, Object>> getMaps(PreparedStatement stmt) throws SQLException {
        List<Map<String, Object>> rows = new ArrayList<>();
        try (ResultSet rs = stmt.executeQuery()) {
            ResultSetMetaData meta = rs.getMetaData();
            int columnCount = meta.getColumnCount();
            while (rs.next()) {
                Map<String, Object> row = new HashMap<>();
                for (int i = 1; i <= columnCount; i++) {
                    row.put(meta.getColumnName(i), rs.getObject(i));
                }
                rows.add(row);
            }
        }
        return rows;
    }

    @Override
    public List<Map<String, Object>> findAll(String tableName) throws Exception {
        String sql = "SELECT * FROM " + tableName;
        try (Connection conn = dataSource.getConnection();
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            return getMaps(stmt);
        } catch (SQLException e) {
            throw new Exception("Ошибка при загрузке справочной таблицы '" + tableName + "': " + e.getMessage(), e);
        }
    }


}
