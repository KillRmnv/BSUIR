package by.romanov.ppois.webapp.controllers;
import java.util.Map;
import by.romanov.ppois.webapp.services.InvestigationService;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Post;
import jakarta.inject.Inject;

@Controller("/views/investigationDepartment")
public class InvestigationController {
    @Inject
    private InvestigationService investigationService;
    @Post("/chooseCase")
    public String chooseCase(int caseId) {
        return "chooseCase";
    }
    @Post("/interviewWitnesses")
    public<T> Map<String,T> interviewWitnesses(int caseId) {

        return null;
    }
}
