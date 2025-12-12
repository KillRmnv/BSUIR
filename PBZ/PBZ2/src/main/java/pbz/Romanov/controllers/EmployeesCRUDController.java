package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Employee;
import pbz.Romanov.entities.search.EmployeeSearch;
import pbz.Romanov.services.EmployeesService;
import pbz.Romanov.services.ReferenceDataService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/Employees")
public class EmployeesCRUDController {

    @Inject
    private final EmployeesService employeesService;
    @Inject
    private final ReferenceDataService referenceDataService;
    public EmployeesCRUDController(EmployeesService employeesService, ReferenceDataService referenceDataService) {
        this.employeesService = employeesService;
        this.referenceDataService = referenceDataService;
    }

    @Get("/")
    @View("EmployeesCRUD")
    public Map<String, Object> employeesCRUDMenu() throws Exception {
        Map<String, Object> model = new HashMap<>();
        model.put("reference",referenceDataService.getReferenceTable("Departments"));
        return model;
    }

    @Post("/search/{page}")
    public List<Employee> getEmployeesNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @Body EmployeeSearch filter
    ) throws Exception {
        List<Employee> fullList = employeesService.getEmployees(filter);
        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, fullList.size());
        if (fromIndex >= fullList.size()) return List.of();
        return fullList.subList(fromIndex, toIndex);
    }

    @Post("/create")
    public void createEmployee(@Body Employee employee) throws Exception {
        employeesService.insertEmployee(employee);
    }

    @Put("/update")
    public void updateEmployee(@Body EmployeeSearch employee) throws Exception {
        if (employee.getId() != null && employee.getId() < 1) {
            employee.setID(null);
        }

        if (employee.getDepartment() != null && employee.getDepartment() < 1) {
            employee.setDepartment(null);
        }

        if (employee.getId() == null) {
            throw new Exception("ID is required for update operation");
        }

        employeesService.updateEmployee(employee);
    }

    @Delete("/delete")
    public void deleteEmployee(@Body EmployeeSearch filter) throws Exception {
        employeesService.deleteEmployee(filter);
    }
}
