package by.romanov.ppois.EnforcementDepartment;

import by.romanov.ppois.*;
import by.romanov.ppois.Police.PoliceStates.InitialState;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Data
public class EnforcementDepartmentContext implements Context {
    @JsonIgnore
    private Input input;
    private List<Case> cases;
    int choice;
    @JsonIgnore
    private State nextStage;
    private Map<Integer, PoliceMan> policeMans;
    private  int policeMan;
    private TransferData transfer;
   public EnforcementDepartmentContext(){
        policeMans = new HashMap<>();
        cases = new ArrayList<>();
        transfer=new TransferData();
        input=new ConsoleInput();
    }
    public EnforcementDepartmentContext(HashMap<Integer, PoliceMan> policeMans){
        this.policeMans = policeMans;
        cases = new ArrayList<>();
        input=new ConsoleInput();
        nextStage=new InitialState();
        transfer=new TransferData();
    }
    public EnforcementDepartmentContext(Input input){
       this.input=input;
       cases = new ArrayList<>();
       transfer=new TransferData();
       nextStage=new InitialState();
       this.policeMans = new HashMap<>();

    }
    public void addCase(Case newCase) {
        cases.add(newCase);
    }

    @Override
    public void setInput(Input input) {
        this.input= input;
    }

    @Override
    public Input getInput() {
        return  input;
    }

    @Override
    @JsonIgnore

    public State getNextState() {
        return new InitialState();
    }
    public void delCase(int index){
        cases.remove(index);
    }
}
