package by.romanov.ppois.StateMachine.EnforcementDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Repository.*;
import by.romanov.ppois.Service.EnforcementService;
import by.romanov.ppois.StateMachine.Context;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.StateMachine.Police.PoliceStates.InitialState;
import by.romanov.ppois.StateMachine.State;
import by.romanov.ppois.Ui.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

@Data
public class EnforcementDepartmentContext implements Context {

    private int choice;
    @JsonIgnore
    private ConsoleUserInterface userInterface;
    @JsonIgnore
    private State nextStage;
    @JsonIgnore
    private Repository<HashMap<Integer, PoliceMan>, PoliceMan, Integer> policeManRepository;
    @JsonIgnore
    private EnforcementService enforcementService;
    private int policeMan;
    private TransferData transfer;


    public EnforcementDepartmentContext() {

        transfer = new TransferData();
        userInterface = new ConsoleUserInterface(new ConsoleInput());
        nextStage = new InitialState();
        enforcementService=new EnforcementService();
        policeManRepository=new PoliceMansJsonRepository();
    }


    public EnforcementDepartmentContext(ConsoleUserInterface userInterface) {

        transfer = new TransferData();
        nextStage = new InitialState();
        enforcementService=new EnforcementService();
        policeManRepository=new PoliceMansJsonRepository();
        this.userInterface = userInterface;


    }

    public List<Case> findActiveCases() throws IOException {
        var cases=enforcementService.getActiveCases();
        List<Case> activeCases = new ArrayList<>();
        for(var caseToCheck:cases) {
            if(!caseToCheck.isActive()){
                activeCases.add(caseToCheck);
            }
        }
        return activeCases;
    }
@JsonIgnore
    @Override
    public ConsoleUserInterface getUserInterface() {
        return userInterface;
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
        return new InitialState();
    }
}