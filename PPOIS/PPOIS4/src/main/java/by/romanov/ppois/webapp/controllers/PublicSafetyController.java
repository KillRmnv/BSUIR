package by.romanov.ppois.webapp.controllers;

import by.romanov.ppois.webapp.services.HRService;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Post;
import jakarta.inject.Inject;

@Controller("/views/publicSafetyDepartment")
public class PublicSafetyController {
    @Inject
    private HRService hrService;
    @Post("/chooseOperation")
    public String chooseOperation(int choice) {
    return null;
    }
    @Post("/schoolCampaign")
    public String PatrolSchool(int choice) {
        return null;
    }
    @Post("/patrolArea")
    public String PatrolArea(int choice) {
        return null;
    }
}
