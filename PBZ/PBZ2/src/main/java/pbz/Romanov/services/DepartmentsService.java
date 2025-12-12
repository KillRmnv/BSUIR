package pbz.Romanov.services;

import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
import pbz.Romanov.entities.Department;
import pbz.Romanov.entities.search.DepartmentSearch;
import pbz.Romanov.repository.DBInterface;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Singleton
public class DepartmentsService {

    @Inject
    @Named("PostgreSQLRepository")
    private DBInterface dbInterface;

    public DepartmentsService(DBInterface dbInterface) {
        this.dbInterface = dbInterface;
    }

    public List<Department> getDepartments(DepartmentSearch filter) throws Exception {
        List<Object> params = setUpForDBOperation(filter);
        List<Map<String, Object>> result = dbInterface.find(params, Department.class);
        List<Department> departments = new ArrayList<>();
        for (Map<String, Object> row : result) {
            departments.add(new Department(
                    (int) row.get("department_id"),
                    (String) row.get("department_name")
            ));
        }
        return departments;
    }

    public void insertDepartment(Department department) throws Exception {
        dbInterface.save(List.of( department.getDepartmentName()), Department.class);
    }

    public void updateDepartment(Department department) throws Exception {
        dbInterface.update(form(department.getDepartmentId(), department.getDepartmentName()), Department.class);
    }

    public int deleteDepartment(DepartmentSearch filter) throws Exception {
        List<Object> params = setUpForDBOperation(filter);
         dbInterface.delete(params, Department.class);
         return 0;
    }

    private List<Object> setUpForDBOperation(DepartmentSearch department) {
        return form(department.getDepartmentId(), department.getDepartmentName());
    }

    private List<Object> form(Integer id, String name) {
        List<Object> params = new ArrayList<>();
        params.add(id);
        params.add(name);
        return params;
    }
}
