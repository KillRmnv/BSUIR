package by.romanov.ppois.InvestigationDepartment;

import by.romanov.ppois.*;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
public class InvestigationDepartmentContext implements Context {
    private TransferData transfer;
    @JsonIgnore
    private Input input;
    private List<Case> cases;
    private SuspectSource suspectSource;
    private Case CurrentCase;
    @JsonIgnore
    private State choice;
    public InvestigationDepartmentContext(){
        transfer = new TransferData();
        cases = new ArrayList<>();
        suspectSource = new SuspectSource();
        CurrentCase = new Case();
        input=new ConsoleInput();
    }
    public InvestigationDepartmentContext(SuspectSource suspectSource) {
        this.suspectSource = suspectSource;
        this.cases = new ArrayList<>();
        this.CurrentCase = new Case();
        input=new ConsoleInput();
        transfer=new TransferData();
    }
    public InvestigationDepartmentContext(Input input) {
        this.input = input;
        this.cases = new ArrayList<>();
        this.CurrentCase = new Case();
        transfer=new TransferData();
        suspectSource=new SuspectSource();
    }

    public void addCase(Case cases) {
        if (cases != null)
            this.cases.add(cases);
    }

    public void delCasenSuspect() {
        //TODO: implement
        suspectSource.deleteSuspect(CurrentCase.getSuspects().getFirst().getFullName());
        cases.remove(CurrentCase);
    }

    @Override
    public void setInput(Input input) {
        this.input =  input;
    }

    @Override
    public Input getInput() {
        return (Input) input;
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return choice;
    }

}