package pbz.Romanov.controllers;

import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.views.View;
import jakarta.inject.Inject;
import pbz.Romanov.services.MainMenuService;
import pbz.Romanov.services.ReferenceDataService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller("/")
public class MainMenuController {
    @Inject
    private final MainMenuService mainMenuService;
    @Inject
    private  final ReferenceDataService referenceDataService;
    public MainMenuController(MainMenuService mainMenuService, ReferenceDataService referenceDataService) {
        this.mainMenuService = mainMenuService;
        this.referenceDataService = referenceDataService;
    }

    @Get("/")
    @View("MainMenu")
    public Map<String, Object> updateMainMenu() throws Exception {
        Map<String, Object> model = new HashMap<>();
        model.put("references",referenceDataService.getReferenceTable("Departments"));
        return model;
    }

    @Get("/employees_table")
    public List<Map<String, Object>> employeesByMonthAndDepartmentTable(int department, String Date, int index, int page, int amountOnPage) throws Exception {
        return mainMenuService.employeesByMonthAndDepartment(department, Date, index,page,amountOnPage);
    }

    @Get("/unrecieved_table")
    public List<Map<String, Object>> unrecievedPrintingsForTwoMonths(int page, int amountOnPage) throws Exception {

        return mainMenuService.unrecievedPrintingsForTwoMonths(page, amountOnPage);
    }

    @Get("/printings_for_year_table")
    public List<Map<String, Object>> printingsForYear(int page, int amountOnPage,int year) throws Exception {
        return mainMenuService.printingsForYear(page, amountOnPage,year);
    }

    @Get("/printings_by_state_table")
    public List<Map<String, Object>> findPrintingsByStateAndType(String state_var, String type_var, int page, int amountOnPage) throws Exception {
        return mainMenuService.findPrintingsByStateAndType(state_var, type_var,page,amountOnPage);
    }
}