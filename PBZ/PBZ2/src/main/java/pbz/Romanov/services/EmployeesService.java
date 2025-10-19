package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.Employee;
import pbz.Romanov.repository.DBInterface;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Singleton
public class EmployeesService {
    @Inject
    @Named("PostgreSQLRepository")
    private DBInterface dbInterface;

    public EmployeesService(DBInterface dbInterface) {
        this.dbInterface = dbInterface;
    }

    public List<Employee> getEmployees(Employee employee) throws Exception {
        List<Object> params = setUpForDBOperation(employee);
        List<Map<String, Object>> result = dbInterface.find(params, Employee.class);
        List<Employee> employees = new ArrayList<>();
        for (Map<String, Object> row : result) {
            employees.add(new Employee((Integer) row.get("employee_id"), (String) row.get("Фамилия"),
                    (String) row.get("Имя"), (String) row.get("Отчество"), (String) row.get("Должность"),
                    (String) row.get("Подразделение"), List.of()));
        }
        return employees;
    }


    public void insertEmployee(Employee employee) throws Exception {
        List<Object> params = new ArrayList<>();
        params.add(employee.getSecondName());
        params.add(employee.getFirstName());
        params.add(employee.getThirdName());
        params.add(employee.getPosition());
        params.add(employee.getDepartment());
        dbInterface.save(params, Employee.class);
    }

    private List<Object> setUpForDBOperation(Employee employee) {
        List<Object> params = new ArrayList<>();
        params.add(employee.getId());
        params.add(employee.getSecondName());
        params.add(employee.getFirstName());
        params.add(employee.getThirdName());
        params.add(employee.getPosition());
        params.add(employee.getDepartment());
        return params;
    }

    public void updateEmployee(Employee employee) throws Exception {
        List<Object> params = setUpForDBOperation(employee);
        dbInterface.update(params, Employee.class);
    }

    public int deleteEmployee(Employee employee) throws Exception {
        List<Object> params = setUpForDBOperation(employee);
        return dbInterface.delete(params, Employee.class);
    }

}
