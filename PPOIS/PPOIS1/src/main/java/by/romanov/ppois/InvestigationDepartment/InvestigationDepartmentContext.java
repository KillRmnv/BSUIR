package by.romanov.ppois.InvestigationDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Entities.Case;
import by.romanov.ppois.Entities.SuspectSource;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
public class InvestigationDepartmentContext implements Context {
    private TransferData transfer;
    private List<Case> cases;
    private SuspectSource suspectSource;
    private Case CurrentCase;
    @JsonIgnore
    private UserInterface userInterface;
    @JsonIgnore
    private State choice;
    @JsonIgnore
    private Source source;
    public InvestigationDepartmentContext(){
        transfer = new TransferData();
        cases = new ArrayList<>();
        suspectSource = new SuspectSource();
        CurrentCase = new Case();
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        source=new JacksonSerializer();
    }
    public InvestigationDepartmentContext(SuspectSource suspectSource) {
        this.suspectSource = suspectSource;
        this.cases = new ArrayList<>();
        this.CurrentCase = new Case();
        transfer=new TransferData();
        userInterface=new ConsoleUserInterface(new ConsoleInput());
        source=new JacksonSerializer();
    }
    public InvestigationDepartmentContext(Input input) {
        this.cases = new ArrayList<>();
        this.CurrentCase = new Case();
        transfer=new TransferData();
        suspectSource=new SuspectSource();
        userInterface=new ConsoleUserInterface(input);
        source=new JacksonSerializer();
    }

    public void addCase(Case cases) {
        if (cases != null)
            this.cases.add(cases);
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
        return choice;
    }

}