package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Employee;
import pbz.Romanov.services.EmployeesService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/Employees")
public class EmployeesCRUDController {
    @Inject
    private final EmployeesService employeesService;

    public EmployeesCRUDController(EmployeesService employeesService) {
        this.employeesService = employeesService;
    }

    @Get("/")
    @View("EmployeesCRUD")
    public Map<String, Object> employeesCRUDMenu() {
        return new HashMap<>();
    }

    @Get("/{page}")
    public List<Employee> getEmployeesNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @QueryValue(value = "id", defaultValue = "-1") int id,
            @QueryValue(value = "firstName", defaultValue = "") String firstname,
            @QueryValue(value = "secondName", defaultValue = "") String secondName,
            @QueryValue(value = "thirdName", defaultValue = "") String thirdName,
            @QueryValue(value = "position", defaultValue = "") String position,
            @QueryValue(value = "department", defaultValue = "") String department
    ) throws Exception {
        Employee filter = new Employee();
        if (id > -1)
            filter.setID(id);
        filter.setFirstName(firstname);
        filter.setSecondName(secondName);
        filter.setThirdName(thirdName);
        filter.setPosition(position);
        filter.setDepartment(department);
        List<Employee> fullList = employeesService.getEmployees(filter);
        int start = (page - 1) * amountOnPage;
        return fullList.subList(start, Math.min(start + amountOnPage, fullList.size()));
    }



    @Get("/create")
    public void createEmployee(@QueryValue(value = "id", defaultValue = "-1") int id,
            @QueryValue(value = "firstName", defaultValue = "") String firstname,
            @QueryValue(value = "secondName", defaultValue = "") String secondName,
            @QueryValue(value = "thirdName", defaultValue = "") String thirdName,
            @QueryValue(value = "position", defaultValue = "") String position,
            @QueryValue(value = "department", defaultValue = "") String department) throws Exception {
        Employee filter = new Employee();
        if (id > -1)
            filter.setID(id);
        filter.setFirstName(firstname);
        filter.setSecondName(secondName);
        filter.setThirdName(thirdName);
        filter.setPosition(position);
        filter.setDepartment(department);
        employeesService.insertEmployee(filter);
    }

    @Get("/update")
    public void updateEmployee(@QueryValue(value = "id", defaultValue = "-1") int id,
            @QueryValue(value = "firstName", defaultValue = "") String firstname,
            @QueryValue(value = "secondName", defaultValue = "") String secondName,
            @QueryValue(value = "thirdName", defaultValue = "") String thirdName,
            @QueryValue(value = "position", defaultValue = "") String position,
            @QueryValue(value = "department", defaultValue = "") String department) throws Exception {
        Employee filter = new Employee();
        if (id > -1)
            filter.setID(id);
        filter.setFirstName(firstname);
        filter.setSecondName(secondName);
        filter.setThirdName(thirdName);
        filter.setPosition(position);
        filter.setDepartment(department);
        employeesService.updateEmployee(filter);
    }

    @Get("/delete")
    public void deleteEmployee(@QueryValue(value = "id", defaultValue = "-1") int id,
            @QueryValue(value = "firstName", defaultValue = "") String firstname,
            @QueryValue(value = "secondName", defaultValue = "") String secondName,
            @QueryValue(value = "thirdName", defaultValue = "") String thirdName,
            @QueryValue(value = "position", defaultValue = "") String position,
            @QueryValue(value = "department", defaultValue = "") String department) throws Exception {
        Employee filter = new Employee();
        if (id > -1)
            filter.setID(id);
        filter.setFirstName(firstname);
        filter.setSecondName(secondName);
        filter.setThirdName(thirdName);
        filter.setPosition(position);
        filter.setDepartment(department);
        employeesService.deleteEmployee(filter);
    }
}
