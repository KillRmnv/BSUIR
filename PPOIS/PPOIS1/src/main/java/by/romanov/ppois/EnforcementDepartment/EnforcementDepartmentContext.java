package by.romanov.ppois.EnforcementDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.PoliceMan;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import lombok.Setter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Data
public class EnforcementDepartmentContext implements Context {

    private List<Case> cases;
    private int choice;
    @JsonIgnore
    private UserInterface userInterface;
    @JsonIgnore
    private State nextStage;
    private Map<Integer, PoliceMan> policeMans;
    @Setter
    private int policeMan;
    private TransferData transfer;
    @JsonIgnore
    private Source source;

    public EnforcementDepartmentContext() {
        policeMans = new HashMap<>();
        cases = new ArrayList<>();
        transfer = new TransferData();
        userInterface = new ConsoleUserInterface(new ConsoleInput());
        source=new JacksonSerializer();
    }

    public EnforcementDepartmentContext(HashMap<Integer, PoliceMan> policeMans) {
        this.policeMans = policeMans;
        cases = new ArrayList<>();
        nextStage = new InitialState();
        transfer = new TransferData();
        userInterface = new ConsoleUserInterface(new ConsoleInput());
        source=new JacksonSerializer();
    }

    public EnforcementDepartmentContext(Input input) {
        cases = new ArrayList<>();
        transfer = new TransferData();
        nextStage = new InitialState();
        this.policeMans = new HashMap<>();
        userInterface = new ConsoleUserInterface(input);
        source=new JacksonSerializer();
    }

    public void addCase(Case newCase) {
        cases.add(newCase);
    }

    @Override
    public void setUserInterface(UserInterface userInterface) {
        this.userInterface = userInterface;
    }


    @Override
    public UserInterface getUserInterface() {
        return userInterface;
    }
    @JsonIgnore
    @Override
    public void setInput(Input input) {
        userInterface.setInput(input);
    }
    @JsonIgnore
    @Override
    public Input getInput() {
        return userInterface.getInput();
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return new InitialState();
    }

    public void delCase(int index) {
        cases.remove(index);
    }
}
