package by.romanov.ppois.webapp.controllers;

import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.webapp.services.ControlCentreService;
import io.micronaut.http.annotation.Body;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Post;
import jakarta.inject.Inject;

import java.util.List;
@Controller("/views/controlCentre")
public class ControlCentreController {
    @Inject
    private ControlCentreService controlCentreService;
    @Post("/chooseCase")
    public String chooseCase(@Body Case request) {
        return "chooseCase";
    }
    @Post("/contacts")
    public String contacts(List<String> contacts) {
        return "contacts";
    }
    @Post("/traits")
    public String traits() {
        return "traits";
    }
    @Get("/manipulatingSuspectSource/initial")
    public List<Suspect> manipulatingSuspectSource() {
        return null;
    }
    @Post("/manipulatingSuspectSource/deleteSuspect")
    public void deleteSuspect(String name) {

    }
    @Post("/manipulatingSuspectSource/addSuspect")
    public String addSuspect(@Body Suspect suspect) {
        return "addSuspect";
    }
}
