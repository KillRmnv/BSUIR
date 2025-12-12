package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.Employee;
import pbz.Romanov.entities.search.EmployeeSearch;
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

    public List<Employee> getEmployees(EmployeeSearch employee) throws Exception {
        List<Object> params = setUpForDBOperation(employee);
        List<Map<String, Object>> result = dbInterface.find(params, Employee.class);
        List<Employee> employees = new ArrayList<>();
        for (Map<String, Object> row : result) {
            employees.add(new Employee((Integer) row.get("employee_id"), (String) row.get("first_name"),
                    (String) row.get("second_name"), (String) row.get("third_name"), (String) row.get("employee_position"),
                    (int) row.get("department_id")));
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

    private List<Object> setUpForDBOperation(EmployeeSearch employee) {
        return form(employee.getId(), employee.getSecondName(), employee.getFirstName(), employee.getThirdName(), employee.getPosition(), employee.getDepartment());
    }

    private List<Object> form(int id, String secondName, String firstName, String thirdName, String position, int department) {
        List<Object> params = new ArrayList<>();
        params.add(id);
        params.add(secondName);
        params.add(firstName);
        params.add(thirdName);
        params.add(position);
        params.add(department);
        return params;
    }

    public void updateEmployee(EmployeeSearch employee) throws Exception {
        List<Object> params = new ArrayList<>();
        params.add(employee.getId());
        if (employee.getSecondName().isEmpty())
            params.add(null);
        else
            params.add(employee.getSecondName());
        if (employee.getFirstName().isEmpty())
            params.add(null);
        else
            params.add(employee.getFirstName());
        if (employee.getThirdName().isEmpty())
            params.add(null);
        else
            params.add(employee.getThirdName());
        if (employee.getPosition().isEmpty())
            params.add(null);
        else
            params.add(employee.getPosition());

        params.add(employee.getDepartment());
        dbInterface.update(params, Employee.class);
    }

    public int deleteEmployee(EmployeeSearch employee) throws Exception {
        List<Object> params = setUpForDBOperation(employee);
         dbInterface.delete(params, Employee.class);
         return 0;
    }

}
