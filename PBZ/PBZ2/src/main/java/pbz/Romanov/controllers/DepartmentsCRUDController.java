package pbz.Romanov.controllers;

import io.micronaut.http.annotation.*;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.entities.Department;
import pbz.Romanov.entities.search.DepartmentSearch;
import pbz.Romanov.services.DepartmentsService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/Departments")
public class DepartmentsCRUDController {

    @Inject
    private final DepartmentsService departmentsService;

    public DepartmentsCRUDController(DepartmentsService departmentsService) {
        this.departmentsService = departmentsService;
    }

    @Get("/")
    @View("DepartmentsCRUD")
    public Map<String, Object> departmentsCRUDMenu() {
        return new HashMap<>();
    }

    @Post("/search/{page}")
    public List<Department> getDepartmentsNextPage(
            @PathVariable int page,
            @QueryValue int amountOnPage,
            @Body DepartmentSearch filter
    ) throws Exception {
        List<Department> fullList = departmentsService.getDepartments(filter);
        int fromIndex = (page - 1) * amountOnPage;
        int toIndex = Math.min(fromIndex + amountOnPage, fullList.size());
        if (fromIndex >= fullList.size()) return List.of();
        return fullList.subList(fromIndex, toIndex);
    }

    @Post("/create")
    public void createDepartment(@Body Department department) throws Exception {
        departmentsService.insertDepartment(department);
    }

    @Put("/update")
    public void updateDepartment(@Body DepartmentSearch department) throws Exception {
        departmentsService.updateDepartment(department);
    }

    @Post("/delete")
    public void deleteDepartment(@Body DepartmentSearch filter) throws Exception {
        departmentsService.deleteDepartment(filter);
    }
}
