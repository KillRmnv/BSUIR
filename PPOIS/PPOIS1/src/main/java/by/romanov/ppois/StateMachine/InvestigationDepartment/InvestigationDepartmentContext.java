package by.romanov.ppois.StateMachine.InvestigationDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Entities.Suspect;
import by.romanov.ppois.Repository.*;
import by.romanov.ppois.Service.InvestigationService;
import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.SuspectSource;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.Ui.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Data
public class InvestigationDepartmentContext implements Context {
    private TransferData transfer;
    @JsonIgnore
    private ConsoleUserInterface userInterface;
    @JsonIgnore
    private State choice;
    @JsonIgnore
    private InvestigationService investigationService;

    public InvestigationDepartmentContext() {
        transfer=new TransferData();
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        investigationService=new InvestigationService();
    }
    public InvestigationDepartmentContext(ConsoleUserInterface userInterface) {
        transfer=new TransferData();
        this.userInterface=userInterface;
        investigationService=new InvestigationService();
    }
    public InvestigationDepartmentContext(ConsoleUserInterface userInterface,Repository<List<Case>, Case, Integer> casesRepository,
                                          Repository<SuspectSource, Suspect,String> suspectsRepository) {
        investigationService=new InvestigationService(casesRepository,suspectsRepository);
        transfer=new TransferData();
        this.userInterface=userInterface;

    }
    public void addCase(Case cases) throws IOException {
        if (cases != null) {
            investigationService.getCaseRepository().add(cases);
        }
    }
    public List<Case> findActiveCases() throws IOException {
        var cases=investigationService.getCaseRepository().loadAll();
        List<Case> activeCases = new ArrayList<>();
        for(var caseToCheck:cases) {
            if(caseToCheck.isActive()){
                activeCases.add(caseToCheck);
            }
        }
        return activeCases;
    }
    @JsonIgnore
    @Override
    public void setInput(ConsoleInput input) {
        userInterface.setConsoleInput(input);
    }
    @JsonIgnore
    @Override
    public ConsoleInput getInput() {
        return userInterface.getConsoleInput();
    }
    @Override
    @JsonIgnore
    public State getNextState() {
        return choice;
    }
}