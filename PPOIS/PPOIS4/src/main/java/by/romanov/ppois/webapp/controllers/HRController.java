package by.romanov.ppois.webapp.controllers;

import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.webapp.services.HRService;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Post;
import jakarta.inject.Inject;

import java.util.Map;

@Controller("/views/hrDepartment")
public class HRController {

    @Inject
    private HRService hrService;

    @Post("/chooseOperation")
    public String chooseOperation(String operation) {
        return "chooseOperation";
    }

    @Post("/hirePoliceMan")
    public <T> Map<String, T> hirePoliceMan(PoliceMan policeMan) {
        return null;
    }

    @Post("/firePoliceMan")
    public <T> Map<String, T> firePoliceMan(Integer choice) {
        return null;
    }
}
