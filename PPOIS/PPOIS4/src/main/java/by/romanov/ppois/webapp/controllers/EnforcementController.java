package by.romanov.ppois.webapp.controllers;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.webapp.services.EnforcementService;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Post;
import jakarta.inject.Inject;

import java.util.Map;

@Controller("/views/enforcementDepartment")
public class EnforcementController {
    @Inject
    private EnforcementService enforcementService;

    @Post("/chooseCase")
    public String chooseCase(Case request) {
        return "chooseCase";
    }

    @Post("/choosePoliceMan")
    public String choosePoliceMan(int policeManId) {
        return "choosePoliceMan";
    }

    @Post("/catchSuspect")
    public <T> Map<String, T> catchSuspect(Map<String, T> request) {
        return null;
    }
}
