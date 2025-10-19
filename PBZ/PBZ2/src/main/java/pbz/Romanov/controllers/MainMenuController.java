package pbz.Romanov.controllers;

import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.services.MainMenuService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/")
public class MainMenuController {
    @Inject
    private final MainMenuService mainMenuService;

    public MainMenuController(MainMenuService mainMenuService) {
        this.mainMenuService = mainMenuService;
    }

    @Get("/")
    @View("MainMenu")
    public Map<String, Object> updateMainMenu() {
        return new HashMap<>();
    }

    @Get("/employees_table")
    public List<Map<String, Object>> employeesByMonthAndDepartmentTable(String department, String Date, String name, int page, int amountOnPage) throws Exception {
        return mainMenuService.employeesByMonthAndDepartment(department, Date, name,page,amountOnPage);
    }

    @Get("/unrecieved_table")
    public List<Map<String, Object>> unrecievedPrintingsForTwoMonths(int page, int amountOnPage) throws Exception {

        return mainMenuService.unrecievedPrintingsForTwoMonths(page, amountOnPage);
    }

    @Get("/printings_for_year_table")
    public List<Map<String, Object>> printingsForYear(int page, int amountOnPage) throws Exception {
        return mainMenuService.printingsForYear(page, amountOnPage);
    }

    @Get("/printings_by_state_table")
    public List<Map<String, Object>> findPrintingsByStateAndType(String state_var, String type_var, int page, int amountOnPage) throws Exception {
        return mainMenuService.findPrintingsByStateAndType(state_var, type_var,page,amountOnPage);
    }
}